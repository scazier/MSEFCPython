import string

def foo(filename):
    dic = {}
    #a = App()


    for letter in string.printable:
        dic[letter] = 0


    with open(filename,"r") as sourcefile, open("/".join(filename.split('/')[:-1])+"-stat.txt", "w") as statfile:
        for ligne in sourcefile:
            for letter in ligne:
                dic[letter] += 1
    return dic



