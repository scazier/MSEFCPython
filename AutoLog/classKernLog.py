from classLog import Log

struct = {
    "test"  : "kern",
    "header":["Month","Day","Time","Host","Unknown","Interface","Info"],
    "regex" : '([A-Za-z]{3}) ([ 0-9][0-9]) ([0-9]{2}:[0-9]{2}:[0-9]{2}) ([^:]*:) ?(\[[^ ]*\]) ?(.[^ ]*) ?(.*)'
}

class kernLog(Log):
    def __init__(self, filename):
        Log.__init__(self,filename, struct)
        if self.testLog():
            print(self.testLog())
            self.parseLog()
        else:
            print(self.testLog())
            pass



#([A-Za-z]{3}) ([ 0-9][0-9]) ([0-9]{2}:[0-9]{2}:[0-9]{2}) ([^:]*:) ?(\[[^ ]*\]) ?(.[^ ]*) ?(.*)