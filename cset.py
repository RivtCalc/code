from __future__ import division
from __future__ import print_function
from collections import OrderedDict
import oncemod.config as om


class SetDict(object):

    def __init__(self, mfile):
        """
        Constructs an ordered dictionary of operations in a project set

        **methods**

        sdicts() constructs the set dictionary
        tag_p() add project parameters to set dictionary
        tag_c() add collect parameters to set dictionary

        """
        # files
        setfile = mfile
        mofile.close()
        self.cfolder = mpath

        # dictionaries and lists
        self.sdict = OrderedDict()

        # method tags
        slist = ['[p]', '[c]', '[:]', '[#]', '[~]']
        self.stags = slist


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

    def sdicts(self):
        """
        Build the set dictionary.

        The key for a [p] operation is info
        The key for a [c] operation is set

        The dictionary structure is:
        project data:[[p], globaltemplate, globalsize, [projdata]
        collect calc file: [[c], calcfile, pdfstyle, calcset]

        """

        for i in self.mstrx:
            #print('i', i.strip())
            if len(i.strip()) == 0:
                stag = '[~]'  # blank
            else:
               pass
            #print('tag ', stag)

            # pending blocks
            pendlist = ['p', 'c']
            if pend == 'c' and stag == '[~]':
                self.tag_c(ip)
            elif pend == 'p' and i == '[:] ':
                self.tag_p(ip)
            if pend in pendlist and stag != '[~]':
                ip += i
                continue

            # select tag
            if stag in self.stags:
                if stag ==   '[p]':
                    ip += i
                    pend = 'p'
                elif stag == '[c]':
                    ip += i
                    pend = 'c'
                else:
                    continue
        #for i in self.odict: print(self.odict[i])

    def tag_p(self, ip):
        """add [p] to sdict """
        pass

    def tag_c(self, ip):
        """add [c] to sdict """
        pass


class SetPDF(object):
    pass
