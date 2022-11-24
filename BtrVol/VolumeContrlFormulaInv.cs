using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace BtrVol
{
    internal class VolumeContrlFormulaInv
    {
        public double VolumeContrlFormulaLinearInv(long volume, double start, double end, long duration)
        {
            if (end == start) return 0.0;
            double time = ((volume - start) * (double)duration) / (end - start);
            return time;
        }

        public double VolumeContrlFormulaCosineInv(double volume, double start, double end, long duration)
        {
            if (end == start) return 0.0;
            double time = ((double)duration / Math.PI) * Math.Acos((2 * volume - start - end) / (start - end));
            return time;
        }

        public double VolumeContrlFormulaHalfCosineInv(double volume, double start, double end, long duration)
        {
            if (end == start) return 0.0;
            double time = (2 * (double)duration / Math.PI) * Math.Acos((volume - end) / (start - end));
            return time;
        }
        public double VolumeContrlFormulaHalfSineInv(double volume, double start, double end, long duration)
        {
            if (end == start) return 0.0;
            double time = (2 * (double)duration / Math.PI) * Math.Asin((volume - start) / (end - start));
            return time;
        }
    }
}
