
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
        if rpay == -1:
            return "The transaction was declined"
        return rpay

    def cancelpay(self,r):
        canceldtl = {'action_type': 'cancel_pay','transaction_id':r}
        rcancle = requests.post(self.url,data= canceldtl)
        if rcancle == -1:
            return "The transaction was declined"
        elif rcancle ==1:
            return rcancle

    def supply(self,name,address,city,country,zip):
        supplydtls = {'action_type': 'supply', 'name': name
                      ,'address':address,'city':city
                      ,'country':country,'zip':zip}
        rsupply = requests.post(self.url,data= supplydtls)
        if rsupply == -1:
            return "The shipment was declined"
        return rsupply

    def cancelsupply(self,rsupply):
        cancelsupplydtl = {'action_type': 'cancel_supply','transaction_id':rsupply}
        rcanclesupply = requests.post(self.url,data= cancelsupplydtl)
        if rcanclesupply == -1:
            return "The shipment was declined"
        return rcanclesupply



