from __future__ import division
from __future__ import print_function
from collections import OrderedDict
import once.config as cfg
import os


class ProjStart(object):
    """Compile calcs into a project calc set - not started"""

    def __init__(self):
        """ Construct lists and dictionaries of project calc data
        ::
        
          **methods**
          build_pdict() constructs the proj calc data dictionary
          build_plist() constructs the proj calc division list
        
          pdf=
          always
          never
          asneeded
        """
        # files


        # method tags
        plist = ['[p]', '[#] pformat' '[#]', '[~]']
        self.ptags = plist
        self.pd = OrderedDict()


    def build_pdict(self):
        """constructs the project data dictionary

        """
        pass


    def build_plist(self):
        """ constructs the proj calc division list

        """

        pass


class WritePcalc(object):
    """ Write the project PDF calc """

    pass
