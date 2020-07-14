import os
import fnmatch

def Walk(root='.', recurse=False, pattern='*'):
    """
        Generator for walking a directory tree.
        Starts at specified root folder, returning files
        that match our pattern. Optionally will also
        recurse through sub-folders.
    """
    for path, subdirs, files in os.walk(root):
        for name in files:
            #print("name", name)
            if fnmatch.fnmatch(name, pattern):
                yield os.path.join(path, name)
        if not recurse:
            break

def LOC(root='', recurse=False, spec="*.txt"):
    """
        Counts lines of code in two ways:
            maximal size (source LOC) with blank lines and comments
            minimal size (logical LOC) stripping same

    """
    count_mini, count_maxi = 0, 0
    root = os.getcwd()
    numfile = 0
    for fspec in Walk(root, recurse, spec1):
        #print('x', fspec)
        numfile +=1
        skip = False
        for line in open(fspec).readlines():
            count_maxi += 1
            
            line = line.strip()
            if line:
                if line.startswith('#'):
                    continue
                if line.startswith('"""'):
                    skip = not skip
                    continue
                if not skip:
                    count_mini += 1

    return count_mini, count_maxi, numfile
  
if __name__ == "__main__":
    cwd1 = os.getcwd()
    print("Lines of Code")
    print("=============")
    print("current directory: ", cwd1)
    spec1 = "*.txt"
    min1,max1,numf = LOC(spec = spec1)
    print(spec1, ": min  = ", min1, " | max  = ", max1, " | files = ", numf)
    spec1 = "*.py"
    min1,max1,numf = LOC(spec = spec1)
    print(spec1, ": min  = ", min1, " | max  = ", max1, " | files = ", numf)
      