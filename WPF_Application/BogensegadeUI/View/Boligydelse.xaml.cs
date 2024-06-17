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
        public string Id { get; set; }
        public int Boligafgift { get; set; }
        public int Faellesudgifter { get; set; }
        public int AcontoVarme { get; set; }
        public int AcontoVand { get; set; }
        public string Kontobeskeder { get; set; }
    }

    /// <summary>
    /// Interaction logic for Boligydelse.xaml
    /// </summary>
    public partial class Boligydelse : UserControl
    {
        private string jsonFilePath = "";
        public List<ApartmentInfo> apartmentInfos { get; set; }

        public Boligydelse()
        {
            InitializeComponent();
        }

        private void LoadApartmentInfo(string path)
        {
            if (!File.Exists(path))
            {
                return;
            }

            string jsonData = File.ReadAllText(path);
            Debug.WriteLine(jsonData);
            apartmentInfos = JsonConvert.DeserializeObject<List<ApartmentInfo>>(jsonData);
            Debug.WriteLine(apartmentInfos);
            datagridApartmentInfo.ItemsSource = apartmentInfos;
        }

        private void btnLoadApartmentInfo_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog fileDialog = new OpenFileDialog();
            fileDialog.Filter = "JSON files (*.txt)|*.json|All files (*.*)|*.*";
            bool? okBtnHit = fileDialog.ShowDialog();
            if (okBtnHit == true)
            {
                jsonFilePath = fileDialog.FileName;
                LoadApartmentInfo(jsonFilePath);
            }
            else
            {
                // User didnt pick anything
            }

        }

        private void btnLoadAccountStatement_Click(object sender, RoutedEventArgs e)
        {

        }
    }
}
