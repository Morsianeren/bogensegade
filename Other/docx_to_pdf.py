import os
import comtypes.client # pip install comtypes

def docx_to_pdf(docx_path, pdf_path):
    """
    Convert a docx file to pdf using Microsoft Word.
    
    :param docx_path: Path to the .docx file
    :param pdf_path: Path where the .pdf file will be saved
    """
    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(docx_path)
    doc.SaveAs(pdf_path, FileFormat=17)
    doc.Close()
    word.Quit()

if __name__ == "__main__":
    folder_path = os.getcwd()
    pdf_folder = os.path.join(folder_path, 'PDF')

    # Create 'PDF' folder if it does not exist
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)
    
    for file in os.listdir(folder_path):
        if file.endswith(".docx"):
            docx_file = os.path.join(folder_path, file)
            pdf_file_name = os.path.splitext(file)[0] + '.pdf'
            pdf_file = os.path.join(pdf_folder, pdf_file_name)
            docx_to_pdf(docx_file, pdf_file)
            print(f'Converted: {file} to PDF')