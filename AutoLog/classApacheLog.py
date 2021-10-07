from classLog import Log


struct = {
    "test": "Apache",
    "header": ["ip", "date", "time", "method",
               "target", "protocole_version", "code", "rest"],
    "regex": '^([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\s-\s-\s\[([0-9]{1,2}\/[A-Za-z]{1,5}\/[0-9]{1,4}):([0-9]{2}:[0-9]{2}:[0-9]{2})\s\+[0-9]{1,9}\]\s\"([A-Z]{1,10})(.+\")\s([0-9]{3})\s([0-9]+)\s\"(.+)\"\s\"(.+)\"'
}


class apacheLog(Log):
    def __init__(self, filename):
        Log.__init__(self, filename, struct)
        if self.testLog():
            self.parseLog()
        else:
            pass


print(apacheLog("AutoLog/logFiles/apache.log").testLog())
