using OxyPlot.Series;
using OxyPlot;

namespace BtrVol
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            var myModel = new PlotModel { Title = "Example 1" };
            myModel.Series.Add(new FunctionSeries(Math.Cos, 0, 10, 0.1, "cos(x)"));
            plotView2.Model = myModel;
        }

    }
}