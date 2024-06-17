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

namespace BogensegadeUI
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            
        }

        private void btnBoligydelse_Click(object sender, RoutedEventArgs e)
        {
            gridContent.Children.Clear();
            BogensegadeUI.View.Boligydelse usercontrol = new View.Boligydelse();
            gridContent.Children.Add(usercontrol);
        }

        private void btnVenteliste_Click(object sender, RoutedEventArgs e)
        {
            gridContent.Children.Clear();
            BogensegadeUI.View.Venteliste usercontrol = new View.Venteliste();
            gridContent.Children.Add(usercontrol);
        }

        private void btnBudget_Click(object sender, RoutedEventArgs e)
        {
            gridContent.Children.Clear();
            BogensegadeUI.View.Budget usercontrol = new View.Budget();
            gridContent.Children.Add(usercontrol);
        }
    }
}
