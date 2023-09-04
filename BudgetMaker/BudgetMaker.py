from csv import DictReader
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

# Define in which column 'beløb' is defiend in the csv file
BELOEB = 1
# Define in which column your 'emne' / subject is defined in the csv file
EMNE = 9

class Value:
    def __init__(self, key:str, val:float) -> None:
        self.values = dict(str, Value)
        self.val = float()
        self.delimiter = ','

        self.add(key, val)

    def add(self, key:str, val:float):
        k = key.strip()
        val = Value

        if (self.delimiter in k):
            parent_subj = key.split(',')[0]

        

    def __str__(self):
        for k, v in self.child_values.items():
            return ""



# Main class for reading the csv file from the bank
class Reader:
    def __init__(self, file, delimiter) -> None:
        self.f = DictReader(file, delimiter=delimiter)
        self.total = 0.0
        self.subjects = dict()
        self.child_subjects = dict()
        self.parents = set([])
        self._init_values()
        self._round_attributes()

    def _init_values(self):
        for row in self.f:
            # Get 'Beløb'/amount
            val = row[self.f.fieldnames[BELOEB]]
            # Replace , with . so it can be converted to float
            val = val.replace('.', '')
            val = val.replace(',', '.')
            # Convert string to float
            try:
                cash = float(val)
            except Exception:
                print("Could not convert row", row)
                continue

            #print(row, '\n' ,cash)

            # Get 'Emne'/subject
            subj = row[self.f.fieldnames[EMNE]]
            if subj is None:
                subj = 'Ignore'
            else:
                subj = subj.strip()

            # If there is a parent in the subj name, it is separeted by comma
            if ',' in subj:
                # Get parent
                parent_subj = subj.split(',')[0]
                if parent_subj != subj:
                    # Add cash to child
                    if subj not in self.child_subjects:
                        self.child_subjects[subj] = cash
                    else:
                        self.child_subjects[subj] += cash
                    subj = parent_subj
                    self.parents.add(parent_subj)

            # Add cash to its subject
            if subj not in self.subjects:
                self.subjects[subj] = cash
            else:
                self.subjects[subj] += cash

            if subj != "Ignore":
                self.total += cash

    def _round_attributes(self):
        self.total = round(self.total, 2)
        for key in self.subjects:
            self.subjects[key] = round(self.subjects[key], 2)
            
# Main class for writing to a new excel file
class Writer(Workbook):
    def __init__(self, reader: Reader) -> None:
        super().__init__()
        self.ws: Worksheet = self.active  # Used for convenient typehint
        self.reader = reader

    def append_subjects(self, sort:bool=False):
        subjects = self.reader.subjects
        total = 0.0

        if sort:
            subjects = dict(sorted(subjects.items(), key=lambda item: item[1]))

        print(subjects)

        for key, val in subjects.items():
            self.active.append([key, val])
            total += val

            child_dict = self._get_children(key)

            for orphant, val2 in child_dict.items():
                self.active.append([orphant, val2])
        
        self.active.append([])
        self.active.append(["I alt", total])



    def _get_children(self, parent) -> dict:
        ret = dict()
        child_subjects: dict(str, float) = self.reader.child_subjects
        # print("Parent: " + parent)
        for child, val in child_subjects.items():
            if parent in child:
                # Remove parent from child
                orphant:str = child[len(parent):]
                orphant = orphant.replace(',', ' - ')
                ret[orphant] = val
        
        return ret

# Main script
with open("Raw.csv", encoding='UTF-8-SIG', mode='r') as f_raw:
    reader = Reader(f_raw, ';')
    writer = Writer(reader)
    ws: Worksheet = writer.active

    writer.append_subjects(sort=True)

    writer.save("Test.xlsx")