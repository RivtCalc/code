"""Run script from the model folder.
    Program zips database folders for uploading to cloud database.
    usage: python -m once -s dbzip.py
    outputs two files to project folder:
        date_projectfolder.zip includes db folders and files except pdf calcs
        date_projectfolder.zip includes dbcalc folder with only pdf calcs
   """
import os
import zipfile
import datetime


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        path1 = root.replace('/','\\')
        basename1 = path1.split('\\')[-1]
        if basename1.startswith('db'):
            #print(path1)
            for file1 in files:
                #print('file', file1)
                if not str(file1).endswith('.pdf'):
                    ziph.write(os.path.join(basename1, file1))
        else:
            continue

def zipdir2(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        path1 = root.replace('/','\\')
        basename1 = path1.split('\\')[-1]
        if basename1.startswith('db'):
            #print(path1)
            for file1 in files:
                if str(file1).endswith('.pdf'):
                    ziph.write(os.path.join(basename1, file1))
        else:
            continue

def run():
    # Get project folder and zip file name
    cwd1 = os.getcwd()                  
    os.chdir("..")
    proj_root = os.getcwd()
    print('< project folder: ' + proj_root +' >')
    
    _basename =  os.path.basename(proj_root)
    _dt = datetime.datetime.now()
    _d1 = 'db'+str(_dt.date())
    _d2 = _d1.replace('-','')
    _d3 = _d2 + '_' + _basename + '.zip'    
    zipf = zipfile.ZipFile(_d3, 'w', zipfile.ZIP_DEFLATED)
    zipdir(proj_root, zipf)
    zipf.close()
    print('< database zip file written: ' + _d3 + ' >')


    _d4 = _d2 + '_' + _basename + '_pdf.zip'
    zipf = zipfile.ZipFile(_d4, 'w', zipfile.ZIP_DEFLATED)
    zipdir2(proj_root, zipf)
    zipf.close()
    print('< database zip file written: ' + _d4 + ' >')

    
if __name__ == "__main__":
    run()
    