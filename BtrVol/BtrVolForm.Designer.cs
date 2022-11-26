namespace BtrVol
{
    partial class BtrVolForm
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(BtrVolForm));
            this.labelNumericUpDownStart = new System.Windows.Forms.Label();
            this.labelNumericUpDownEnd = new System.Windows.Forms.Label();
            this.labelNumericUpDownDuration = new System.Windows.Forms.Label();
            this.numericUpDownDuration = new System.Windows.Forms.NumericUpDown();
            this.trackBarStart = new System.Windows.Forms.TrackBar();
            this.trackBarEnd = new System.Windows.Forms.TrackBar();
            this.labelValueStart = new System.Windows.Forms.Label();
            this.labelValueEnd = new System.Windows.Forms.Label();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.toolStripStatusLabel1 = new System.Windows.Forms.ToolStripStatusLabel();
            this.toolStripStatusLabel2 = new System.Windows.Forms.ToolStripStatusLabel();
            this.button1 = new System.Windows.Forms.Button();
            this.progressBar1 = new System.Windows.Forms.ProgressBar();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.radioButton3 = new System.Windows.Forms.RadioButton();
            this.radioButton2 = new System.Windows.Forms.RadioButton();
            this.radioButton1 = new System.Windows.Forms.RadioButton();
            this.radioButton4 = new System.Windows.Forms.RadioButton();
            this.plotView = new OxyPlot.WindowsForms.PlotView();
            this.flowLayoutPanel1 = new System.Windows.Forms.FlowLayoutPanel();
            this.labelInterval = new System.Windows.Forms.Label();
            this.labelValueInterval = new System.Windows.Forms.Label();
            this.trackBarInterval = new System.Windows.Forms.TrackBar();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownDuration)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackBarStart)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackBarEnd)).BeginInit();
            this.statusStrip1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.trackBarInterval)).BeginInit();
            this.SuspendLayout();
            // 
            // labelNumericUpDownStart
            // 
            this.labelNumericUpDownStart.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelNumericUpDownStart.AutoSize = true;
            this.labelNumericUpDownStart.Location = new System.Drawing.Point(12, 211);
            this.labelNumericUpDownStart.Name = "labelNumericUpDownStart";
            this.labelNumericUpDownStart.Size = new System.Drawing.Size(43, 20);
            this.labelNumericUpDownStart.TabIndex = 1;
            this.labelNumericUpDownStart.Text = "Start:";
            // 
            // labelNumericUpDownEnd
            // 
            this.labelNumericUpDownEnd.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelNumericUpDownEnd.AutoSize = true;
            this.labelNumericUpDownEnd.Location = new System.Drawing.Point(12, 244);
            this.labelNumericUpDownEnd.Name = "labelNumericUpDownEnd";
            this.labelNumericUpDownEnd.Size = new System.Drawing.Size(37, 20);
            this.labelNumericUpDownEnd.TabIndex = 3;
            this.labelNumericUpDownEnd.Text = "End:";
            // 
            // labelNumericUpDownDuration
            // 
            this.labelNumericUpDownDuration.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelNumericUpDownDuration.AutoSize = true;
            this.labelNumericUpDownDuration.Location = new System.Drawing.Point(12, 279);
            this.labelNumericUpDownDuration.Name = "labelNumericUpDownDuration";
            this.labelNumericUpDownDuration.Size = new System.Drawing.Size(70, 20);
            this.labelNumericUpDownDuration.TabIndex = 5;
            this.labelNumericUpDownDuration.Text = "Duration:";
            // 
            // numericUpDownDuration
            // 
            this.numericUpDownDuration.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.numericUpDownDuration.Location = new System.Drawing.Point(118, 277);
            this.numericUpDownDuration.Maximum = new decimal(new int[] {
            36000,
            0,
            0,
            0});
            this.numericUpDownDuration.Name = "numericUpDownDuration";
            this.numericUpDownDuration.Size = new System.Drawing.Size(200, 27);
            this.numericUpDownDuration.TabIndex = 6;
            this.numericUpDownDuration.Value = new decimal(new int[] {
            10,
            0,
            0,
            0});
            this.numericUpDownDuration.ValueChanged += new System.EventHandler(this.numericUpDownDuration_ValueChanged);
            // 
            // trackBarStart
            // 
            this.trackBarStart.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.trackBarStart.AutoSize = false;
            this.trackBarStart.Location = new System.Drawing.Point(110, 211);
            this.trackBarStart.Maximum = 100;
            this.trackBarStart.Name = "trackBarStart";
            this.trackBarStart.Size = new System.Drawing.Size(208, 27);
            this.trackBarStart.TabIndex = 2;
            this.trackBarStart.Scroll += new System.EventHandler(this.trackBarStart_Scroll);
            // 
            // trackBarEnd
            // 
            this.trackBarEnd.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.trackBarEnd.AutoSize = false;
            this.trackBarEnd.Location = new System.Drawing.Point(110, 244);
            this.trackBarEnd.Maximum = 100;
            this.trackBarEnd.Name = "trackBarEnd";
            this.trackBarEnd.Size = new System.Drawing.Size(208, 27);
            this.trackBarEnd.TabIndex = 4;
            this.trackBarEnd.Scroll += new System.EventHandler(this.trackBarEnd_Scroll);
            // 
            // labelValueStart
            // 
            this.labelValueStart.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelValueStart.AutoSize = true;
            this.labelValueStart.Location = new System.Drawing.Point(74, 211);
            this.labelValueStart.Name = "labelValueStart";
            this.labelValueStart.Size = new System.Drawing.Size(33, 20);
            this.labelValueStart.TabIndex = 12;
            this.labelValueStart.Text = "100";
            this.labelValueStart.TextAlign = System.Drawing.ContentAlignment.TopRight;
            // 
            // labelValueEnd
            // 
            this.labelValueEnd.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelValueEnd.AutoSize = true;
            this.labelValueEnd.Location = new System.Drawing.Point(74, 244);
            this.labelValueEnd.Name = "labelValueEnd";
            this.labelValueEnd.Size = new System.Drawing.Size(33, 20);
            this.labelValueEnd.TabIndex = 13;
            this.labelValueEnd.Text = "100";
            this.labelValueEnd.TextAlign = System.Drawing.ContentAlignment.TopRight;
            // 
            // statusStrip1
            // 
            this.statusStrip1.ImageScalingSize = new System.Drawing.Size(20, 20);
            this.statusStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripStatusLabel1,
            this.toolStripStatusLabel2});
            this.statusStrip1.LayoutStyle = System.Windows.Forms.ToolStripLayoutStyle.HorizontalStackWithOverflow;
            this.statusStrip1.Location = new System.Drawing.Point(0, 376);
            this.statusStrip1.Name = "statusStrip1";
            this.statusStrip1.Size = new System.Drawing.Size(444, 26);
            this.statusStrip1.TabIndex = 14;
            this.statusStrip1.Text = "statusStrip1";
            // 
            // toolStripStatusLabel1
            // 
            this.toolStripStatusLabel1.Name = "toolStripStatusLabel1";
            this.toolStripStatusLabel1.Size = new System.Drawing.Size(49, 20);
            this.toolStripStatusLabel1.Text = "Status";
            // 
            // toolStripStatusLabel2
            // 
            this.toolStripStatusLabel2.Alignment = System.Windows.Forms.ToolStripItemAlignment.Right;
            this.toolStripStatusLabel2.IsLink = true;
            this.toolStripStatusLabel2.Name = "toolStripStatusLabel2";
            this.toolStripStatusLabel2.Size = new System.Drawing.Size(41, 20);
            this.toolStripStatusLabel2.Text = "Help";
            this.toolStripStatusLabel2.Click += new System.EventHandler(this.toolStripStatusLabel2_Click);
            // 
            // button1
            // 
            this.button1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.button1.Location = new System.Drawing.Point(12, 344);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(70, 29);
            this.button1.TabIndex = 15;
            this.button1.Text = "Start";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // progressBar1
            // 
            this.progressBar1.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.progressBar1.Location = new System.Drawing.Point(88, 343);
            this.progressBar1.Name = "progressBar1";
            this.progressBar1.Size = new System.Drawing.Size(344, 29);
            this.progressBar1.TabIndex = 16;
            // 
            // timer1
            // 
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // radioButton3
            // 
            this.radioButton3.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.radioButton3.AutoSize = true;
            this.radioButton3.Location = new System.Drawing.Point(324, 283);
            this.radioButton3.Name = "radioButton3";
            this.radioButton3.Size = new System.Drawing.Size(108, 24);
            this.radioButton3.TabIndex = 10;
            this.radioButton3.TabStop = true;
            this.radioButton3.Text = "Half-Cosine";
            this.radioButton3.UseVisualStyleBackColor = true;
            this.radioButton3.CheckedChanged += new System.EventHandler(this.radioButton3_CheckedChanged);
            // 
            // radioButton2
            // 
            this.radioButton2.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.radioButton2.AutoSize = true;
            this.radioButton2.Location = new System.Drawing.Point(324, 253);
            this.radioButton2.Name = "radioButton2";
            this.radioButton2.Size = new System.Drawing.Size(74, 24);
            this.radioButton2.TabIndex = 9;
            this.radioButton2.TabStop = true;
            this.radioButton2.Text = "Cosine";
            this.radioButton2.UseVisualStyleBackColor = true;
            this.radioButton2.CheckedChanged += new System.EventHandler(this.radioButton2_CheckedChanged);
            // 
            // radioButton1
            // 
            this.radioButton1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.radioButton1.AutoSize = true;
            this.radioButton1.Checked = true;
            this.radioButton1.Location = new System.Drawing.Point(324, 223);
            this.radioButton1.Name = "radioButton1";
            this.radioButton1.Size = new System.Drawing.Size(70, 24);
            this.radioButton1.TabIndex = 8;
            this.radioButton1.TabStop = true;
            this.radioButton1.Text = "Linear";
            this.radioButton1.UseVisualStyleBackColor = true;
            this.radioButton1.CheckedChanged += new System.EventHandler(this.radioButton1_CheckedChanged);
            // 
            // radioButton4
            // 
            this.radioButton4.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.radioButton4.AutoSize = true;
            this.radioButton4.Location = new System.Drawing.Point(324, 313);
            this.radioButton4.Name = "radioButton4";
            this.radioButton4.Size = new System.Drawing.Size(92, 24);
            this.radioButton4.TabIndex = 11;
            this.radioButton4.TabStop = true;
            this.radioButton4.Text = "Half-Sine";
            this.radioButton4.UseVisualStyleBackColor = true;
            this.radioButton4.CheckedChanged += new System.EventHandler(this.radioButton4_CheckedChanged);
            // 
            // plotView
            // 
            this.plotView.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.plotView.Location = new System.Drawing.Point(0, 0);
            this.plotView.Name = "plotView";
            this.plotView.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.plotView.Size = new System.Drawing.Size(444, 205);
            this.plotView.TabIndex = 0;
            this.plotView.Text = "plotView2";
            this.plotView.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.plotView.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.plotView.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // flowLayoutPanel1
            // 
            this.flowLayoutPanel1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.flowLayoutPanel1.AutoSize = true;
            this.flowLayoutPanel1.AutoSizeMode = System.Windows.Forms.AutoSizeMode.GrowAndShrink;
            this.flowLayoutPanel1.FlowDirection = System.Windows.Forms.FlowDirection.TopDown;
            this.flowLayoutPanel1.Location = new System.Drawing.Point(432, 337);
            this.flowLayoutPanel1.Name = "flowLayoutPanel1";
            this.flowLayoutPanel1.Size = new System.Drawing.Size(0, 0);
            this.flowLayoutPanel1.TabIndex = 17;
            // 
            // labelInterval
            // 
            this.labelInterval.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelInterval.AutoSize = true;
            this.labelInterval.Location = new System.Drawing.Point(12, 310);
            this.labelInterval.Name = "labelInterval";
            this.labelInterval.Size = new System.Drawing.Size(61, 20);
            this.labelInterval.TabIndex = 5;
            this.labelInterval.Text = "Interval:";
            // 
            // labelValueInterval
            // 
            this.labelValueInterval.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelValueInterval.AutoSize = true;
            this.labelValueInterval.Location = new System.Drawing.Point(79, 310);
            this.labelValueInterval.Name = "labelValueInterval";
            this.labelValueInterval.Size = new System.Drawing.Size(28, 20);
            this.labelValueInterval.TabIndex = 19;
            this.labelValueInterval.Text = "9.9";
            this.labelValueInterval.TextAlign = System.Drawing.ContentAlignment.TopRight;
            // 
            // trackBarInterval
            // 
            this.trackBarInterval.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.trackBarInterval.AutoSize = false;
            this.trackBarInterval.Location = new System.Drawing.Point(110, 310);
            this.trackBarInterval.Maximum = 10000;
            this.trackBarInterval.Minimum = 100;
            this.trackBarInterval.Name = "trackBarInterval";
            this.trackBarInterval.Size = new System.Drawing.Size(208, 27);
            this.trackBarInterval.SmallChange = 100;
            this.trackBarInterval.TabIndex = 18;
            this.trackBarInterval.Value = 100;
            this.trackBarInterval.Scroll += new System.EventHandler(this.trackBarInterval_Scroll);
            // 
            // BtrVolForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(444, 402);
            this.Controls.Add(this.labelValueInterval);
            this.Controls.Add(this.trackBarInterval);
            this.Controls.Add(this.radioButton4);
            this.Controls.Add(this.radioButton2);
            this.Controls.Add(this.radioButton3);
            this.Controls.Add(this.radioButton1);
            this.Controls.Add(this.flowLayoutPanel1);
            this.Controls.Add(this.progressBar1);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.statusStrip1);
            this.Controls.Add(this.labelValueEnd);
            this.Controls.Add(this.labelValueStart);
            this.Controls.Add(this.trackBarEnd);
            this.Controls.Add(this.trackBarStart);
            this.Controls.Add(this.labelInterval);
            this.Controls.Add(this.labelNumericUpDownDuration);
            this.Controls.Add(this.numericUpDownDuration);
            this.Controls.Add(this.labelNumericUpDownEnd);
            this.Controls.Add(this.labelNumericUpDownStart);
            this.Controls.Add(this.plotView);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "BtrVolForm";
            this.Text = "BtrVol";
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownDuration)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackBarStart)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackBarEnd)).EndInit();
            this.statusStrip1.ResumeLayout(false);
            this.statusStrip1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.trackBarInterval)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private Label labelNumericUpDownStart;
        private Label labelNumericUpDownEnd;
        private Label labelNumericUpDownDuration;
        private NumericUpDown numericUpDownDuration;
        private TrackBar trackBarStart;
        private TrackBar trackBarEnd;
        private Label labelValueStart;
        private Label labelValueEnd;
        private StatusStrip statusStrip1;
        private Button button1;
        private ProgressBar progressBar1;
        private ToolStripStatusLabel toolStripStatusLabel1;
        private System.Windows.Forms.Timer timer1;
        private RadioButton radioButton3;
        private RadioButton radioButton2;
        private RadioButton radioButton1;
        private RadioButton radioButton4;
        private OxyPlot.WindowsForms.PlotView plotView;
        private FlowLayoutPanel flowLayoutPanel1;
        private Label labelInterval;
        private Label labelValueInterval;
        private TrackBar trackBarInterval;
        private ToolStripStatusLabel toolStripStatusLabel2;
    }
}