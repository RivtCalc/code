"""Run script from model folder. Write the restructured text table.
   First row are column headings.  If called from command line then
   all csv files in folder are converted.
   
   """
import sys
import csv
import os
import glob

def _get_out(out=None):
    """ return a file like object from different kinds of values
    None: returns stdout
    file: returns itself
    
    """
    if out is None:
        return sys.stdout
    else:
        return out

def _underline(title, underliner="=", endl="\n", out=None):
    """ write *title* *underlined* to *out*
    
    """
    out = _get_out(out)
    out.write(title)
    out.write(endl)
    out.write(underliner * len(title))
    out.write(endl * 2)

def _separate(sizes, out=None, separator="=", endl="\n"):
    """write the separators for the table using sizes
    to get the size of the longest string of a column
    
    """
    out = _get_out(out)
    for size in sizes:
        out.write(separator * size)
        out.write(" ")
    out.write(endl)

def _write_row(sizes, items, out=None, endl="\n"):
    """write a row adding padding
       if the item is not the longest of the column
    
    """
    out = _get_out(out)
    for item, max_size in zip(items, sizes):
        item_len = len(item)
        out.write(item)
        if item_len < max_size:
            out.write(" " * (max_size - item_len))
        out.write(" ")
    out.write(endl)

def _process(in_=None, out=None, title=None):
    """read a csv table from in and write the rest table to out
    
    """
    handle = open(in_,'r')
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
        _underline(title)
    _separate(sizes, out)
    _write_row(sizes, rows[0], out)
    _separate(sizes, out)
    for row in rows[1:]:
        _write_row(sizes, row, out)
    _separate(sizes, out)

def _run(csvfile, width):
    """convert csv file to rst table with same base file name
    
    """
    cwd1 = os.getcwd()                  
    os.chdir("..")
    proj_root = os.getcwd()
    path2 = os.path.join(proj_root, "dbtable")
    os.chdir(path2)
    list1 = glob.glob('*.csv')
    #print(list1)
    title = ''
    # write tables to files and terminal
    fileout1 = csvfile.replace('.csv','.rst')           
    with open(fileout1, 'w') as file1: 
        _process(csvfile, out = file1, title=title)
    with open(fileout1, 'r') as file2:
        rsttab = file2.read()
    return rsttab
    
def _rundir():
    """run a command line program from the model directory
    usage: python -m once -s cvs2rst.py  (n,n,n)
    All csv files in directory are converted. 
    
    n,n,n are the optional character widths of
    columns 2,3 and 4.  Use 0 if column does not exist or omit
    for single line per cell. (not yet implemented)

    """
    cwd1 = os.getcwd()                  
    os.chdir("..")
    proj_root = os.getcwd()
    path2 = os.path.join(proj_root, "dbtable")
    os.chdir(path2)
    list1 = glob.glob('*.csv')
    #print(list1)
    title = ''
    # write tables to files and terminal
    for filex in list1:
        fileout1 = filex.replace('.csv','.rst')           
        with open(fileout1, 'w') as file1: 
            _process(filex, out = file1, title=title)
        while _process(filex) != None:
            print(_process(filex))
        
    
if __name__ == "__main__":
    _rundir()
    