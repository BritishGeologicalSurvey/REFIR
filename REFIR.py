"""
*** REFIR v1.0 ***
- component of REFIR 20.0 -
- Script to run FIX.py and FOXI.py in parallel -

Copyright (C) 2020 Tobias Dürig, Fabio Dioguardi
==============                     ===================
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
at your option any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

If you wish to contribute to the development of REFIR or to reports bugs or other problems with
the software, please write an email to me.

Contact: tobi@hi.is, fabiod@bgs.ac.uk


RNZ170318FS
"""

import os
import multiprocessing

dir1 = os.path.dirname(os.path.abspath(__file__))
proc = []
def launch_fix():
    import os
    print("Launching FIX")
    os.system("python FIX.py")

def launch_foxi():
    import os
    print("Launching FOXI")
    os.system("python FOXI.py")

#runInParallel(launch_fix, launch_foxi, control_widget)
if __name__ == '__main__':
    fns = (launch_fix, launch_foxi)
    for fn in fns:
        p = multiprocessing.Process(target=fn)
        proc.append(p)
        p.start()
