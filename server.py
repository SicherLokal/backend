from flask import Flask, request, make_response
import json
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None, max_age=21600,
                attach_to_all=True, automatic_options=True):
    """Decorator function that allows crossdomain requests.
      Courtesy of
      https://blog.skyred.fi/articles/better-crossdomain-snippet-for-flask.html
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        """ Determines which methods are allowed
        """
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        """The decorator function
        """
        def wrapped_function(*args, **kwargs):
            """Caries out the actual cross domain code
            """
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


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
@crossdomain(origin='*')
def get_warenkorb_of_user(uid):
    resp = app.make_default_options_response()
    resp.headers["Access-Control-Allow-Origin"] = "*"
    if(warenkorb.get(uid, None) != None):
        return ",".join(map(str,warenkorb[uid].values()))
    else:
        return "Invalid uid"


@app.route('/add/<string:uid>', methods=['POST'])
@crossdomain(origin='*')
def add_to_warenkorb_of_user(uid):
    if(warenkorb.get(uid, None) == None):
        warenkorb[uid] = dict()
    products = json.loads(request.form["json_of_products"])
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
@crossdomain(origin='*')
def remove_from_warenkorb_of_user(uid):
    if(warenkorb.get(uid, None) == None):
        return "Invalid uid"
    products = json.loads(request.form["json_of_products"])
    # [{"id": "1","name": "Toilettenpapier", "amount": 2020}]
    for produkt_dict in products:
        warenkorb[uid][produkt_dict["id"]].amount -= produkt_dict["amount"]
    return "success."

if __name__ == '__main__':
    app.run()
