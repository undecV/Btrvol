using OxyPlot.Series;
using OxyPlot;
using OxyPlot.Axes;
using AudioSwitcher.AudioApi.CoreAudio;
using System.Diagnostics;
using Microsoft.WindowsAPICodePack.Taskbar;
using System.Text.Json;

namespace BtrVol
{
    public partial class BtrVolForm : Form
    {
        CoreAudioDevice defaultPlaybackDevice = new CoreAudioController().DefaultPlaybackDevice;

        private string homepage = "https://github.com/undecV/BtrVol";

        public enum VolCtrlMethod { Linear, Cosine, HalfCosine, HalfSine }

        public class BtrVolConfig
        {
            public double Start { get; set; }  // 0 to 1
            public double End { get; set; }  // 0 to 1
            public long Duration { get; set; }  // second.
            public int Interval { get; set; }  // ms.
            public VolCtrlMethod VolCtrlMethod { get; set; }
        }

        public BtrVolConfig DeepCopyBtrVolConfig(BtrVolConfig originalConfig)
        {
            var newConfig = new BtrVolConfig
            {
                Start = originalConfig.Start,
                End = originalConfig.End,
                Duration = originalConfig.Duration,
                Interval = originalConfig.Interval,
                VolCtrlMethod = originalConfig.VolCtrlMethod
            };
            return newConfig;
        }

        private BtrVolConfig defaultConfig = new BtrVolConfig
        {
            Start = 0.2,
            End = 0.6,
            Duration = 10,
            Interval = 100,
            VolCtrlMethod = VolCtrlMethod.Linear,
        };

        private string configFilePath = Path.Combine(
            AppDomain.CurrentDomain.BaseDirectory,
            "BtrVol.config.json"
            );
        private BtrVolConfig currentConfig;

        private BtrVolConfig LoadConfig(BtrVolConfig defaultConfig)
        {
            var config = DeepCopyBtrVolConfig(defaultConfig);
            bool doSaveConfig = false;
            if (File.Exists(configFilePath))
            {
                try
                {
                    var text = File.ReadAllText(configFilePath);
                    config = JsonSerializer.Deserialize<BtrVolConfig>(text)!;
                }
                catch (Exception)
                {
                    // Debug.WriteLine("Failed to read config file.");
                    doSaveConfig = true;
                }
            }
            else { doSaveConfig = true; }
            if (doSaveConfig) { saveConfig(config, configFilePath); }

            // Debug.WriteLine("Config loaded: " + JsonSerializer.Serialize(config));
            return config;
        }

        private void saveConfig(BtrVolConfig config, string dstPath)
        {
            string jsonString = JsonSerializer.Serialize(config);
            File.WriteAllText(dstPath, jsonString);
        }

        private void applyConfig(BtrVolConfig config)
        {
            trackBarStart.Value = (int)(config.Start * 100.0);
            trackBarEnd.Value = (int)(config.End * 100.0);
            trackBarInterval.Value = config.Interval;
            numericUpDownDuration.Value = config.Duration;
            labelValueStart.Text = trackBarStart.Value.ToString();
            labelValueEnd.Text = trackBarEnd.Value.ToString();
            labelValueInterval.Text = (config.Interval / 1000.0).ToString("0.0");
            progressBar1.Value = 0;
        }

        public BtrVolForm()
        {
            InitializeComponent();

            currentConfig = LoadConfig(defaultConfig);
            applyConfig(currentConfig);

            UpdateGraph();
            statVolume();
        }

        private double volumeContrlFormula(VolCtrlMethod volumeContrlMethodSelector, double time, double start, double end, double duration)
        {
            double x = time;
            double s = start;
            double d = end;
            double t = duration;
            double PI = Math.PI;

            switch (volumeContrlMethodSelector)
            {
                case VolCtrlMethod.Linear:
                    return (x * (d - s) / t) + s;
                case VolCtrlMethod.Cosine:
                    return Math.Cos(x * PI / t) * ((s - d) / 2.0) + ((s + d) / 2.0);
                case VolCtrlMethod.HalfCosine:
                    return Math.Cos((x * PI) / (2.0 * t)) * (s - d) + d;
                case VolCtrlMethod.HalfSine:
                    return Math.Sin((x * PI) / (2.0 * t)) * (d - s) + s;
                default:
                    return 0.0;
            }
        }

        private int simpleVolumeContrlFormula(VolCtrlMethod volumeContrlMethodSelector, double time, double start, double end, double duration)
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
            var start = currentConfig.Start;
            var end = currentConfig.End;
            var duration = currentConfig.Duration;

            Func<double, double> VCFormulaLinear = (x) => volumeContrlFormula(VolCtrlMethod.Linear, x, start, end, duration) * 100.0;
            Func<double, double> VCFormulaCosine = (x) => volumeContrlFormula(VolCtrlMethod.Cosine, x, start, end, duration) * 100.0;
            Func<double, double> VCFormulaHalfCosine = (x) => volumeContrlFormula(VolCtrlMethod.HalfCosine, x, start, end, duration) * 100.0;
            Func<double, double> VCFormulaHalfSine = (x) => volumeContrlFormula(VolCtrlMethod.HalfSine, x, start, end, duration) * 100.0;

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
            this.toolStripStatusLabel1.Text = "Current Method: " + currentConfig.VolCtrlMethod.ToString();
        }

        private enum btrVolStatus { idle, working }
        private btrVolStatus btrVolCurrentStatus = btrVolStatus.idle;

        private void button1_Click(object sender, EventArgs e)
        {
            switch (btrVolCurrentStatus)
            {
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
            this.toolStripStatusLabel1.Text = $"Current volume: {defaultPlaybackDevice.Volume}";
        }

        private void setBtrVolIdle()
        {
            btrVolCurrentStatus = btrVolStatus.idle;
            this.button1.Text = "Start";
            widgetEnabled(true);
            this.toolStripStatusLabel1.Text = $"{this.toolStripStatusLabel1.Text}, stoped.";
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
            setVolume((int)currentConfig.Start * 100);
            this.toolStripStatusLabel1.Text = $"{this.toolStripStatusLabel1.Text}, start.";
            timer1.Interval = currentConfig.Interval;
            timer1.Start();
        }

        long currentTimer = 0;
        private void timer1_Tick(object sender, EventArgs e)
        {
            if (currentTimer >= (currentConfig.Duration * 1000))
            {
                setVolume((int)(currentConfig.End * 100));
                setProgress(100);
                setBtrVolIdle();
                return;
            }
            int vol = simpleVolumeContrlFormula(currentConfig.VolCtrlMethod, currentTimer, currentConfig.Start, currentConfig.End, currentConfig.Duration * 1000);
            setVolume(vol);
            int progressPercentage = (int)(currentTimer / (currentConfig.Duration * 10));
            setProgress(progressPercentage);
            currentTimer += currentConfig.Interval;
        }

        /*
         * Value Changed Callback
         */

        private void numericUpDownDuration_ValueChanged(object sender, EventArgs e)
        {
            currentConfig.Duration = (long)this.numericUpDownDuration.Value;
            UpdateGraph();
        }

        private void trackBarStart_Scroll(object sender, EventArgs e)
        {
            currentConfig.Start = (double)this.trackBarStart.Value / 100.0;
            this.labelValueStart.Text = this.trackBarStart.Value.ToString();
            UpdateGraph();
        }

        private void trackBarEnd_Scroll(object sender, EventArgs e)
        {
            currentConfig.End = (double)this.trackBarEnd.Value / 100.0;
            this.labelValueEnd.Text = this.trackBarEnd.Value.ToString();
            UpdateGraph();
        }
        private void trackBarInterval_Scroll(object sender, EventArgs e)
        {
            currentConfig.Interval = this.trackBarInterval.Value;
            this.labelValueInterval.Text = (currentConfig.Interval / 1000.0).ToString("0.0");
            UpdateGraph();
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            currentConfig.VolCtrlMethod = VolCtrlMethod.Linear;
            statMethod();
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            currentConfig.VolCtrlMethod = VolCtrlMethod.Cosine;
            statMethod();
        }

        private void radioButton3_CheckedChanged(object sender, EventArgs e)
        {
            currentConfig.VolCtrlMethod = VolCtrlMethod.HalfCosine;
            statMethod();
        }

        private void radioButton4_CheckedChanged(object sender, EventArgs e)
        {
            currentConfig.VolCtrlMethod = VolCtrlMethod.HalfSine;
            statMethod();
        }

        private void toolStripStatusLabel2_Click(object sender, EventArgs e)
        {
            Process.Start(new ProcessStartInfo(homepage) { UseShellExecute = true });
        }

        private void button2_Click(object sender, EventArgs e)
        {
            try
            {
                saveConfig(currentConfig, configFilePath);
                toolStripStatusLabel1.Text = "Configuration saved.";
            }
            catch (Exception)
            {
                toolStripStatusLabel1.Text = "Configuration save failed.";
            }
        }
    }
}