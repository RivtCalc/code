import sys
import csv
import textwrap
from tabulate import tabulate
from tkinter import *

# default maximum column width
maxwidth = 30

def convert_csv(infile, outfile, maxwidth1):
    """ Convert csv to grid rst
    """
    with open(infile, 'r') as csvfile:
        reader = csv.reader(csvfile)
        parse1 = []
        for row in reader:
            for i in range(len(row)):
                templist = textwrap.wrap(row[i], maxwidth1) 
                row[i] = """\n""".join(templist)
                #row[i] = row[i].replace(" ","""\n""")
            parse1.append(row)

    #print(parse1)

    with open(outfile, "w") as out_file:
        try: 
            print("\ntabulating file `{}'".format(infile))
            out_file.write(tabulate(parse1,
                                tablefmt="grid",
                                headers="firstrow"))            
            print("\nrst table is in file `{}'".format(outfile))
        except:
            print("\nWriting file `{}' did not succeed.".format(outfile))
    
    with open(outfile, "r") as out1:
        file1 = out1.readlines()
    with open(outfile, "w") as out2:
        for i in file1:
            out2.write("    " + i)

def clickButton(event):
    widget = root.focus_get()
    if widget != root:
        widget.invoke()

if __name__ == "__main__":
    """ Run as command line script 
    """
    args = sys.argv
    input_file = args[1]
    output_file = args[1].split(".")[0] + ".rst"
    #print(input_file, output_file)
    
    try:
        if type(args[2]) is int:
            maxwidth = args[2]
    except:
        root=Tk()
        a=StringVar()
        Label(root, text="input max column width (characters) : ").pack()
        Entry(root, textvariable=a).pack()
        Button(root, text='Enter', command=root.destroy).pack()
        root.bind("<Return>", clickButton)
        root.mainloop()    
        try:
            maxwidth = int(a.get())
        except:
            maxwidth = 30
    
    convert_csv(input_file, output_file, maxwidth)  


