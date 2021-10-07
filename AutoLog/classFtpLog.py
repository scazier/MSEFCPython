from classLog import Log

struct = {
    "test"  : "FileZilla",
    "header":["Unknown","Date","Time","User","IP","Command"],
    "regex" : '^(\([0-9]{1,100}\))\s([0-9]{2}/[0-9]{2}/[0-9]{4})\s([0-9]{2}:[0-9]{2}:[0-9]{2})\s-\s([A-Za-z]+|\(not\slogged\sin+\))\s\(([0-9]{1,3}[\.][0-9]{1,3}[\.][0-9]{1,3}[\.][0-9]{1,3})\)>(.+)'
}

class ftpLog(Log):
    def __init__(self, filename):
        Log.__init__(self,filename, struct)
        if self.testLog():
            self.parseLog()
        else:
            pass




print(ftpLog("/home/m0xy/Documents/MSEFC/Regex/Exercice_regex/log.txt").getHeader())
