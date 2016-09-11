from flask import Flask
from flask import jsonify
from ConfigParser import SafeConfigParser

import csv
import re
import json

class MockWineStore:

    config_file = 'config.ini'

    def __init__(self):
        parser = SafeConfigParser()
        parser.read(MockWineStore.config_file)
        self.not_allowed_states = parser.get('states', 'notAllowedStates').split(', ')
        self.filename = parser.get('files', 'orders')
        self.orders = []
        self.column_dic = {}

    def validate_one(self,order):
        id = order[self.column_dic['id']]
        name = order[self.column_dic['name']]
        email = order[self.column_dic['email']]
        state = order[self.column_dic['state']]
        zipcode = order[self.column_dic['zipcode']]
        birthday = order[self.column_dic['birthday']]
        valid = False
        errors = []
        z_sum = 0

        if state in self.not_allowed_states:
            errors.append({"rule":"AllowedStates", "message": "We don't ship to " + state})

        if not zipcode.isdigit():
            errors.append({"rule":"ZipcodeDigits", "message": "Your zipcode has non-digit"})

        if len(zipcode)!=5 and len(zipcode)!=9:
            errors.append({"rule":"ZipcodeLength", "message": "Your zipcode length is neither 5 or 9"})

        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            errors.append({"rule":"EmailFormat", "message": "Your email is illegal"})

        for d in zipcode:
            z_sum += int(d)

            if z_sum>20:
                errors.append({"rule":"ZipCodeSum", "message": "Your zipcode sum is too large"})
                break

        suffix = email.split('.')[-1].lower()
        if state=='NY' and suffix=='net':
            errors.append({"rule":"NYnoNet", "message": "NY does not allow .net email"})

        if not errors :
            valid = True

        return {"order_id": id,
                "name": name,
                "state": state,
                "zipcode": zipcode,
                "birthday": birthday,
                "valid": valid,
                "errors": errors}

    def validate(self, order, last_order=()):

        id = order[self.column_dic['id']]
        name = order[self.column_dic['name']]
        email = order[self.column_dic['email']]
        state = order[self.column_dic['state']]
        zipcode = order[self.column_dic['zipcode']]
        birthday = order[self.column_dic['birthday']]
	valid = False
        z_sum = 0

        if last_order and last_order[0]==state and last_order[1]==zipcode:
            self.orders.append({"order_id":id,"name":name,"valid":last_order[2]})
            return last_order
            
        if state in self.not_allowed_states:
            self.orders.append({"order_id":id, "name":name, "valid":False})
            return (state,zipcode,False)

        if not zipcode.isdigit():
            self.orders.append({"order_id":id, "name":name, "valid":False})
            return (state,zipcode,False)

        if len(zipcode)!=5 and len(zipcode)!=9:
            self.orders.append({"order_id":id, "name":name, "valid":False})
            return (state,zipcode,False)

        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            self.orders.append({"order_id":id, "name":name, "valid":False})
            return (state,zipcode,False)

        for d in zipcode:
            z_sum += int(d)

            if z_sum>20:
                self.orders.append({"order_id":id, "name":name, "valid":False})
                return (state,zipcode,False)

        suffix = email.split('.')[-1].lower()
        if state=='NY' and suffix=='net':
            self.orders.append({"order_id":id, "name":name, "valid":False})
            return (state,zipcode,False)

        self.orders.append({"order_id":id, "name":name, "valid":True})
        return (state,zipcode,True)

    def import_orders(self):

        with open(self.filename,'r') as f:

            reader = csv.reader(f)
            header = reader.next()[0].split('|')

            for ind, column in enumerate(header):
                self.column_dic[column] = ind

            last_order = ()

            for row in reader:
                order = row[0].split('|')
                last_order = self.validate(order, last_order)
 
    def get_orders(self):
        return self.orders

    def get_order(self, order_id):
        output = None

        with open(self.filename,'r') as f:
            reader = csv.reader(f)
            reader.next()

            for row in reader:
                order = row[0].split('|')
                id = order[self.column_dic['id']]

                if int(id)==(order_id):
                    print id
                    output = self.validate_one(order)

        return output

app = Flask(__name__)
mws = MockWineStore()

@app.route('/orders/import')
def import_orders():
    orders = mws.import_orders()
    return "Imported."

@app.route('/orders')
def get_orders():
    return jsonify({"results": mws.orders})

@app.route('/orders/<int:id>')
def get_order(id):
    order = mws.get_order(id)
    return jsonify(order)

if __name__ == '__main__':
    app.run()

