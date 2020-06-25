import fnmatch
import os
import pathlib
import subprocess
from datetime import time

import jsons
import requests
import unittest

import transaction

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


class ExternalServiceAPI:

    def connect(self):
        handsheke = {"action_type": "handshake"}
        r = requests.post("https://cs-bgu-wsep.herokuapp.com/", data=handsheke)
        self.url = "https://cs-bgu-wsep.herokuapp.com/"

    def pay(self, number, month, year, holder, ccv, id):
        paydtls = {'action_type': 'pay', "card_number": number
            , "month": month, 'year': year, 'holder': holder
            , 'ccv': ccv, 'id': id}
        print('paydtls')
        print(paydtls)
        path=find('post.py',pathlib.Path(__file__).parent.absolute())[0];
        print('Before Line')
        proc = subprocess.Popen("python "+path+" "+ jsons.dumps(paydtls), stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True)

        rpay = proc.communicate()[0]
        # rpay = requests.post("https://cs-bgu-wsep.herokuapp.com/", data=paydtls, timeout=5)
        print('After Line')
        try:
            rpay =int(str(rpay).replace('b','').replace('\'','').replace('\\r','').replace('\\n','').replace('`','').replace("\"",''))
        except:
            return -1
        if int(rpay) == -1:
            return "The transaction was declined"
        return int(rpay)

    def cancelpay(self, r):
        canceldtl = {'action_type': 'cancel_pay', 'transaction_id': r}

        rcancle = requests.post("https://cs-bgu-wsep.herokuapp.com/", data=canceldtl)
        if int(rcancle.content) == -1:
            return "The transaction was declined"
        elif int(rcancle.content) == 1:
            return int(rcancle.content)

    def supply(self, name, address, city, country, zip):
        supplydtls = {'action_type': 'supply', 'name': name
            , 'address': address, 'city': city
            , 'country': country, 'zip': zip}
        path = find('post.py', pathlib.Path(__file__).parent.absolute())[0];
        print('Before Line')
        proc = subprocess.Popen("python " + path + " " + jsons.dumps(supplydtls), stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=True)

        rsupply = proc.communicate()[0]
        rsupply = int(str(rsupply).replace('b', '').replace('\'', '').replace('\\r', '').replace('\\n', '').replace('`',
                                                                                                                    '').replace(
            "\"", ''))

        #rsupply = requests.post("https://cs-bgu-wsep.herokuapp.com/", data=supplydtls)
        if int(rsupply) == -1:
            return "The shipment was declined"
        return int(rsupply)

    def cancelsupply(self, rsupply):
        cancelsupplydtl = {'action_type': 'cancel_supply', 'transaction_id': rsupply}
        rcanclesupply = requests.post("https://cs-bgu-wsep.herokuapp.com/", data=cancelsupplydtl)
        if int(rcanclesupply.content) == -1:
            return "The shipment was declined"
        return int(rcanclesupply.content)
