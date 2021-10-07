import re

class Log:
    def __init__(self, filename, struct):
        self.filename = filename
        self.struct = struct
        self.headers = self.struct["header"]
        self.content = []

    def testLog(self):
        # Verification de log
        return False if re.search(self.struct["test"],'\n'.join(open(self.filename,'r').readlines()[:10])) is None else True


    def parseLog(self):
        with open(self.filename,'r') as log:
            for line in log:
                match = re.search(self.struct["regex"], line)
                if match:
                    self.content.append(list(match.groups()))

    def getHeader(self):
        return self.headers

    def getContent(self):
        return self.content
