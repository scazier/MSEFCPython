import re

from Log import Log

struct = {
    "test"  : "FileZilla",
    "header":["Unknown","Date","Time","User","IP","Command"],
    "regex" : '^(\([0-9]{1,100}\))\s([0-9]{2}/[0-9]{2}/[0-9]{4})\s([0-9]{2}:[0-9]{2}:[0-9]{2})\s-\s([A-Za-z]+|\(not\slogged\sin+\))\s\(([0-9]{1,3}[\.][0-9]{1,3}[\.][0-9]{1,3}[\.][0-9]{1,3})\)>(.+)'
}

class FtpLog(Log):
    def __init__(self, filename):
        Log.__init__(self,filename, struct)
        if self.testLog():
            print("ICI")
            self.parseLog()
        else:
            pass

    def testLog(self):
        if re.search(self.struct["regex"],''.join(open(self.filename,'r').readlines()[:10])) is None:
            self.struct["regex"] = '^([A-Za-z]{3})\s([A-Za-z]{3})\s[0-9]{1,2}\s([0-9]{2}:[0-9]{2}:[0-9]{2})\s[0-9]{4}\s(\[.+\])(|\[.+\])\s([A-Z]+.+):\s(.+)\"(::.+:.+)\"'
            self.header = ["Day","Month","Number","Date","Year","PID","user","info"]
        return True




#print(ftpLog("/home/m0xy/Documents/MSEFC/Regex/Exercice_regex/test.txt").getContent())
