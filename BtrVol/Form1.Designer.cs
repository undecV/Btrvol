namespace BtrVol
{
    partial class Form1
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
            this.plotView = new OxyPlot.WindowsForms.PlotView();
            this.labelNumericUpDownS = new System.Windows.Forms.Label();
            this.labelNumericUpDownD = new System.Windows.Forms.Label();
            this.labelNumericUpDownT = new System.Windows.Forms.Label();
            this.numericUpDownT = new System.Windows.Forms.NumericUpDown();
            this.radioButton1 = new System.Windows.Forms.RadioButton();
            this.radioButton2 = new System.Windows.Forms.RadioButton();
            this.radioButton3 = new System.Windows.Forms.RadioButton();
            this.radioButton4 = new System.Windows.Forms.RadioButton();
            this.labelInfo = new System.Windows.Forms.Label();
            this.trackBarS = new System.Windows.Forms.TrackBar();
            this.trackBarD = new System.Windows.Forms.TrackBar();
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownT)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackBarS)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackBarD)).BeginInit();
            this.SuspendLayout();
            // 
            // plotView
            // 
            this.plotView.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.plotView.Location = new System.Drawing.Point(12, 12);
            this.plotView.Name = "plotView";
            this.plotView.PanCursor = System.Windows.Forms.Cursors.Hand;
            this.plotView.Size = new System.Drawing.Size(360, 217);
            this.plotView.TabIndex = 0;
            this.plotView.Text = "plotView2";
            this.plotView.ZoomHorizontalCursor = System.Windows.Forms.Cursors.SizeWE;
            this.plotView.ZoomRectangleCursor = System.Windows.Forms.Cursors.SizeNWSE;
            this.plotView.ZoomVerticalCursor = System.Windows.Forms.Cursors.SizeNS;
            // 
            // labelNumericUpDownS
            // 
            this.labelNumericUpDownS.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelNumericUpDownS.AutoSize = true;
            this.labelNumericUpDownS.Location = new System.Drawing.Point(12, 237);
            this.labelNumericUpDownS.Name = "labelNumericUpDownS";
            this.labelNumericUpDownS.Size = new System.Drawing.Size(43, 20);
            this.labelNumericUpDownS.TabIndex = 1;
            this.labelNumericUpDownS.Text = "Start:";
            // 
            // labelNumericUpDownD
            // 
            this.labelNumericUpDownD.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelNumericUpDownD.AutoSize = true;
            this.labelNumericUpDownD.Location = new System.Drawing.Point(12, 267);
            this.labelNumericUpDownD.Name = "labelNumericUpDownD";
            this.labelNumericUpDownD.Size = new System.Drawing.Size(37, 20);
            this.labelNumericUpDownD.TabIndex = 3;
            this.labelNumericUpDownD.Text = "End:";
            // 
            // labelNumericUpDownT
            // 
            this.labelNumericUpDownT.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.labelNumericUpDownT.AutoSize = true;
            this.labelNumericUpDownT.Location = new System.Drawing.Point(12, 303);
            this.labelNumericUpDownT.Name = "labelNumericUpDownT";
            this.labelNumericUpDownT.Size = new System.Drawing.Size(70, 20);
            this.labelNumericUpDownT.TabIndex = 5;
            this.labelNumericUpDownT.Text = "Duration:";
            // 
            // numericUpDownT
            // 
            this.numericUpDownT.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.numericUpDownT.Location = new System.Drawing.Point(88, 301);
            this.numericUpDownT.Maximum = new decimal(new int[] {
            36000,
            0,
            0,
            0});
            this.numericUpDownT.Name = "numericUpDownT";
            this.numericUpDownT.Size = new System.Drawing.Size(170, 27);
            this.numericUpDownT.TabIndex = 6;
            this.numericUpDownT.Value = new decimal(new int[] {
            10,
            0,
            0,
            0});
            this.numericUpDownT.ValueChanged += new System.EventHandler(this.numericUpDownT_ValueChanged);
            // 
            // radioButton1
            // 
            this.radioButton1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.radioButton1.AutoSize = true;
            this.radioButton1.Checked = true;
            this.radioButton1.Location = new System.Drawing.Point(264, 235);
            this.radioButton1.Name = "radioButton1";
            this.radioButton1.Size = new System.Drawing.Size(70, 24);
            this.radioButton1.TabIndex = 8;
            this.radioButton1.TabStop = true;
            this.radioButton1.Text = "Linear";
            this.radioButton1.UseVisualStyleBackColor = true;
            // 
            // radioButton2
            // 
            this.radioButton2.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.radioButton2.AutoSize = true;
            this.radioButton2.Location = new System.Drawing.Point(264, 265);
            this.radioButton2.Name = "radioButton2";
            this.radioButton2.Size = new System.Drawing.Size(74, 24);
            this.radioButton2.TabIndex = 9;
            this.radioButton2.TabStop = true;
            this.radioButton2.Text = "Cosine";
            this.radioButton2.UseVisualStyleBackColor = true;
            // 
            // radioButton3
            // 
            this.radioButton3.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.radioButton3.AutoSize = true;
            this.radioButton3.Location = new System.Drawing.Point(264, 295);
            this.radioButton3.Name = "radioButton3";
            this.radioButton3.Size = new System.Drawing.Size(108, 24);
            this.radioButton3.TabIndex = 10;
            this.radioButton3.TabStop = true;
            this.radioButton3.Text = "Half-Cosine";
            this.radioButton3.UseVisualStyleBackColor = true;
            // 
            // radioButton4
            // 
            this.radioButton4.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.radioButton4.AutoSize = true;
            this.radioButton4.Location = new System.Drawing.Point(264, 325);
            this.radioButton4.Name = "radioButton4";
            this.radioButton4.Size = new System.Drawing.Size(92, 24);
            this.radioButton4.TabIndex = 11;
            this.radioButton4.TabStop = true;
            this.radioButton4.Text = "Half-Sine";
            this.radioButton4.UseVisualStyleBackColor = true;
            // 
            // labelInfo
            // 
            this.labelInfo.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.labelInfo.AutoSize = true;
            this.labelInfo.Location = new System.Drawing.Point(12, 341);
            this.labelInfo.Name = "labelInfo";
            this.labelInfo.Size = new System.Drawing.Size(35, 20);
            this.labelInfo.TabIndex = 7;
            this.labelInfo.Text = "Info";
            // 
            // trackBarS
            // 
            this.trackBarS.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.trackBarS.AutoSize = false;
            this.trackBarS.Location = new System.Drawing.Point(88, 235);
            this.trackBarS.Maximum = 100;
            this.trackBarS.Name = "trackBarS";
            this.trackBarS.Size = new System.Drawing.Size(170, 27);
            this.trackBarS.TabIndex = 2;
            this.trackBarS.Scroll += new System.EventHandler(this.trackBarS_Scroll);
            // 
            // trackBarD
            // 
            this.trackBarD.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.trackBarD.AutoSize = false;
            this.trackBarD.Location = new System.Drawing.Point(88, 268);
            this.trackBarD.Maximum = 100;
            this.trackBarD.Name = "trackBarD";
            this.trackBarD.Size = new System.Drawing.Size(170, 27);
            this.trackBarD.TabIndex = 4;
            this.trackBarD.Scroll += new System.EventHandler(this.trackBarD_Scroll);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(384, 370);
            this.Controls.Add(this.trackBarD);
            this.Controls.Add(this.trackBarS);
            this.Controls.Add(this.labelInfo);
            this.Controls.Add(this.radioButton4);
            this.Controls.Add(this.radioButton3);
            this.Controls.Add(this.radioButton2);
            this.Controls.Add(this.radioButton1);
            this.Controls.Add(this.labelNumericUpDownT);
            this.Controls.Add(this.numericUpDownT);
            this.Controls.Add(this.labelNumericUpDownD);
            this.Controls.Add(this.labelNumericUpDownS);
            this.Controls.Add(this.plotView);
            this.Name = "Form1";
            this.Text = "Form1";
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDownT)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackBarS)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.trackBarD)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private OxyPlot.WindowsForms.PlotView plotView1;
        private OxyPlot.WindowsForms.PlotView plotView;
        private Label labelNumericUpDownS;
        private Label labelNumericUpDownD;
        private Label labelNumericUpDownT;
        private NumericUpDown numericUpDownT;
        private RadioButton radioButton1;
        private RadioButton radioButton2;
        private RadioButton radioButton3;
        private RadioButton radioButton4;
        private Label labelInfo;
        private TrackBar trackBarS;
        private TrackBar trackBarD;
    }
}