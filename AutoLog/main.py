from Log import Log


class logAnalysis:
    def __init__(self, filename):
        self.logType(filename)

    def logType(self, filename):
        self.file = Log(filename)
        if not self.file.testLog():
            return -1
        """
        print(apacheLog(filename).testLog())
        if apacheLog(filename).testLog():
            self.file = apacheLog(filename)
        elif ftplog(filename).testLog():
            self.file = ftpLog(filename)
        elif sysLog(filename).testLog():
            self.file = sysLog(filename)
        elif kernLog(filename).testLog():
            self.file = kernLog(filename)
        else:
            return -1
        """

    def parseLog(self):
        return self.file.parseLog()

def main():
    print("Start log analysis...")
    print(logAnalysis("AutoLog/logFiles/kern.log").parseLog())


if __name__=='__main__':
    main()
