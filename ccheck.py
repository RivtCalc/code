from __future__ import print_function
import os
import oncepy.oconfig as cfg

class ModCheck(object):

    def __init__(self):
        """ check model syntax and record events"""
        # calc log
        lname = cfg.mfile
        logn = lname.split('.')
        self.logname = '.'.join([logn[0], 'log' + logn[1], logn[2]])

    def ewrite1(self, estrng):
        """initialize file"""
        try:
            os.remove(self.logname)
        except:
            pass

        print(estrng)
        ef = open(self.logname, 'w')
        estrng += '\n'
        ef.write(estrng)
        ef.close()

    def ewrite2(self, estrng):
        """write processes"""
        print(estrng)
        ef = open(self.logname, 'a')
        estrng += '\n'
        ef.write(estrng)
        ef.close()
