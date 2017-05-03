"""Run script from model folder. Read all toc files in the temp folder.  
   Write the toc PDF to the calc folder.
   """

import sys
import csv
import os
import glob
import shutil

preamble = r"""\\documentclass[12pt,notitle]{report}
% generated by Docutils <http://docutils.sourceforge.net/>
\\usepackage{fixltx2e} % LaTeX patches, \\textsubscript
\\usepackage{cmap} % fix search and cut-and-paste in Acrobat
\\usepackage{ifthen}
\\usepackage[T1]{fontenc}
\\usepackage[utf8]{ }
\\usepackage{amsmath}
\\usepackage{float} % float configuration
\\floatplacement{figure}{H} % place figures here definitely
\\usepackage{graphicx}
\\setcounter{secnumdepth}{0}

%%% Custom LaTeX preamble
% PDF Standard Fonts
\\usepackage{mathptmx} % Times
\\usepackage[scaled=.90]{helvet}
\\usepackage{courier}

%%% User specified packages and stylesheets
\\usepackage{C:/Anaconda3/lib/site-packages/once/once}



%% pagestyle plain
\\fancypagestyle{plain}{%
\\fancyhf{}
%\\fancyhead[L]{\\leftmark}
%\\fancyhead[R]{\\normalsize Page \\thepage\\ of \\pageref*{LastPage} \\phantom{aaaaaaaaaa}}
%\\renewcommand\\chaptermark[1]{\\markboth{#1}{}} 
%\\renewcommand\\sectionmark[1]{\\markright{\\thesection.\\ #1}}
\\fancyfoot[C]{}
\\renewcommand\\headrulewidth{0pt}
\\renewcommand\\footrulewidth{1pt}
}
%% pagestyle fancy
%% header
\\pagestyle{fancy}
\\fancyhf{}
\\fancyhead[L]{\\leftmark}
\\fancyhead[R]{\\phantom{aaaaaaaaaa}}
%\\renewcommand\\chaptermark[1]{\\markboth{#1}{}} 
%\\renewcommand\\sectionmark[1]{\\markright{\\thesection.\\ #1}}
%% footer
\\fancyfoot[C]{}
\\renewcommand\\headrulewidth{1pt}
\\renewcommand\\footrulewidth{1pt}


%%% Fallback definitions for Docutils-specific commands

% providelength (provide a length variable and set default, if it is new)
\\providecommand*{\\DUprovidelength}[2]{
  \\ifthenelse{\\isundefined{#1}}{\\newlength{#1}\\setlength{#1}{#2}}{}
}

% lineblock environment
\\DUprovidelength{\\DUlineblockindent}{2.5em}
\\ifthenelse{\\isundefined{\\DUlineblock}}{
  \\newenvironment{DUlineblock}[1]{%
    \\list{}{\\setlength{\\partopsep}{\\parskip}
            \\addtolength{\\partopsep}{\\baselineskip}
            \\setlength{\\topsep}{0pt}
            \\setlength{\\itemsep}{0.15\\baselineskip}
            \\setlength{\\parsep}{0pt}
            \\setlength{\\leftmargin}{#1}}
    \\raggedright
  }
{\\endlist}}
{}
"""

preamble = preamble.replace("\\\\","\\")

enddoc = """\\end{document}
"""

def run():
    '''
    run as a command line program from the model directory
    usage: python -m once -s projecttoc.py
    '''

    cwd1 = os.getcwd()                  
    os.chdir("..")
    cwd2 = os.getcwd()
    path2 = os.path.join(cwd2, "reprt")
    os.chdir(path2)
    list1 = glob.glob('*.toc')
    list1.sort()
    print(list1)
    tocpart = ""        
    inx1 = 1
    s2 = ''

    for inp1 in list1:
        with open(inp1,'r') as file2:
            s1 = file2.read()  
        for j in range(1,100):
            tst1 = "{chapter." + str(j) +"}"
            s1=s1.replace(tst1," ")
        with open(inp1, 'w') as file3:
            file3.write(s1)
    
    with open("reportmerge.txt",'r') as file0:
        calclist = file0.readlines()

    bodydoc = """%%% Body
    \\renewcommand{\\contentsname}{""" + calclist[0].strip() + """}
    %\\renewcommand{\\chaptername}{}
    
    \\begin{document}
    \\tableofcontents
    
    \\today
    \\newline
    \\newline
    """

    for item1 in calclist:        
        if item1.split('|')[0].strip() ==  'm':
            inx1+=1
            s2 = """
            \\underline{\\textbf{"""+ item1.split('|')[1].strip()+"""}}
            \\makeatletter
            \\input{""" + inp1 + """}
            \\makeatother
            \\vspace{6mm}
            """
        elif item1.split('|')[0].strip() ==  'a':
            s2 = """
            Appendix:  """ + (item1.split('|'))[1].strip() +"""
            \\vspace{6mm}
            """
        else:
            s2 = ' '
        
        tocpart += s2
        print('s2',s2)
    
    tocstring = preamble + bodydoc + tocpart + enddoc
    with open("projecttoc.tex", 'w') as file1:
        file1.write(tocstring)

    pdf1 ='latexmk -xelatex -quiet -f ' + os.path.join(path2, 'projecttoc.tex')
    os.system(pdf1)
    
    try:
        os.remove("projecttoc.toc")
    except:
        pass

def clean():
    cleanlist = ('*.aux', '*.out', '*.fls', '*.fdb_latexmk', '*.aux')
    for i1 in cleanlist:                            
        for f1 in glob.glob(i1):
            try:
                os.remove(f1)
            except OSError:
                pass

    
if __name__ == "__main__":
    clean()
    run()
    clean()

