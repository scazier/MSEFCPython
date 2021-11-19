import re


class Log:
    def __init__(self, filename):
        self.filename = filename
        #self.struct = struct
        #self.header = self.struct["header"]
        self.content = []

    """
    def testLog(self):
        # Verification de log
        with open(self.filename,'r') as log:
            return bool(re.match(self.struct['regex'], ''.join(log.readlines()[:10])))
    """
    def testLog(self):
        found = 0
        with open('AutoLog/struct.conf','r') as struct:
            for conf in struct:
                conf = conf.split(';')
                with open(self.filename,'r') as log:
                    isCorrectStruct = bool(re.match(conf[2], ''.join([log.readline() for i in range(10)])))
                    if isCorrectStruct:
                        self.type   = conf[0]
                        self.header = conf[1].split(',')
                        self.regex  = conf[2]
                        found = 1
        return found

    """
    def parseLog(self):
        with open(self.filename,'r') as log:
            for line in log:
                match = re.search(self.struct["regex"], line)
                if match:
                    self.content.append(list(match.groups()))
        return self.content
    """
    def parseLog(self):
        with open(self.filename,'r') as log:
            for line in log:
                match = re.search(self.regex, line)
                if match:
                    self.content.append(list(match.groups()))
        return self.content

    def filter(self, pattern, field):
        filtered = []
        for line in self.content:
            if re.match(pattern, line[field]):
                filtered.append(line)
                # Add in Qt5 dataframe

    def getHeader(self):
        return self.header

    def getContent(self):
        return self.content
