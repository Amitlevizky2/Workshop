
import requests
import unittest

import transaction


class ExternalServiceAPI:


    def connect(self):
        handsheke = {"action_type": "handshake"}
        r = requests.post("https://cs-bgu-wsep.herokuapp.com/", data=handsheke)
        self.url = "https://cs-bgu-wsep.herokuapp.com/"

    def pay(self,number,month,year,holder,ccv,id):
        paydtls ={'action_type': 'pay', "card_number": number
            ,"month": month, 'year':year, 'holder': holder
            ,'ccv': ccv, 'id': id}
        rpay = requests.post("https://cs-bgu-wsep.herokuapp.com/",data = paydtls,timeout=5)
        if int(rpay.content) == -1:
            return "The transaction was declined"
        return int(rpay.content)

    def cancelpay(self,r):
        canceldtl = {'action_type': 'cancel_pay','transaction_id':r}
        rcancle = requests.post("https://cs-bgu-wsep.herokuapp.com/",data= canceldtl)
        if int(rcancle.content) == -1:
            return "The transaction was declined"
        elif int(rcancle.content) == 1:
            return int(rcancle.content)

    def supply(self,name,address,city,country,zip):
        supplydtls = {'action_type': 'supply', 'name': name
                      ,'address':address,'city':city
                      ,'country':country,'zip':zip}
        rsupply = requests.post("https://cs-bgu-wsep.herokuapp.com/",data= supplydtls)
        if int(rsupply.content) == -1:
            return "The shipment was declined"
        return int(rsupply.content)

    def cancelsupply(self,rsupply):
        cancelsupplydtl = {'action_type': 'cancel_supply','transaction_id':rsupply}
        rcanclesupply = requests.post("https://cs-bgu-wsep.herokuapp.com/",data= cancelsupplydtl)
        if int(rcanclesupply.content) == -1:
            return "The shipment was declined"
        return int(rcanclesupply.content)



