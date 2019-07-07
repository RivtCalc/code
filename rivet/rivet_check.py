#!

__version__ = "0.3.0"
__author__ = 'rholland'


def logstart(self):
    """delete log file and initialize new file

    """
    try: os.remove(self.logname)
    except: pass
    with open(self.logname, 'w') as el:
        el.write("< start log: " + str(datetime.datetime.now()) + "  >\n")
    return self.logname

def logwrite(self, estrg, flg):
    """write processes to log file, option echo to terminal

    """
    #print('log', estrg)
    with open(self.logname, 'a') as ef:
        estrg += '\n'
        ef.write(estrg)
    if flg:
        print(estrg)

def logclose(self):
    """close log file

    """
    try:
        with open(self.logname, 'a') as ef:
            ef.write("\n< close log: "  + str(datetime.datetime.now()) + " >")
    except IOError:
        print('error: log file not closed')

