using OxyPlot.Series;
using OxyPlot;
using OxyPlot.Axes;
using AudioSwitcher.AudioApi.CoreAudio;
using System.Diagnostics;
using Microsoft.WindowsAPICodePack.Taskbar;

namespace BtrVol
{

    public partial class BtrVolForm : Form
    {
        CoreAudioDevice defaultPlaybackDevice = new CoreAudioController().DefaultPlaybackDevice;

        private string homepage = "https://github.com/undecV/BtrVol";

        // double volume = 0;
        private double start = 0.2;
        private double end = 0.8;
        private long duration = 10;
        private int interval = 100;

        public BtrVolForm()
        {
            InitializeComponent();

            this.trackBarStart.Value = (int)(start * 100.0);
            this.trackBarEnd.Value = (int)(end * 100.0);
            this.trackBarInterval.Value = interval;
            this.numericUpDownDuration.Value = duration;
            this.labelValueStart.Text = this.trackBarStart.Value.ToString();
            this.labelValueEnd.Text = this.trackBarEnd.Value.ToString();
            this.labelValueInterval.Text = (interval / 1000.0).ToString("0.0");
            progressBar1.Value = 0;

            UpdateGraph();
            statVolume();
        }


        private enum vcMethod { Linear, Cosine, HalfCosine, HalfSine }
        private vcMethod vcMethodSelector = vcMethod.Linear;
        private double volumeContrlFormula(vcMethod volumeContrlMethodSelector, double time, double start, double end, double duration)
        {
            double x = time;
            double s = start;
            double d = end;
            double t = duration;
            double PI = Math.PI;
            
            switch (volumeContrlMethodSelector) {
                case vcMethod.Linear:
                    return (x * (d - s) / t) + s;
                case vcMethod.Cosine:
                    return Math.Cos(x * PI / t) * ((s - d) / 2.0) + ((s + d) / 2.0);
                case vcMethod.HalfCosine:
                    return Math.Cos((x * PI) / (2.0 * t)) * (s - d) + d;
                case vcMethod.HalfSine:
                    return Math.Sin((x * PI) / (2.0 * t)) * (d - s) + s;
                default:
                    return 0.0;
            }
        }

        private int simpleVolumeContrlFormula(vcMethod volumeContrlMethodSelector, double time, double start, double end, double duration)
        {
            double vol = volumeContrlFormula(volumeContrlMethodSelector, time, start, end, duration) * 100.0;

            if (start < end)
            {
                return (int)Math.Floor(vol);
            }
            else if (end < start)
            {
                return (int)Math.Ceiling(vol);
            }
            else
            {
                return (int)Math.Round(vol);
            }
        }

        public void UpdateGraph()
        {
            Func<double, double> VCFormulaLinear = (x) => volumeContrlFormula(vcMethod.Linear, x, start, end, duration) * 100.0;
            Func<double, double> VCFormulaCosine = (x) => volumeContrlFormula(vcMethod.Cosine, x, start, end, duration) * 100.0;
            Func<double, double> VCFormulaHalfCosine = (x) => volumeContrlFormula(vcMethod.HalfCosine, x, start, end, duration) * 100.0;
            Func<double, double> VCFormulaHalfSine = (x) => volumeContrlFormula(vcMethod.HalfSine, x, start, end, duration) * 100.0;

            double graphInterval = 0.01;
            // double intervalSecond = interval / 1000.0;
            // if (intervalSecond >= duration)
            // {
            //     graphInterval = duration;
            // }
            // else
            // {
            //     graphInterval = intervalSecond;
            // }

            var myModel = new PlotModel { Title = "" };
            myModel.Series.Add(new FunctionSeries(VCFormulaLinear, 0, duration, graphInterval, "Linear"));
            myModel.Series.Add(new FunctionSeries(VCFormulaCosine, 0, duration, graphInterval, "Cosine"));
            myModel.Series.Add(new FunctionSeries(VCFormulaHalfCosine, 0, duration, graphInterval, "Half-Cosine"));
            myModel.Series.Add(new FunctionSeries(VCFormulaHalfSine, 0, duration, graphInterval, "Half-Sine"));
            myModel.Axes.Add(new LinearAxis { Position = AxisPosition.Bottom, Minimum = 0, Maximum = duration, Title = "" });
            myModel.Axes.Add(new LinearAxis { Position = AxisPosition.Left, Minimum = 0, Maximum = 100, Title = "" });
            plotView.Model = myModel;
            plotView.Invalidate();
        }

        private void statVolume()
        {
            toolStripStatusLabel1.Text = "Current Volume: " + defaultPlaybackDevice.Volume;
        }

        private void statMethod()
        {
            toolStripStatusLabel1.Text = "Current Method: " + vcMethodSelector.ToString();
        }

        private enum btrVolStatus { idle, working }
        private btrVolStatus btrVolCurrentStatus = btrVolStatus.idle;

        private void button1_Click(object sender, EventArgs e)
        {
            switch (btrVolCurrentStatus) {
                case btrVolStatus.idle:
                    setBtrVolWorking();
                    break;
                case btrVolStatus.working:
                    setBtrVolIdle();
                    break;
            }
            // statBtrVolStatus();
        }

        private void widgetEnabled(bool enabled)
        {
            trackBarStart.Enabled = enabled;
            trackBarEnd.Enabled = enabled;
            numericUpDownDuration.Enabled = enabled;
            trackBarInterval.Enabled = enabled;
            radioButton1.Enabled = enabled;
            radioButton2.Enabled = enabled;
            radioButton3.Enabled = enabled;
            radioButton4.Enabled = enabled;
        }

        private void setProgress(int progressPercentage)
        {
            progressBar1.Value = progressPercentage;
            TaskbarManager.Instance.SetProgressValue(progressPercentage, 100);
        }

        private void setVolume(int simpleVolume)
        {
            defaultPlaybackDevice.Volume = simpleVolume;
            toolStripStatusLabel1.Text = $"Current volume: {defaultPlaybackDevice.Volume}";
        }

        private void setBtrVolIdle()
        {
            btrVolCurrentStatus = btrVolStatus.idle;
            this.button1.Text = "Start";
            widgetEnabled(true);
            toolStripStatusLabel1.Text = $"{toolStripStatusLabel1.Text}, stoped.";
            TaskbarManager.Instance.SetProgressState(TaskbarProgressBarState.NoProgress);
            timer1.Stop();
        }

            private void setBtrVolWorking()
        {
            btrVolCurrentStatus = btrVolStatus.working;
            this.button1.Text = "Stop";
            widgetEnabled(false);
            TaskbarManager.Instance.SetProgressState(TaskbarProgressBarState.Normal);
            setProgress(0);
            currentTimer = 0;
            setVolume((int)(start * 100));
            toolStripStatusLabel1.Text = $"{toolStripStatusLabel1.Text}, start.";
            timer1.Interval = interval;
            timer1.Start();
        }

        long currentTimer = 0;
        private void timer1_Tick(object sender, EventArgs e)
        {
            if (currentTimer >= (duration * 1000))
            {
                setVolume((int)(end * 100));
                setProgress(100);
                setBtrVolIdle();
                return;
            }
            int vol = simpleVolumeContrlFormula(vcMethodSelector, currentTimer, start, end, duration * 1000);
            setVolume(vol);
            int progressPercentage = (int)(currentTimer / (duration * 10));
            setProgress(progressPercentage);
            currentTimer += interval;
        }

        /*
         * Value Changed Callback
         */

        private void numericUpDownDuration_ValueChanged(object sender, EventArgs e)
        {
            duration = (long)this.numericUpDownDuration.Value;
            UpdateGraph();
        }

        private void trackBarStart_Scroll(object sender, EventArgs e)
        {
            start = (double)this.trackBarStart.Value / 100.0;
            this.labelValueStart.Text = this.trackBarStart.Value.ToString();
            UpdateGraph();
        }

        private void trackBarEnd_Scroll(object sender, EventArgs e)
        {
            end = (double)this.trackBarEnd.Value / 100.0;
            this.labelValueEnd.Text = this.trackBarEnd.Value.ToString();
            UpdateGraph();
        }
        private void trackBarInterval_Scroll(object sender, EventArgs e)
        {
            interval = this.trackBarInterval.Value;
            this.labelValueInterval.Text = (interval / 1000.0).ToString("0.0");
            UpdateGraph();
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            vcMethodSelector = vcMethod.Linear;
            statMethod();
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            vcMethodSelector = vcMethod.Cosine;
            statMethod();
        }

        private void radioButton3_CheckedChanged(object sender, EventArgs e)
        {
            vcMethodSelector = vcMethod.HalfCosine;
            statMethod();
        }

        private void radioButton4_CheckedChanged(object sender, EventArgs e)
        {
            vcMethodSelector = vcMethod.HalfSine;
            statMethod();
        }

        private void toolStripStatusLabel2_Click(object sender, EventArgs e)
        {
            Process.Start(new ProcessStartInfo(homepage) { UseShellExecute = true });
        }
    }
}