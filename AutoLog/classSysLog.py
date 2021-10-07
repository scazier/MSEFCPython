from classLog import Log

struct = {
    "test"  : "syslog",
    "header":["Month","Day","Time","User","Daemon","Info"],
    "regex" : '([A-Z][a-z]{2})\s+([0-9]{1,2})\s([0-9]{2}:[0-9]{2}:[0-9]{2})\s(.+|\(not\slogged\sin+\))\s(.+\[[0-9]+\]):\s(.+)'
}

class sysLog(Log):
    def __init__(self, filename):
        Log.__init__(self,filename, struct)
        if self.testLog():
            print(self.testLog())
            self.parseLog()
        else:
            print(self.testLog())
            pass




print(sysLog("/var/log/syslog.1").getContent())

#([A-Z][a-z]{2})\s+([0-9]{1,2})\s([0-9]{2}:[0-9]{2}:[0-9]{2})\s([A-Za-z]+|\(not\slogged\sin+\))\s(.+\[[0-9]+\]):\s(.+)
