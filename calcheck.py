#!

from __future__ import print_function
import os
import datetime
import locale
import once.config as cfg

__version__ = "0.3.0"
__author__ = 'rholland'
#locale.setlocale(locale.LC_ALL, '')

class ModCheck(object):
    """minimum error checking and logging class

    """
    def __init__(self):
        """ open log file for events and errors

        """
        temppath = os.path.join(cfg.ppath , "temp")
        if not os.path.exists(temppath):
            os.makedirs(temppath)

        self.logname = ''
        self.logname = os.path.join(cfg.ppath , "temp", cfg.logfile)
        #print('log name,',self.logname)

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

