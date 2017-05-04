"""Run script from model folder as command line program.
    Zips the database folders for uploading to cloud database. 
    usage: python -m once -s dbzip.py
    
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
            print(path1)
            for file in files:
                ziph.write(os.path.join(basename1, file))
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
    
if __name__ == "__main__":
    run()
    