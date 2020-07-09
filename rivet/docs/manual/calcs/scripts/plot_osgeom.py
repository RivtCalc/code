import os
import sys
from pylab import *

def m_edict(filelines):
    """ make element dictionary

    [trussID] [type node1 node2 A matID]
    """

    edict = {}
    for i1 in filelines:
        try:
            i2 = i1.split()
        except:
            continue
        if i2[0] == 'element':
            if i2[1] == 'truss':
                edict[int(i2[2])] = [i2[1], int(i2[3]), int(i2[4]),
                                     float(i2[5]), int(i2[6])]
    return edict

def m_ndict(filelines):
    """ make node dictionary

    [nodeID] [x y z]
    """

    ndict = {}
    for i1 in filelines:
        try:
            i2 = i1.split()
        except:
            continue
        if i2[0] == 'node':
            if len(i2) == 4:
                ndict[int(i2[1])] = [float(i2[2]), float(i2[3])]
            else:
                ndict[int(i2[1])] = [float(i2[2]), float(i2[3]), float(i2[4])]
    return ndict

def plotgeo(ndict, edict, pltname):
    """ plot goemetry """

    clf()
    xlabel('x [in]')
    ylabel('y [in]')
    grid()
    ex = []
    ey = []
    ex4 = []
    ey4 = []
    eavg = []
    for en in edict:
        ex1 = ndict[edict[en][1]][0]
        ey1 = ndict[edict[en][1]][1]
        ex2 = ndict[edict[en][2]][0]
        ey2 = ndict[edict[en][2]][1]
        ex.append(ex1)
        ey.append(ey1)
        ex.append(ex2)
        ey.append(ey2)
        ex.append(None)
        ey.append(None)
        ex4.append(ex1)
        ey4.append(ey1)
        ex4.append(ex2)
        ey4.append(ey2)

        eavg.append([en,(ex1+ex2)/2.,(ey1+ey2)/2.])

    #axes().set_xlim = ((min(ex)-10, max(ex)+10))
    #axes().set_ylim = ((min(ey)-10, max(ey)+10))
    axes().set(aspect=1,
               xlim = ((min(ex4)*1.05, max(ex4)*1.05)),
               ylim = ((min(ey4)*1.05, max(ey4)*1.05)))

    #axes().set_aspect('equal', 'box')
    plot(ex, ey ,'k-', label="geometry")

    for k in ndict:
        text(ndict[k][0],ndict[k][1],k,fontsize=11, fontweight='bold')

    for j in eavg:
        text(j[1],j[2],j[0], fontsize=14, fontweight='bold')

    #legend()
    #show()
    savefig(pltname + ".png", bbox_inches='tight')


def osplot(tclfile):
    """  plot geometry for OpenSees tcl file

    function plots geometry using matplotlib

    Args:
    tcl file (file)

    methods called:
    ndict - generates node dictionary
    edict - generates element dictionary
    plotgeo - generates plot and writes to file
    """

    f = open(tclfile, 'r')
    filelines = f.readlines()
    f.close
    pltname = os.path.basename(tclfile).split('.')[0] + "fig"

    filelines = [j.strip('\n') for j in filelines]
    ndict = m_ndict(filelines)
    edict = m_edict(filelines)
    plotgeo(ndict, edict, pltname)
    return  "plot file '" + pltname + ".png'" + ' written'

#if __name__ == "__main__":
#    print('running as main')
#    file1 = sys.argv[1]
#    osplot(file1)
