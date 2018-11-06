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
