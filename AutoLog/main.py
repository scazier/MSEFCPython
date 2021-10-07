from classApacheLog import apacheLog
from classKernLog import kernLog


print("TEST=============CLASS APACHE")
print("TEST=apachelog.testlog()")
print(apacheLog("AutoLog/logFiles/apache.log").testLog())
print(apacheLog("AutoLog/logFiles/apache.log").parseLog())

print("TEST=============CLASS KERNEL")
print("TEST=kernlog.testlog()")
print(kernLog("AutoLog\logFiles\kern.log").testLog())
print(kernLog("AutoLog/logFiles/kern.log").getContent())
