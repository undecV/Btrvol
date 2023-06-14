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
            components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(BtrVolForm));
            labelNumericUpDownStart = new Label();
            labelNumericUpDownEnd = new Label();
            labelNumericUpDownDuration = new Label();
            numericUpDownDuration = new NumericUpDown();
            trackBarStart = new TrackBar();
            trackBarEnd = new TrackBar();
            labelValueStart = new Label();
            labelValueEnd = new Label();
            statusStrip1 = new StatusStrip();
            toolStripStatusLabel1 = new ToolStripStatusLabel();
            toolStripStatusLabel2 = new ToolStripStatusLabel();
            button1 = new Button();
            progressBar1 = new ProgressBar();
            timer1 = new System.Windows.Forms.Timer(components);
            radioButton3 = new RadioButton();
            radioButton2 = new RadioButton();
            radioButton1 = new RadioButton();
            radioButton4 = new RadioButton();
            plotView = new OxyPlot.WindowsForms.PlotView();
            flowLayoutPanel1 = new FlowLayoutPanel();
            labelInterval = new Label();
            labelValueInterval = new Label();
            trackBarInterval = new TrackBar();
            button2 = new Button();
            ((System.ComponentModel.ISupportInitialize)numericUpDownDuration).BeginInit();
            ((System.ComponentModel.ISupportInitialize)trackBarStart).BeginInit();
            ((System.ComponentModel.ISupportInitialize)trackBarEnd).BeginInit();
            statusStrip1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)trackBarInterval).BeginInit();
            SuspendLayout();
            // 
            // labelNumericUpDownStart
            // 
            labelNumericUpDownStart.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            labelNumericUpDownStart.AutoSize = true;
            labelNumericUpDownStart.Location = new Point(12, 211);
            labelNumericUpDownStart.Name = "labelNumericUpDownStart";
            labelNumericUpDownStart.Size = new Size(43, 20);
            labelNumericUpDownStart.TabIndex = 1;
            labelNumericUpDownStart.Text = "Start:";
            // 
            // labelNumericUpDownEnd
            // 
            labelNumericUpDownEnd.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            labelNumericUpDownEnd.AutoSize = true;
            labelNumericUpDownEnd.Location = new Point(12, 244);
            labelNumericUpDownEnd.Name = "labelNumericUpDownEnd";
            labelNumericUpDownEnd.Size = new Size(37, 20);
            labelNumericUpDownEnd.TabIndex = 3;
            labelNumericUpDownEnd.Text = "End:";
            // 
            // labelNumericUpDownDuration
            // 
            labelNumericUpDownDuration.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            labelNumericUpDownDuration.AutoSize = true;
            labelNumericUpDownDuration.Location = new Point(12, 279);
            labelNumericUpDownDuration.Name = "labelNumericUpDownDuration";
            labelNumericUpDownDuration.Size = new Size(70, 20);
            labelNumericUpDownDuration.TabIndex = 5;
            labelNumericUpDownDuration.Text = "Duration:";
            // 
            // numericUpDownDuration
            // 
            numericUpDownDuration.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            numericUpDownDuration.Increment = new decimal(new int[] { 60, 0, 0, 0 });
            numericUpDownDuration.Location = new Point(118, 277);
            numericUpDownDuration.Maximum = new decimal(new int[] { 36000, 0, 0, 0 });
            numericUpDownDuration.Name = "numericUpDownDuration";
            numericUpDownDuration.Size = new Size(200, 27);
            numericUpDownDuration.TabIndex = 6;
            numericUpDownDuration.Value = new decimal(new int[] { 10, 0, 0, 0 });
            numericUpDownDuration.ValueChanged += numericUpDownDuration_ValueChanged;
            // 
            // trackBarStart
            // 
            trackBarStart.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            trackBarStart.AutoSize = false;
            trackBarStart.Location = new Point(110, 211);
            trackBarStart.Maximum = 100;
            trackBarStart.Name = "trackBarStart";
            trackBarStart.Size = new Size(208, 27);
            trackBarStart.TabIndex = 2;
            trackBarStart.Scroll += trackBarStart_Scroll;
            // 
            // trackBarEnd
            // 
            trackBarEnd.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            trackBarEnd.AutoSize = false;
            trackBarEnd.Location = new Point(110, 244);
            trackBarEnd.Maximum = 100;
            trackBarEnd.Name = "trackBarEnd";
            trackBarEnd.Size = new Size(208, 27);
            trackBarEnd.TabIndex = 4;
            trackBarEnd.Scroll += trackBarEnd_Scroll;
            // 
            // labelValueStart
            // 
            labelValueStart.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            labelValueStart.AutoSize = true;
            labelValueStart.Location = new Point(74, 211);
            labelValueStart.Name = "labelValueStart";
            labelValueStart.Size = new Size(33, 20);
            labelValueStart.TabIndex = 12;
            labelValueStart.Text = "100";
            labelValueStart.TextAlign = ContentAlignment.TopRight;
            // 
            // labelValueEnd
            // 
            labelValueEnd.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            labelValueEnd.AutoSize = true;
            labelValueEnd.Location = new Point(74, 244);
            labelValueEnd.Name = "labelValueEnd";
            labelValueEnd.Size = new Size(33, 20);
            labelValueEnd.TabIndex = 13;
            labelValueEnd.Text = "100";
            labelValueEnd.TextAlign = ContentAlignment.TopRight;
            // 
            // statusStrip1
            // 
            statusStrip1.ImageScalingSize = new Size(20, 20);
            statusStrip1.Items.AddRange(new ToolStripItem[] { toolStripStatusLabel1, toolStripStatusLabel2 });
            statusStrip1.LayoutStyle = ToolStripLayoutStyle.HorizontalStackWithOverflow;
            statusStrip1.Location = new Point(0, 376);
            statusStrip1.Name = "statusStrip1";
            statusStrip1.Size = new Size(444, 26);
            statusStrip1.TabIndex = 14;
            statusStrip1.Text = "statusStrip1";
            // 
            // toolStripStatusLabel1
            // 
            toolStripStatusLabel1.Name = "toolStripStatusLabel1";
            toolStripStatusLabel1.Size = new Size(49, 20);
            toolStripStatusLabel1.Text = "Status";
            // 
            // toolStripStatusLabel2
            // 
            toolStripStatusLabel2.Alignment = ToolStripItemAlignment.Right;
            toolStripStatusLabel2.IsLink = true;
            toolStripStatusLabel2.Name = "toolStripStatusLabel2";
            toolStripStatusLabel2.Size = new Size(41, 20);
            toolStripStatusLabel2.Text = "Help";
            toolStripStatusLabel2.Click += toolStripStatusLabel2_Click;
            // 
            // button1
            // 
            button1.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            button1.Location = new Point(12, 344);
            button1.Name = "button1";
            button1.Size = new Size(70, 29);
            button1.TabIndex = 15;
            button1.Text = "Start";
            button1.UseVisualStyleBackColor = true;
            button1.Click += button1_Click;
            // 
            // progressBar1
            // 
            progressBar1.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            progressBar1.Location = new Point(88, 343);
            progressBar1.Name = "progressBar1";
            progressBar1.Size = new Size(288, 29);
            progressBar1.TabIndex = 16;
            progressBar1.Value = 50;
            // 
            // timer1
            // 
            timer1.Tick += timer1_Tick;
            // 
            // radioButton3
            // 
            radioButton3.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
            radioButton3.AutoSize = true;
            radioButton3.Location = new Point(324, 283);
            radioButton3.Name = "radioButton3";
            radioButton3.Size = new Size(108, 24);
            radioButton3.TabIndex = 10;
            radioButton3.TabStop = true;
            radioButton3.Text = "Half-Cosine";
            radioButton3.UseVisualStyleBackColor = true;
            radioButton3.CheckedChanged += radioButton3_CheckedChanged;
            // 
            // radioButton2
            // 
            radioButton2.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
            radioButton2.AutoSize = true;
            radioButton2.Location = new Point(324, 253);
            radioButton2.Name = "radioButton2";
            radioButton2.Size = new Size(74, 24);
            radioButton2.TabIndex = 9;
            radioButton2.TabStop = true;
            radioButton2.Text = "Cosine";
            radioButton2.UseVisualStyleBackColor = true;
            radioButton2.CheckedChanged += radioButton2_CheckedChanged;
            // 
            // radioButton1
            // 
            radioButton1.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
            radioButton1.AutoSize = true;
            radioButton1.Checked = true;
            radioButton1.Location = new Point(324, 223);
            radioButton1.Name = "radioButton1";
            radioButton1.Size = new Size(70, 24);
            radioButton1.TabIndex = 8;
            radioButton1.TabStop = true;
            radioButton1.Text = "Linear";
            radioButton1.UseVisualStyleBackColor = true;
            radioButton1.CheckedChanged += radioButton1_CheckedChanged;
            // 
            // radioButton4
            // 
            radioButton4.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
            radioButton4.AutoSize = true;
            radioButton4.Location = new Point(324, 313);
            radioButton4.Name = "radioButton4";
            radioButton4.Size = new Size(92, 24);
            radioButton4.TabIndex = 11;
            radioButton4.TabStop = true;
            radioButton4.Text = "Half-Sine";
            radioButton4.UseVisualStyleBackColor = true;
            radioButton4.CheckedChanged += radioButton4_CheckedChanged;
            // 
            // plotView
            // 
            plotView.Anchor = AnchorStyles.Top | AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            plotView.Location = new Point(0, 0);
            plotView.Name = "plotView";
            plotView.PanCursor = Cursors.Hand;
            plotView.Size = new Size(444, 205);
            plotView.TabIndex = 0;
            plotView.Text = "plotView2";
            plotView.ZoomHorizontalCursor = Cursors.SizeWE;
            plotView.ZoomRectangleCursor = Cursors.SizeNWSE;
            plotView.ZoomVerticalCursor = Cursors.SizeNS;
            // 
            // flowLayoutPanel1
            // 
            flowLayoutPanel1.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
            flowLayoutPanel1.AutoSize = true;
            flowLayoutPanel1.AutoSizeMode = AutoSizeMode.GrowAndShrink;
            flowLayoutPanel1.FlowDirection = FlowDirection.TopDown;
            flowLayoutPanel1.Location = new Point(432, 337);
            flowLayoutPanel1.Name = "flowLayoutPanel1";
            flowLayoutPanel1.Size = new Size(0, 0);
            flowLayoutPanel1.TabIndex = 17;
            // 
            // labelInterval
            // 
            labelInterval.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            labelInterval.AutoSize = true;
            labelInterval.Location = new Point(12, 310);
            labelInterval.Name = "labelInterval";
            labelInterval.Size = new Size(61, 20);
            labelInterval.TabIndex = 5;
            labelInterval.Text = "Interval:";
            // 
            // labelValueInterval
            // 
            labelValueInterval.Anchor = AnchorStyles.Bottom | AnchorStyles.Left;
            labelValueInterval.AutoSize = true;
            labelValueInterval.Location = new Point(79, 310);
            labelValueInterval.Name = "labelValueInterval";
            labelValueInterval.Size = new Size(28, 20);
            labelValueInterval.TabIndex = 19;
            labelValueInterval.Text = "9.9";
            labelValueInterval.TextAlign = ContentAlignment.TopRight;
            // 
            // trackBarInterval
            // 
            trackBarInterval.Anchor = AnchorStyles.Bottom | AnchorStyles.Left | AnchorStyles.Right;
            trackBarInterval.AutoSize = false;
            trackBarInterval.Location = new Point(110, 310);
            trackBarInterval.Maximum = 10000;
            trackBarInterval.Minimum = 100;
            trackBarInterval.Name = "trackBarInterval";
            trackBarInterval.Size = new Size(208, 27);
            trackBarInterval.SmallChange = 100;
            trackBarInterval.TabIndex = 18;
            trackBarInterval.Value = 100;
            trackBarInterval.Scroll += trackBarInterval_Scroll;
            // 
            // button2
            // 
            button2.Anchor = AnchorStyles.Bottom | AnchorStyles.Right;
            button2.Location = new Point(382, 343);
            button2.Name = "button2";
            button2.Size = new Size(50, 29);
            button2.TabIndex = 20;
            button2.Text = "Save";
            button2.UseVisualStyleBackColor = true;
            button2.Click += button2_Click;
            // 
            // BtrVolForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(444, 402);
            Controls.Add(button2);
            Controls.Add(labelValueInterval);
            Controls.Add(trackBarInterval);
            Controls.Add(radioButton4);
            Controls.Add(radioButton2);
            Controls.Add(radioButton3);
            Controls.Add(radioButton1);
            Controls.Add(flowLayoutPanel1);
            Controls.Add(progressBar1);
            Controls.Add(button1);
            Controls.Add(statusStrip1);
            Controls.Add(labelValueEnd);
            Controls.Add(labelValueStart);
            Controls.Add(trackBarEnd);
            Controls.Add(trackBarStart);
            Controls.Add(labelInterval);
            Controls.Add(labelNumericUpDownDuration);
            Controls.Add(numericUpDownDuration);
            Controls.Add(labelNumericUpDownEnd);
            Controls.Add(labelNumericUpDownStart);
            Controls.Add(plotView);
            Icon = (Icon)resources.GetObject("$this.Icon");
            Name = "BtrVolForm";
            Text = "BtrVol";
            ((System.ComponentModel.ISupportInitialize)numericUpDownDuration).EndInit();
            ((System.ComponentModel.ISupportInitialize)trackBarStart).EndInit();
            ((System.ComponentModel.ISupportInitialize)trackBarEnd).EndInit();
            statusStrip1.ResumeLayout(false);
            statusStrip1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)trackBarInterval).EndInit();
            ResumeLayout(false);
            PerformLayout();
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
        private Button button2;
    }
}