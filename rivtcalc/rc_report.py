import once.config as cfg
import os

    def reprt_list(self):
        """Append calc name to reportmerge.txt
        
        """
        try: 
            filen1 = os.path.join(self.rpath, "reportmerge.txt")
            print(filen1)
            file1 = open(filen1, 'r')
            mergelist = file1.readlines()
            file1.close()
            mergelist2 = mergelist[:]
        except OSError:
            print('< reportmerge.txt file not found in reprt folder >')
            return
        calnum1 = self.pdffile[0:5]
        file2 = open(filen1, 'w')
        newstr1 = 'c | ' +  self.pdffile  + ' | ' + self.calctitle
        for itm1 in mergelist:
            if calnum1 in itm1:
                indx1 = mergelist2.index(itm1)
                mergelist2[indx1] = newstr1
                for j1 in mergelist2: file2.write(j1)
                file2.close()
                return
        mergelist2.append("\n" + newstr1)
        for j1 in mergelist2: file2.write(j1)
        file2.close()
        return

