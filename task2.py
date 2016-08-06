import zipfile
import re
import json
import sys
import os.path
import getopt
from operator import itemgetter

class Task2:
    def __init__(self, aWarnIsOn=False):
        # compile regexp
        self.mUuid = re.compile('^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$', re.I)
        self.mGuids = []
        self.mOther = []
        self.mWarnIsOn = aWarnIsOn

    def unzip(self, aPathIn: str) -> bool:
        if not os.path.isfile(aPathIn):
            print("ERR: file not exist")
            return False

        if not zipfile.is_zipfile(aPathIn):
            print("ERR: file not zip")
            return False

        with zipfile.ZipFile(aPathIn) as z:
            for info in z.infolist():
                if info.internal_attr == 0:  # check is file
                    if self.mWarnIsOn: print("WRN: ignore folder", info.filename)
                    continue

                part = info.filename.split('/') # check structure folder/file
                if len(part) != 2:
                    if self.mWarnIsOn: print ("WRN; ignore file 1", info.filename)
                    continue

                if part[1] != 'data.json': # use only data.json
                    if self.mWarnIsOn: print ("WRN: ignore file 2", info.filename)
                    continue
        
                with z.open(info.filename) as file:
                    dt = file.read().decode('utf-8')
                    try:
                        js = json.loads(dt)
                    except json.decoder.JSONDecodeError:
                        print ("ERR: decode JSON failed in", info.filename)
                        return False;
                    
                    if self.mUuid.match(part[0]): #detect guid
                        self.mGuids.append( (part[0], js["value"], js["str"]) )
                    else:
                        self.mOther.append( (part[0], js["value"], js["str"]) )

        return True


    def sort(self):
        self.mGuids.sort(key=itemgetter(1, 2))
        self.mOther.sort(key=itemgetter(0))


    def zip(self, aPathOut: str): #TODO : check valid path
        guids = list(map(lambda t: ';'.join(map(str, t)), self.mGuids))
        other = list(map(lambda t: ';'.join(map(str, t)), self.mOther))
        with zipfile.ZipFile(aPathOut, 'w') as z:
            z.writestr('guids.csv', '\n'.join(guids))
            z.writestr('others.csv','\n'.join(other))


def main():
    ifile='task2.zip'
    ofile='task2_out.zip'
    warn = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],'i:o:w')
    except getopt.GetoptError:
        print("Usage: %s -i input -o output [-w]" % sys.argv[0])
        sys.exit()

    for o, a in opts:
        if o == '-i':
            ifile=a
        elif o == '-o':
            ofile=a
        elif o == '-w':
            warn=True
        else:
            print("Usage: %s -i input -o output [-w]" % sys.argv[0])

    longest = max(len(word) for word in sys.argv)
    print ('%-*s=> %5s' % (longest+1, ifile, ofile))

    zz = Task2(warn)
    if zz.unzip(ifile):
        zz.sort()
        zz.zip(ofile)

if __name__ == "__main__":
    main()