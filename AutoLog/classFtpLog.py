import re

struct = {
    "sep":' ',
    "header":["Unknown","Date","Time","User","IP","Command"]
}

class ftpLog:
    def __init__(self, filename):
        self.filename = filename
        if self.testLog():
            self.parseLog()
        else:
            pass

    def testLog(self):
        # Verification de log FTP
        return True if re.match("FileZilla",'\n'.join(open(self.filename,'r').readlines()[:10])) != None else False



    def parseLog(self):
        self.headers = struct
        self.content = []

        with open(self.filename,'r') as log:
            for line in log:
                match = re.search('^(\([0-9]{1,100}\))\s([0-9]{2}/[0-9]{2}/[0-9]{4})\s([0-9]{2}:[0-9]{2}:[0-9]{2})\s-\s([A-Za-z]+|\(not\slogged\sin+\))\s\(([0-9]{1,3}[\.][0-9]{1,3}[\.][0-9]{1,3}[\.][0-9]{1,3})\)>(.+)',line)
                if match:
                    self.content.append(match.groups())




ftpLog("/home/m0xy/Documents/MSEFC/Regex/Exercice_regex/log.txt")
