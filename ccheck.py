from __future__ import print_function
import os
import time
import oncepy.oconfig as cfg


class ModCheck(object):
    """beginnings of an error checking and logging class

    """
    def __init__(self):
        """ open log file for events and errors

        """
        # calc log
        self.logname = '_modellog.txt'

    def logstart(self):
        """delete log file and initialize new file

        """
        try:
            os.remove(self.logname)
        except:
            pass
        #print('log', estrng)
        with open(self.logname, 'w') as ef:
            ef.write("< start log - todo: write error logs >\n")
            ef.write("<" + time.strftime('%c') + ">\n")

    def errwrite(self, estrg, flg):
        """write processes to log file

        """
        #print('log', estrg)
        with open(self.logname, 'a') as ef:
            estrg += '\n'
            ef.write(estrg)
        if flg:
            print(estrg + '\n')
    def logclose(self):
        """close log file

        """
        try:
            with open(self.logname, 'a') as ef:
                ef.write("<" + time.strftime('%c') + ">\n")
                ef.write("< close log >")
        except IOError:
            print('error: log file not closed')

    def filesum(self):
        """file summary table

        """
        csumm2 =  ((" Files written:\n" +
                    " ------------------\n" +
                    " model file    :  {}\n" +
                    " python file   :  {}\n" +
                    " summary file  :  {}\n" +
                    " reST file     :  {}\n" +
                    " tex file      :  {}\n" +
                    " PDF file      :  {}\n").format(self.calcf, self.pyf,
                            self.sumf, self.rstfile, self.texfile, self.pdf))

        self.errwrite(csumm2, 1)

