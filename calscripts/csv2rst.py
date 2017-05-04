"""Run script from model folder. Reads all csv files in the table folder.  
   Write the restructured text table. First row are column headings.
   """

import sys
import csv
import os
import glob

def get_out(out=None):
    """ return a file like object from different kinds of values
    None: returns stdout
    string: returns open(path)
    file: returns itself
    """

    if out is None:
        return sys.stdout
    else:
        return out

def underline(title, underliner="=", endl="\n", out=None):
    """ write *title* *underlined* to *out*
    """
    
    out = get_out(out)

    out.write(title)
    out.write(endl)
    out.write(underliner * len(title))
    out.write(endl * 2)

def separate(sizes, out=None, separator="=", endl="\n"):
    """write the separators for the table using sizes to get the
    size of the longest string of a column
    """
    
    out = get_out(out)

    for size in sizes:
        out.write(separator * size)
        out.write(" ")

    out.write(endl)

def write_row(sizes, items, out=None, endl="\n"):
    '''
    write a row adding padding if the item is not the
    longest of the column
    '''
    out = get_out(out)

    for item, max_size in zip(items, sizes):
        item_len = len(item)
        out.write(item)

        if item_len < max_size:
            out.write(" " * (max_size - item_len))

        out.write(" ")

    out.write(endl)

def process(in_=None, out=None, title=None):
    '''
    read a csv table from in and write the rest table to out
    print title if title is set
    '''
    handle = open(in_,'r')
    #out = out

    reader = csv.reader(handle)

    rows = [row for row in reader if row]
    cols = len(rows[0])
    sizes = [0] * cols

    for i in range(cols):
        for row in rows:
            row_len = len(row[i])
            max_len = sizes[i]

            if row_len > max_len:
                sizes[i] = row_len

    if title:
        underline(title)

    separate(sizes, out)
    write_row(sizes, rows[0], out)
    separate(sizes, out)

    for row in rows[1:]:
        write_row(sizes, row, out)

    separate(sizes, out)

def run():
    '''
    run as a command line program from the model directory
    usage: python -m once -s cvs2rst.py
    '''
    cwd1 = os.getcwd()                  
    os.chdir("..")
    proj_root = os.getcwd()
    path2 = os.path.join(proj_root, "dbtable")
    os.chdir(path2)
    list1 = glob.glob('*.csv')
    #print(list1)
    title = ''
    # write tables to files
    for filex in list1:
        fileout1 = filex.replace('.csv','.rst')           
        with open(fileout1, 'w') as file1: 
            process(filex, out = file1, title=title)
        while process(filex) != None:
            print(process(filex))
        
    
if __name__ == "__main__":
    run()
    