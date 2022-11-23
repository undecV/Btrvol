using OxyPlot.Series;
using OxyPlot;
using OxyPlot.Axes;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.TaskbarClock;

namespace BtrVol
{

    public partial class Form1 : Form
    {
        // double volume = 0;
        private double start = 0;
        private double end = 0;
        private long duration = 10;

        public double VolumeContrlFormulaLinear(double volume, double start, double end, long duration)
        {
            if (end == start) return 0.0;
            double time = ((volume - start) * (double)duration) / (end - start);
            return time;
        }

        public double VolumeContrlFormulaCosine(double volume, double start, double end, long duration)
        {
            if (end == start) return 0.0;
            double time = ((double)duration / Math.PI) * Math.Acos((2 * volume - start - end) / (start - end));
            return time;
        }

        public double VolumeContrlFormulaHalfCosine(double volume, double start, double end, long duration)
        {
            if (end == start) return 0.0;
            double time = (2 * (double)duration / Math.PI) * Math.Acos((volume - end) / (start - end));
            return time;
        }
        public double VolumeContrlFormulaHalfSine(double volume, double start, double end, long duration)
        {
            if (end == start) return 0.0;
            double time = (2 * (double)duration / Math.PI) * Math.Asin((volume - start) / (end - start));
            return time;
        }
        public void UpdateGraph()
        {
            Func<double, double> VCFormulaLinear = (x) => VolumeContrlFormulaLinear(x, start, end, duration);
            Func<double, double> VCFormulaCosine = (x) => VolumeContrlFormulaCosine(x, start, end, duration);
            Func<double, double> VCFormulaHalfCosine = (x) => VolumeContrlFormulaHalfCosine(x, start, end, duration);
            Func<double, double> VCFormulaHalfSine = (x) => VolumeContrlFormulaHalfSine(x, start, end, duration);
            var myModel = new PlotModel { Title = "" };
            myModel.Series.Add(new FunctionSeries(VCFormulaLinear, Math.Min(start, end), Math.Max(start, end), 0.01, "cos(x)"));
            myModel.Series.Add(new FunctionSeries(VCFormulaCosine, Math.Min(start, end), Math.Max(start, end), 0.01, "cos(x)"));
            myModel.Series.Add(new FunctionSeries(VCFormulaHalfCosine, Math.Min(start, end), Math.Max(start, end), 0.01, "cos(x)"));
            myModel.Series.Add(new FunctionSeries(VCFormulaHalfSine, Math.Min(start, end), Math.Max(start, end), 0.01, "cos(x)"));
            myModel.Axes.Add(new LinearAxis { Position = AxisPosition.Bottom, Minimum = 0, Maximum = 1, Title = "Vol"});
            myModel.Axes.Add(new LinearAxis { Position = AxisPosition.Left, Minimum = 0, Maximum = duration , Title = "Time"});
            labelInfo.Text = $"Start: {VCFormulaLinear(start)}, End: {VCFormulaLinear(end)}";
            plotView.Model = myModel;
            plotView.Invalidate();
        }

        public Form1()
        {
            InitializeComponent();

            UpdateGraph();
        }

        private void numericUpDownT_ValueChanged(object sender, EventArgs e)
        {
            duration = (long)this.numericUpDownT.Value;
            UpdateGraph();
        }

        private void trackBarS_Scroll(object sender, EventArgs e)
        {
            start = (double)this.trackBarS.Value / 100.0;
            UpdateGraph();
        }

        private void trackBarD_Scroll(object sender, EventArgs e)
        {
            end = (double)this.trackBarD.Value / 100.0;
            UpdateGraph();
        }
    }
}