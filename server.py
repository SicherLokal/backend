from flask import Flask
import json

app = Flask(__name__)


class Produkt:
    def __init__(self, id, name, amount):
        self.id = id
        self.name = name
        self.amount = amount

    def __str__(self):
        return self.name+"("+self.amount+" mal)"


warenkorb = dict()


@app.route('/warenkorb/<string:uid>', methods=['GET'])
def get_warenkorb_of_user(uid):
    if(warenkorb.get(uid, None) != None):
        return ",".join(map(str, warenkorb[uid]))
    else:
        return "Invalid uid"


@app.route('/add/<string:uid>', methods=['POST'])
def add_to_warenkorb_of_user(uid):
    if(warenkorb.get(uid, None) != None):
        warenkorb[uid] = []
    products = json.loads(request.form["json_of_produts"])
    # [{"id": "1","name": "Toilettenpapier", "amount": "2020"}]
    for produkt_dict in products:
        warenkorb[uid].append(
            Produkt(produkt_dict["id"],
                    produkt_dict["name"],
                    produkt_dict["amount"])
        )
    return "success. new cart:" + ",".join(map(str, warenkorb[uid]))

@app.route('/substract/<string:uid>', methods=['POST'])
def remove_from_warenkorb_of_user(uid):
    if(warenkorb.get(uid, None) != None):
        return "Invalid uid"
    products = json.loads(request.form["json_of_produts"])
    # [{"id": "1","name": "Toilettenpapier", "amount": "2020"}]
    for produkt_dict in products:
        for content in warenkorb[uid]:
            if produkt_dict["id"] == content.id:
                content.amount = min(content.amount-produkt_dict["amount"],0)                    


if __name__ == '__main__':
    app.run()
