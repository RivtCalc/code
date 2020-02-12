#! python 
#%%
from rivet.rivet_lib import *

#%%  
i__(""" [[01]] Load Summations
    
    The need to distinguish between the various meanings of "frame of
    reference" has led to a variety of terms. For example, sometimes the type
    of coordinate system is attached as a modifier, as in Cartesian frame of
    reference [#]_.
    
    || [#] footnote text

    Sometimes the state of motion asfda asd s fdas sfdfasdfasdf is
    emphasized, as in rotating frame of reference.  

                        2
                    d w
            M = -EI ───                                 
                        2
                    dx 

    
                     (x + i y)
         ┌── 10   ijk
      ζ= >     ────────────                            
         └── i=4   (γ+ 4)


    Insert text from text, rst, docx or html files
    || text | i,p,5 | ttext1.txt   
    
    Render equations
    || tex  | .5,# | x = \\frac{1 + \\omega}{2 + \\gamma} |
    || ACI 318-05 5.5.1

    || sym | .5,# | x = (1 + omega + α) / (4 + gamma)  | 
    || ACI 318-05 5.5.2

    Render image file
    || img | .5,# | pic1.png |  
    || inserted png file  

    || img | .5,# | pic2.jpg  |
    || inserted jpg file   

    Some added text xxxx is put here and a bit of nonsense to make some
    words for a paragraph.

    Insert table from csv or xlsx files
    || table | r[:]c[1,2]w10 | rebars.csv |  
    || Rebar Table from CSV file [#]_  
    
    || table | r[:]c[1,2] | rebars.xlsx |  
    || Rebar Table from Excel file

    || table | rest | rebars.rst  | 
    || Rebar Table from reST file
    
    || table | include | Table Title [#]_

    +-----------+-------+--------+-------------+-----------+
    |   barsize |   dia |   area |   perimeter |   wt/foot |
    +===========+=======+========+=============+===========+
    |         2 | 0.25  |   0.05 |        0.79 |     0.167 |
    +-----------+-------+--------+-------------+-----------+
    |         3 | 0.375 |   0.11 |        1.18 |     0.376 |
    +-----------+-------+--------+-------------+-----------+
    |         4 | 0.5   |   0.2  |        1.57 |     0.668 |
    +-----------+-------+--------+-------------+-----------+
    |         5 | 0.625 |   0.31 |        1.96 |     1.043 |
    +-----------+-------+--------+-------------+-----------+
    |         6 | 0.75  |   0.44 |        2.36 |     1.502 |
    +-----------+-------+--------+-------------+-----------+
    |         7 | 0.875 |   0.6  |        2.75 |     2.044 |
    +-----------+-------+--------+-------------+-----------+
    |         8 | 1     |   0.79 |        3.14 |     2.67  |
    +-----------+-------+--------+-------------+-----------+
    |         9 | 1.128 |   1    |        3.54 |     3.4   |
    +-----------+-------+--------+-------------+-----------+
    |        10 | 1.27  |   1.27 |        3.99 |     4.303 |
    +-----------+-------+--------+-------------+-----------+
    |        11 | 1.41  |   1.56 |        4.43 |     5.313 |
    +-----------+-------+--------+-------------+-----------+
    |        14 | 1.693 |   2.25 |        5.32 |     7.65  |
    +-----------+-------+--------+-------------+-----------+
    |        18 | 2.257 |   4    |        7.09 |    13.6   |
    +-----------+-------+--------+-------------+-----------+

    || [#] footnote text

    """)
#%%
v__(""" some values 
    
    Some text if needed

    a11 = 12.23              | description 1 
    a22 = 2.2                | description 2 
    a33 = 14                 | description 3 
    Beam1 : aisc12.csv [4]   | beam properties 
    i_x = Beam1[2]           | I major
    i_y = Beam2[3]           | I minor

    """)

e__(""" equations label 
    
    Some introductory text.

    aa2 = a11*14    | [2,2,1,2,#] | 
    equation label  

     
    aa22 = aa2*5    | [2,2,0,2,#] |
    equation label

    """)
#%%
i__(""" [[02]] Seismic Analysis
    
    This is a test γ = 2*Σ of the system and this is a further test
    and another greek letter Γ₂.

    The need to distinguish between the various meanings of "frame of
    reference" has led to a variety of terms. For example, sometimes the type
    of coordinate

    || newpage

    The way it transforms to frames considered as related is emphasized as in
    Galilean frame of reference. Sometimes frames are distinguished by the
    scale of their observations, as in macroscopic and microscopic frames of
    reference [CIT2000]_.

    || [CIT2000] citation text

    """)

v__(""" some values

    this is one line 4 γ
  
    gg = 5.4    | height of roof 
    hh = 12.2   | height of balcony
    w1 = 2.2    | uniform load 

    """)

e__(""" some equations
    
    xx1 = gg + 4     | [2,2,0,#,1] |
    equation label and number

    xx2 = hh + 10    | [2,2,0,2,#]
    no equation label

    """)

#%%
t__(""" [[03]] Manipulate Tables (dataframes) and Plots    

    read csv file into dataframe
    || read | T1 | rebars.csv  
    
    create and populate a table    
    || create | T2 | rebars2.csv
    T2["len1"] = range(1,8)  
    T2["area1"] = range(10,17)  
    T2["prod"] = T2["area1"]*T2["len1"]
    || save | table | T2
    
    insert a table
    || table | rest | rebars2.rst |
    Deflection Table

    plot some data from csv 
    || plot | tb1.csv | x="dia", y="area", row=[1:10], kind="line", grid=1   
    || add  | x="dia", y="perimeter", color="blue"  |
    || save | plot | tb1.png | 

    || img | .5 | tb1.png |
    plot title

    """)

r__(""" write calc, docs or report to files 

    write_utfcalc()
    #write_pdfdoc()
    #write_htmldoc()
    #write_pdfreport()
    
    """)
