import re

class Log:
    def __init__(self, filename, struct):
        self.filename = filename
        self.struct = struct
        self.header = self.struct["header"]
        self.content = []

    def testLog(self):
        # Verification de log
        with open(self.filename,'r') as log:
            return re.match(self.struct['regex'], ''.join(log.readlines()[:10]))


    def parseLog(self):
        with open(self.filename,'r') as log:
            for line in log:
                match = re.search(self.struct["regex"], line)
                if match:
                    self.content.append(list(match.groups()))

    def getHeader(self):
        return self.header

    def getContent(self):
        return self.content
