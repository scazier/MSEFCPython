from classApacheLog import apacheLog


print("TEST=============CLASS APACHE")
print("TEST=apachelog.testlog()")
print(apacheLog("AutoLog/logFiles/apache.log").testLog())
print(apacheLog("AutoLog/logFiles/apache.log").parseLog())
