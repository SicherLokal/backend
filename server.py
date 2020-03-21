from flask import Flask, request
import json


app = Flask(__name__)

class Produkt:
    def __init__(self, id, name, amount):
        self.id = id
        self.name = name
        self.amount = amount

    def __str__(self):
        return self.name+"("+str(self.amount)+" mal)"
    def __repr__(self):
        return self.__str__()


warenkorb = {"username":{"1":Produkt("1","Toilettenpapier",3)}}


@app.route('/warenkorb/<string:uid>', methods=['GET'])
def get_warenkorb_of_user(uid):
    if(warenkorb.get(uid, None) != None):
        return ",".join(map(str,warenkorb[uid].values()))
    else:
        return "Invalid uid"


@app.route('/add/<string:uid>', methods=['POST'])
def add_to_warenkorb_of_user(uid):
    if(warenkorb.get(uid, None) == None):
        warenkorb[uid] = dict()
    products = json.loads(request.form["json_of_produts"])
    # [{"id": "1","name": "Toilettenpapier", "amount": 2020}]
    for produkt_dict in products:
        if warenkorb[uid].get(produkt_dict["id"], None) == None:
            warenkorb[uid][produkt_dict["id"]] = Produkt(produkt_dict["id"],
                                                         produkt_dict["name"],
                                                         produkt_dict["amount"])
        else:
            warenkorb[uid][produkt_dict["id"]].amount += produkt_dict["amount"]

    return "success."


@app.route('/substract/<string:uid>', methods=['POST'])
def remove_from_warenkorb_of_user(uid):
    if(warenkorb.get(uid, None) == None):
        return "Invalid uid"
    products = json.loads(request.form["json_of_produts"])
    # [{"id": "1","name": "Toilettenpapier", "amount": 2020}]
    for produkt_dict in products:
        warenkorb[uid][produkt_dict["id"]].amount -= produkt_dict["amount"]
    return "success."

if __name__ == '__main__':
    app.run()
