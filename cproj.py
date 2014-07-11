from __future__ import division
from __future__ import print_function
from collections import OrderedDict
import oncepy.oconfig as cfg
import os


class ProjStart(object):
    """Assemble calcs into project calc set"""

    def __init__(self):
        """ Construct lists and dictionaries of project calc data

        **methods**
        build_pdict() constructs the proj calc data dictionary
        build_plist() constructs the proj calc model list

        """
        # files


        # method tags
        slist = ['[p]', '[:]', '[#]', '[~]']
        self.stags = slist
        self.ppath = cfg.ppath

        pend = False
        for _j in self.mstr:
            mtag = _j.strip()[0:3]
            if mtag == '[#]':
                if str(_j[:10]) == '[#] format': pend = True
                continue
            if pend and len(_j.strip()) == 0:
                pend = False
                continue
            if pend:
                continue
            self.mstrx.append(_j)
        #print('mstrx',self.mstrx)

    def build_pdict(self):
        """
        The dictionary structure is:
        [project data key]:[values]

        """
        self.aa = OrderedDict()
        #print(self.aa)

    def build_plist(self):
        """ build_plist() constructs the proj calc model list

        calc file list: [calcfile, pdfsize, calctemplate]

        """

        pass


class WritePcalc(object):
    """ Write the project PDF calc """

    pass
