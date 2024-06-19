using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.IO;
using Newtonsoft.Json;
using Microsoft.Win32;
using System.Diagnostics;

namespace BogensegadeUI.View
{

    public class ApartmentInfo
    {
        [JsonProperty("id")]
        public string Id { get; set; }
        [JsonProperty("Boligafgift")]
        public int Boligafgift { get; set; }
        [JsonProperty("Faellesudgifter")]
        public int Faellesudgifter { get; set; }

        [JsonProperty("Aconto varme")]
        public int AcontoVarme { get; set; }
        [JsonProperty("Aconto vand")]
        public int AcontoVand { get; set; }
        [JsonProperty("Kontobeskeder")]
        public string Kontobeskeder { get; set; }
    }

    /// <summary>
    /// Interaction logic for Boligydelse.xaml
    /// </summary>
    public partial class Boligydelse : UserControl
    {
        public string JsonFilePath { get; private set; }
        public string CsvFilePath { get; private set; }
        public List<ApartmentInfo> ApartmentInfos { get; set; }

        public Boligydelse()
        {
            InitializeComponent();
            this.DataContext = this;

            // Initialize datagrid with a empty json
            ApartmentInfos = new List<ApartmentInfo>();
            datagridApartmentInfo.ItemsSource = ApartmentInfos;
        }

        private void LoadApartmentInfo(string path)
        {
            if (!File.Exists(path))
            {
                return;
            }

            string jsonData = File.ReadAllText(path);
            List<ApartmentInfo>? info = JsonConvert.DeserializeObject<List<ApartmentInfo>>(jsonData);

            if (info != null && info.Count > 0)
            {
                ApartmentInfos = info;
                datagridApartmentInfo.ItemsSource = ApartmentInfos;
            }
        }

        private void ActivateButtons()
        {
            if (File.Exists(JsonFilePath))
            {
                btnSaveApartmentInfo.IsEnabled = true;

                if (File.Exists(CsvFilePath))
                    btnBuildOverview.IsEnabled = true;
            }
        }

        private void btnLoadApartmentInfo_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog fileDialog = new OpenFileDialog();
            fileDialog.Filter = "JSON files (*.txt)|*.json|All files (*.*)|*.*";
            bool? okBtnHit = fileDialog.ShowDialog();
            if (okBtnHit == true)
            {
                JsonFilePath = fileDialog.FileName;
                textBlockApartmentFName.Text = System.IO.Path.GetFileName(JsonFilePath);
                LoadApartmentInfo(JsonFilePath);
                ActivateButtons();
            }
            else
            {
                // User didnt pick anything
            }

        }

        private void btnLoadAccountStatement_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog fileDialog = new OpenFileDialog();
            fileDialog.Filter = "csv files (*.csv)|*.csv|All files (*.*)|*.*";
            bool? okBtnHit = fileDialog.ShowDialog();
            if (okBtnHit == true)
            {
                CsvFilePath = fileDialog.FileName;
                textBlockAccountFName.Text = System.IO.Path.GetFileName(CsvFilePath);
                ActivateButtons();
            }
            else
            {
                // User didnt pick anything
            }
        }

        private void btnSaveApartmentInfo_Click(object sender, RoutedEventArgs e)
        {
            // Create and configure SaveFileDialog
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "JSON files (*.json)|*.json|All files (*.*)|*.*";
            saveFileDialog.DefaultExt = ".json";
            saveFileDialog.Title = "Save JSON File";

            // Show the dialog and get the chosen file path
            bool? result = saveFileDialog.ShowDialog();

            if (result == true)
            {
                // Get the selected file path
                string jsonFilePath = saveFileDialog.FileName;

                // Serialize the People list to JSON
                string jsonData = JsonConvert.SerializeObject(ApartmentInfos, Formatting.Indented);

                // Write the JSON data to the selected file path
                File.WriteAllText(jsonFilePath, jsonData);

                // Optionally, inform the user that the file was saved successfully
                MessageBox.Show("File saved successfully!", "Save JSON", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }

        private void btnBuildOverview_Click(object sender, RoutedEventArgs e)
        {
            // Create and configure SaveFileDialog
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "CSV files (*.csv)|*.csv|All files (*.*)|*.*";
            saveFileDialog.DefaultExt = ".csv";
            saveFileDialog.Title = "Save csv File";

            // Show the dialog and get the chosen file path
            bool? result = saveFileDialog.ShowDialog();

            if (result == true)
            {
                // Get the selected file path
                string csvFilePath = saveFileDialog.FileName;

                // TODO: Call python script
                // TODO: Deserialize ApartmentInfos, so the python file can read it

                // Optionally, inform the user that the file was saved successfully
                MessageBox.Show("File saved successfully!", "Save JSON", MessageBoxButton.OK, MessageBoxImage.Information);
            }
        }

        private void datagridApartmentInfo_AddingNewItem(object sender, AddingNewItemEventArgs e)
        {
            if (datagridApartmentInfo.Items.Count > 0)
            {
                btnSaveApartmentInfo.IsEnabled = true;
            }
            else
            {
                btnSaveApartmentInfo.IsEnabled = false;
            }
        }
    }
}
