#!/usr/bin/env python

from numpy import *
from numpy.linalg import solve as nsolve
from pprint import pprint
from pylab import *

"""
direct stiffness method - functions

"""

def length(x,y):
    """pythagorean distance"""

    pdist = sqrt((x[1]-x[0])**2+(y[1]-y[0])**2)

    #print('pdist', pdist)
    return pdist

def thet(x,y):
    """angle of element with horizontal axis"""

    y = y[1]-y[0]
    x = x[1]-x[0]
    try:
        th = arctan(y/x)
    except: th = 0
    if y == 0. : th = 0
    if x == 0. : th = pi/2.
    if y < 0 or x < 0:
        th = th + pi

    #print('th', th)
    return th

def node_dict(nodes, elements, reacts, load1):
    """node and element dictonaries"""

    # [ a, b, c, d] a=restraint, b=direction, c=node, d=force
    dof_list=[]

    # node no: [x, y]
    node = {}

    # element no: [n1, n2, area, modulus]
    element = {}

    for i in nodes:
        node[i[0]] = [i[1], i[2]]
    for i in elements:
        element[i[0]] = [i[1], i[2], i[3], i[4]]

    # populate dof list
    for i in node:
        dof_list.append([0,1,i,0])
        dof_list.append([0,2,i,0])

    for i in reacts:
        for j in dof_list:
            nd = i[0]
            if nd == j[2]:
                dof_list[nd*2][0] =   i[1]
                dof_list[nd*2+1][0] = i[2]

    for i in load1:
        for j in dof_list:
            nd = i[0]
            if nd == j[2]:
                dof_list[nd*2][3] =   i[1]
                dof_list[nd*2+1][3] = i[2]

    #print('n,e,d', node, element, dof_list, sep='\n')
    return node, element, dof_list

def assem_global(node, element, dof_list):
    """assemble global stiffness matrix"""

    k = zeros((len(dof_list),len(dof_list)))

    for i in element:
        node1 = element[i][0]
        node2 = element[i][1]
        x = [node[node1][0],node[node2][0]]
        y = [node[node1][1],node[node2][1]]

        lngth = length(x,y)
        theta = thet(x,y)
        stifc = (element[i][2]*element[i][3])/lngth

        rc1 = node1*2
        rc2 = node1*2 + 1
        rc3 = node2*2
        rc4 = node2*2 + 1

        # diagonal terms
        k[rc1][rc1] += cos(theta)**2*stifc
        k[rc2][rc2] += sin(theta)**2*stifc
        k[rc3][rc3] += cos(theta)**2*stifc
        k[rc4][rc4] += sin(theta)**2*stifc

        # off diagonal
        k[rc1][rc2] += (sin(theta)*cos(theta))*stifc
        k[rc2][rc1] = k[rc1][rc2]
        k[rc1][rc3] += -(cos(theta)**2)*stifc
        k[rc3][rc1] = k[rc1][rc3]
        k[rc1][rc4] += (-sin(theta)*cos(theta))*stifc
        k[rc4][rc1] = k[rc1][rc4]
        k[rc2][rc3] += (-sin(theta)*cos(theta))*stifc
        k[rc3][rc2] = k[rc2][rc3]
        k[rc2][rc4] += (-sin(theta)**2)*stifc
        k[rc4][rc2] = k[rc2][rc4]
        k[rc3][rc4] += (sin(theta)*cos(theta))*stifc
        k[rc4][rc3] = k[rc3][rc4]

    #set_printoptions(linewidth = 100)
    #print('global k')
    #print(k)
    return k

def displace(k, dof_list, node):
    """displacements and reactions"""

    # load vector
    p=zeros(2*len(node))
    for i in dof_list:
        indx = i[2]*2 + i[1]-1
        p[indx] = i[3]

    # deflections
    kreduce = []
    for i in dof_list:
        indx = i[2]*2 + i[1]-1
        if i[0]:
            kreduce.append(indx)
    k1 = delete(k, kreduce, 0)
    k1 = delete(k1, kreduce, 1)
    p2 = delete(p, kreduce, 0)
    #print(p2, k2, sep='\n')

    defxy = nsolve(array(k1), array(p2))
    #print('defxy', defxy)

    # reactions
    kreact = list(range(2*len(node)))
    for i in kreduce:
        kreact.remove(i)
    k2 = delete(k, kreact, 0)
    k2 = delete(k2, kreduce, 1)
    preact = dot(k2, defxy)
    #print('reactions', preact)

    dof_defx = {}
    dof_defy = {}
    reactx = {}
    reacty = {}

    re = enumerate(preact)
    en = enumerate(defxy)
    for i in range(2*len(node)):
        if i in kreduce:
            if i%2 == 0:
                dof_defx[i//2] = 0.
                reactx[i//2] = next(re)[1]
            else:
                dof_defy[i//2] = 0.
                reacty[i//2] = next(re)[1]
        else:
            if i%2 == 0:
                dof_defx[i//2] = next(en)[1]
            else:
                dof_defy[i//2] = next(en)[1]

    #print('x, y displ', dof_defx, dof_defy, sep='\n')
    return dof_defx, dof_defy, reactx, reacty

def axial_elem(uv, theta, stifc):
    """element stiffness matrix"""

    kel = zeros((2,4))
    kel[0][0] = cos(theta)**2*stifc
    kel[0][1] += (sin(theta)*cos(theta))*stifc
    kel[0][2] = -(cos(theta)**2)*stifc
    kel[0][3] += (-sin(theta)*cos(theta))*stifc
    kel[1][0] += (sin(theta)*cos(theta))*stifc
    kel[1][1] += sin(theta)**2*stifc
    kel[1][2] += (-sin(theta)*cos(theta))*stifc
    kel[1][3] += -sin(theta)**2*stifc
    el1 = dot(kel,uv)
    kelm = dot([cos(theta), sin(theta)], el1)

    #print('element k', kelm)
    return kelm

def axial_force(dof_defx, dof_defy, node, element):
    """return elment forces in dictionary"""

    el_force = {}
    for i in element:
        node1 = element[i][0]
        node2 = element[i][1]
        x = [node[node1][0], node[node2][0]]
        y = [node[node1][1], node[node2][1]]
        lngth = length(x,y)
        theta = thet(x,y)
        stifc = (element[i][2]*element[i][3]) / lngth
        uv = [dof_defx[node1], dof_defy[node1],
              dof_defx[node2], dof_defy[node2]]

        fa = axial_elem(uv, theta, stifc)
        el_force[i] = -fa

    #print('element force', el_force)
    return el_force

def disp_tables(dof_defx, dof_defy, af, rx1, ry1):
    """return table of displacements"""

    s2 = s5 = s7 = s12 = s15 = ''

    s1 = '  node        x displacement \n'
    for i in dof_defx:
        s2 += (str(i).strip()).center(8) + str(dof_defx[i]).rjust(15) + '\n'
    s4 = '  node        y displacement \n'
    for i in dof_defy:
        s5 += (str(i).strip()).center(8) + str(dof_defy[i]).rjust(15) + '\n'


    s11 = '  node           reaction  \n'
    for i in rx1:
        s12 += (str(i).strip()).center(8) + 'x dir ' + str(rx1[i]).rjust(11) + '\n'
    for i in ry1:
        s15 += (str(i).strip()).center(8) + 'x dir ' + str(ry1[i]).rjust(11) + '\n'

    for i in af:
        s6 = '  element        axial force \n'
        s7 += (str(i).strip()).center(8) + str(af[i]).rjust(15) + '\n'

    table1 = ''.join([s1,s2,s4,s5, s11, s12, s15, s6, s7])

    #print('tables', table1)
    return table1

def plot_geom(plttype, node, element, el_force, dof_defx, dof_defy,
              load1, react1, rx1, ry1, title1):
    """ plot geometry

    plot type
    1 = plot element and node numbers
    2 = plot loads
    3 = plot element forces and react
    """
    dsc = 100     # deflection scale factor
    fs1 = 12    # font size

    # format values
    eavg={}
    for i in element:
        exa = (node[element[i][0]][0] + node[element[i][1]][0]) / 2.
        eya = (node[element[i][0]][1] + node[element[i][1]][1]) / 2.
        eavg[i] = ["%.1f" % el_force[i],exa,eya]

    exa = [eavg[i][1] for i in eavg]
    eya = [eavg[i][2] for i in eavg]

    clf()
    # get ranges
    ex_min = min([node[i][0] for i in node])
    ey_min = min([node[i][1] for i in node])
    ex_max = max([node[i][0] for i in node])
    ey_max = max([node[i][1] for i in node])
    ex_del = ex_max - ex_min
    ey_del = ey_max - ey_min

    # geometry
    if plttype == 1:
        for k in node:
            text(node[k][0],node[k][1],k,fontsize=fs1,
                 fontweight='bold')
        for k in element:
            text(eavg[k][1],eavg[k][2],'-'+str(k)+'-', fontsize=fs1)
    # loads and reactions
    elif plttype == 2:
        for j in load1:
            text(node[j[0]][0],node[j[0]][1]+.05*ey_del,str(j[1])+' | '+str(j[2]),
                 horizontalalignment='center', fontsize=fs1)
        for j in react1:
            text(node[j[0]][0],node[j[0]][1]-.15*ey_del,str(j[1])+' | '+str(j[2]),
                 horizontalalignment='center', fontsize=fs1, fontweight='bold')
    # element forces
    elif plttype == 3:
        for i in element:
            text(eavg[i][1], eavg[i][2], eavg[i][0], fontsize=fs1)
        for q in rx1:
            text(node[q][0], node[q][1]-.15*ey_del," %.1f |" % rx1[q] ,fontsize=fs1,
                 horizontalalignment='right', fontweight='bold')
        for q in ry1:
            text(node[q][0], node[q][1]-.15*ey_del, "| %.1f " % ry1[q], fontsize = fs1,
                 horizontalalignment='left', fontweight='bold')

    # plot shape
    ev = element.values()
    for jj in ev:
        ex = [node[jj[0]][0], node[jj[1]][0]]
        ey = [node[jj[0]][1], node[jj[1]][1]]

        exd = [node[jj[0]][0] + (dsc*dof_defx[jj[0]]),
            node[jj[1]][0] + (dsc*dof_defx[jj[1]])]

        eyd = [node[jj[0]][1] + (dsc*dof_defy[jj[0]]),
            node[jj[1]][1] + (dsc*dof_defy[jj[1]])]

        plot(ex,ey,'k-',linewidth = 1.0)

        if plttype == 2:
            plot(exd,eyd,'k--',linewidth = 2.0)

    grid()
    title(title1)

    xlabel('x')
    ylabel('y')
    axes().set(aspect=1,
            xlim = (ex_min - .1*ex_del, ex_max + .2*ex_del),
            ylim = (ey_min - .2*ey_del, ey_max + .2*ey_del))

    figname = 'geom'+str(plttype)+'.png'
    savefig(figname, bbox_inches='tight')

def direct_stiff(node1, element1, react1,load1):
    """executes stiffness functions

    1. structure dictionaries   : node_dict()
    2. global stiffness         : assem_global()
    3. displacements and reacts : displace()
    4. element forces           : axial_force()
    5. tables and plots         : disp_tables(), force_tables()
    """

    # 1. generate structure dictionary
    n1, e1, dof1 = node_dict(node1, element1, react1, load1)

    # 2. generate global stiffness
    globalk = assem_global(n1, e1, dof1)

    # 3. calculate displacements and reactions
    dx, dy, rx, ry =  displace(globalk, dof1, n1)

    # 4. calculate element forces
    aforce = axial_force(dx, dy, n1, e1)

    # 5. write tables and plots
    dtable = disp_tables(dx, dy, aforce, rx, ry)
    plot_geom(1, n1, e1, aforce, dx, dy, load1, react1, rx, ry,
              'Nodes and Elements')
    plot_geom(2, n1, e1, aforce, dx, dy, load1, react1, rx, ry,
              'Loads, Restraints and Deflected Shape')
    plot_geom(3, n1, e1, aforce, dx, dy, load1, react1,rx ,ry,
              'Axial Force and Reactions')

    return dtable
