


class metaLog(object):
    regex = '([(\d\.)]+) - - \[(.*?)\] "(.*?)" (\d+) - "(.*?)" "(.*?)"'
    dic_fields = {"ip", "date", "time", "methode",
                  "target", "protocole_version", "code", "rest"}
    

    def __init__(self,filename):
        # Initialize the parser
        print('metaLog initialized')

    def parse(filename):
        #Read the file and construct the object list
        pass

    def test(filename):
        #test if the first line of filename match the regex
        return True #or false




