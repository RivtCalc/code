"""Run batch program in dbmodel folder
    usage: python -m once -s modelbatch.py

   """
import os
import glob


def run():
    """run models
    
    """
    calclist1 = glob.glob('m*.txt')
    calclist1.sort()
    for itm1 in calclist1:
        print("< batch model run: " + itm1 +" >")
        cmdline1 = "python -m once " + itm1
        #print(cmdline1)
        os.system(cmdline1)


if __name__ == "__main__":
    modeldir = os.getcwd()
    print("====================================")
    print("on-c-e batch run" )
    print("model directory: " + modeldir)
    print("====================================")
    print("   ")
    run()
    