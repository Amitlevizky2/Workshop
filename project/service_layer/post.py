import subprocess
import sys





def method_name(paydtls):
    import requests
    x={}

    for i in range(1,len(paydtls),2):

        x[paydtls[i].replace(':','').replace('{','')]=paydtls[i+1].replace(',','')

    rpay = requests.post("https://cs-bgu-wsep.herokuapp.com/", data=x, timeout=5)
    print(rpay.content)

method_name(sys.argv)


