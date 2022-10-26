using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;

namespace HilbertsCurve_CS
{

    public class HilbertsCurve
    {
        public int iterator; public int dimention;
        private int min_height; private int max_height;
        private int min_x; private int max_x;

        public HilbertsCurve(int iterator, int dimention)
        {
            //Initialize a hilbert curve with:
            //Args:
            //iterator(int): iterations to use in constructing the hilbert curve.
            //   if float, must satisfy p % 1 = 0
            //dimention(int): number of dimensions.
            //    if float must satisfy n % 1 = 0
            //

            if (iterator <= 0 | dimention <= 0)
            {
                throw new ArgumentException($"Error. Number of dimentions and number of iterations need to be positive. Ckeck please values: {iterator} and {dimention}.");
            }

            this.iterator = iterator;
            this.dimention = dimention;
            this.min_height = 0;
            this.max_height = (int)System.Math.Pow(2, this.iterator * this.dimention) - 1;
            this.min_x = 0;
            this.max_x = (int)System.Math.Pow(2, this.iterator) - 1;
        }

        public HilbertsCurve(float iterator, float dimention)
        {
            //Initialize a hilbert curve with:
            //Args:
            //iterator(float): iterations to use in constructing the hilbert curve.
            //   if float, must satisfy p % 1 = 0
            //dimention(float): number of dimensions.
            //    if float must satisfy n % 1 = 0
            //

            if (iterator <= 0 | dimention <= 0)
            {
                throw new ArgumentException($"Error. Number of dimentions and number of iterations need to be positive. Ckeck please values: {iterator} and {dimention}.");
            }

            this.iterator = (int)iterator;
            this.dimention = (int)dimention;
            this.min_height = 0;
            this.max_height = (int)System.Math.Pow(2, this.iterator * this.dimention) - 1;
            this.min_x = 0;
            this.max_x = (int)System.Math.Pow(2, this.iterator) - 1;
        }

        public override string ToString()
        {

            return ($"Hilbert's curve:\nIterations - {this.iterator}, Dimention - {this.dimention}.");
        }

        private static string Slice(string _value, int start)
        {
            int len = _value.Length - start;
            return _value.Substring(start, len);
        }

        private static string Slice(string _value, int start, int end)
        {
            int len = end - start;
            return _value.Substring(start, len);
        }

        private static string Slice(string _value, int start, int end, int step)
        {
            int len = end - start;
            _value = _value.Substring(start, len);
            string str_step = "";
            for (int i = 0; i < _value.Length; i = i + step)
            {
                str_step += _value[i];
            }
            return str_step;
        }

        private static string ToBinary(int number, int padding)
        {
            //Return a binary string representation of `number` zero padded to `padding`
            string binary = Convert.ToString(number, 2).PadLeft(padding, '0');
            return binary;
        }

        private static int FromBinary(string binary_number)
        {
            //Return int from a binary string `binary_number`
            return Convert.ToInt32(binary_number, 2);
        }

        private List<List<int>> Hilbert_integer_to_transpose(int hilbert_number)
        {
            /* Store a hilbert integer (`hilbert_number`) as its transpose (`coods_list`).

            Args:
                hilbert_number(int): integer distance along hilbert curve

            Returns:
                coods_list(list): transpose of hilbert_number
            */

            List<List<int>> coods_list = new List<List<int>>();

            for (int i = 0; i < hilbert_number; i++)
            {
                List<int> coordinates = new List<int>();
                string i_bin = HilbertsCurve.ToBinary(i, this.iterator * this.dimention);
                for (int j = this.dimention; j < 2 * this.dimention; j++)
                {
                    coordinates.Add(HilbertsCurve.FromBinary(new string(i_bin.Where((ch, index) => index % (this.dimention) == (j - this.dimention)).ToArray())));
                }
                coods_list.Add(coordinates);
            }
            return coods_list;
        }

        private List<int> Hilbert_integer_to_transpose_single(int hilbert_number)
        {
            /* Store a hilbert integer (`hilbert_number`) as its transpose (`coordinate`).

            Args:
                hilbert_number(int): integer distance along hilbert curve

            Returns:
                coordinate(list): transpose of hilbert_number
            */
            List<int> coordinate = new List<int>();
            string i_bin = HilbertsCurve.ToBinary(hilbert_number, this.iterator * this.dimention);

            for (int i = 0; i < this.dimention; i++)
            {
                int j = 0;
                
                coordinate.Add(HilbertsCurve.FromBinary(new string(i_bin.Where((ch, index) => index % (this.dimention) == (i)).ToArray())));
                ++j;
                
            }
            return coordinate;
        }

        private int Transpose_to_hilbert_integer(List<int> coods_list)
        {
            /*R estore a hilbert integer (`hilbert_number`) from its transpose (`coods_list`).

        Args:
            coods_list (list): transpose of hilbert_number

        Returns:
            hilbert_number (int): integer distance along hilbert curve
        */
            List<string> binaries = new List<string>(); string temp_h_str = "";
            for (int i = 0; i < this.dimention; i++)
            {
                binaries.Add(HilbertsCurve.ToBinary(coods_list[i], this.iterator));
            }

            foreach (string i in binaries)
            {
                for (int j = 0; j < this.iterator; j++)
                {
                    temp_h_str += i[j];
                }
            }

            return HilbertsCurve.FromBinary(temp_h_str);
        }
        
        public List<int> Point_from_distance(int distance)
        {
            /*Return a point in n-dimensional space given a distance along a hilbert curve.

        Args:
            distance (int): integer distance along hilbert curve

        Returns:
            point (iterable of ints): an n-dimensional vector of lengh n where
            each component value is between 0 and 2**this.iterator-1.
        */

            List<int> point = new List<int>();
            int z; int t; int q = 2; int p;

            point = this.Hilbert_integer_to_transpose_single(distance);
            z = 2 << (this.iterator - 1);
            t = point[this.dimention - 1] >> 1;

            for (int i = this.dimention - 1; i > 0; i--)
            {
                point[i] ^= point[i - 1]; //logic
            }
            point[0] ^= t;

            // Undo excess work
            while (q != 2)
            {
                p = q - 1;

                for (int i = this.dimention - 1; i > -1; i--)
                {
                    if (Convert.ToBoolean(q & point[i]))
                    {
                        point[0] = point[0] ^ p;
                    }
                    else
                    {
                        t = (point[0] ^ point[i]) & p;
                        point[0] = point[0] ^ t;
                        point[i] = point[i] ^ t;
                    }
                }
                q <<= 1;
            }
            return point;
        }

        public List<List<int>> Points_from_distance(List<int> distances)
        {
            /*Return points in n-dimensional space given distances along a hilbert curve.

        Args:
            distances (iterable of int): iterable of integer distances along hilbert curve

        Returns:
            points (iterable of iterable of ints): an iterable of n-dimensional vectors
                where each vector has lengh n and component values between 0 and 2**iterator - 1.
        */

            List<List<int>> points = new List<List<int>>();

            foreach (int i in distances)
            {
                if (i > this.max_height)
                {
                    throw new ArgumentException($"All values in distances must be <= 2^(iterator * dimention)-1 ({Math.Pow(2, this.iterator * this.dimention) - 1})");
                }
                else if (i < this.min_height)
                {
                    throw new ArgumentException($"All values in distances must be >= {this.min_height}");
                }
            }

            foreach(int i in distances)
            {
                points.Add(this.Point_from_distance(i));
            }
            return points;
        }

        public int Distance_from_point(List<int> point)
        {
            /*Return distance along the hilbert curve for a given point.

        Args:
            point (iterable of ints): an n-dimensional vector where each component value
                is between 0 and 2**iterator - 1.

        Returns:
            distance (int): integer distance along hilbert curve
        */
            int m = 1 << (this.iterator - 1);
            int q = m; int p; int t;
            int distance;
            while (q > 1)
            {
                p = q - 1;
                for (int i = 0; i < this.dimention; i++)
                {
                    if (Convert.ToBoolean(q & point[i]))
                    {
                        point[0] ^= p;
                    }
                    else
                    {
                        t = (point[0] ^ point[i]) & p;
                        point[0] ^= t;
                        point[i] ^= t;
                    }
                }
                q >>= 1;
            }

            for (int i = 1; i < this.dimention; i++)
            {
                point[i] ^= point[i - 1];
            }

            t = 0;
            q = m;
            while (q > 1)
            {
                if (Convert.ToBoolean(q & point[this.dimention - 1]))
                {
                    t ^= q - 1;
                }
                q >>= 1;
            }

            for (int i = 0; i < this.dimention; i++)
            {
                point[i] ^= t;
            }

            distance = this.Transpose_to_hilbert_integer(point);
            return distance;
        }

        public List<int> Distances_from_points(List<List<int>> points)
        {

            List<int> distances = new List<int>();

            foreach(List<int> i in points)
            {
                if (i.Count != this.dimention)
                {
                    throw new ArgumentException($"All vectors in points must have length {this.dimention} ({Math.Pow(2, this.iterator * this.dimention) - 1})");
                }

                foreach (int j in i)
                {
                    if (j > this.max_x)
                    {
                        throw new ArgumentException($"All coordinate values in all vectors in points must be <= 2^iterator-1");
                    }
                    else if (j < this.min_x)
                    {
                        throw new ArgumentException($"All coordinate values in all vectors in points must be > {this.min_x}");
                    }
                }
            }

            foreach (List<int> i in points)
            {
                distances.Add(this.Distance_from_point(i));
            }

            return distances;
        }
    }
}
