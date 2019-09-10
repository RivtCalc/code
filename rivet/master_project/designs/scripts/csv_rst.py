import sys
import csv
from tabulate import tabulate
import textwrap

def convert_csv(infile : string, 
                outfile : string, 
                wd1 : int=30):
    """ Convert csv to grid rst with max column width

    Args:
        infile : input file ".csv"
        outfile : output file ".rst"
        wd1 : max column width
    """
    with open(infile, 'r') as csvfile:
        reader = csv.reader(csvfile)
        parse1 = []
        for row in reader:
            for i in range(len(row)):
                templist = textwrap.wrap(row[i],width = wd1) 
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

if __name__ == "__main__":
    """ Run as command line script 
    """
    args = sys.argv
    input_file = args[1]
    wd = 30   # max column width
    try:
        wd = args[2]
    except:
        pass
    output_file = args[1].split(".")[0] + ".rst"
    #print(input_file, output_file)
    convert_csv(input_file, output_file, wd)  