from flask import Flask, request
import re

app = Flask(__name__)

class Store:
    def __init__(self):
        self.__data = []
        self.alias = {'lzj1':'00E0701B7792'}

    def delete(self,data):
        if data in self.__data:
            self.__data.remove(data)

    def add(self, data):
        if data not in self.__data:
            self.__data.append(data)

    def get(self):
        return self.__data

def isMac(str):
    r = re.match("[A-Fa-f0-9]{12}",str)
    if r:
        return True
    return False

store = Store()

@app.route("/wake/alias/<name>")
def wake_name(name):
    add = store.alias.get(name)
    if add:
        wake(add)
        return 'OK'
    return 'name not exists'

@app.route("/wake/<address>")
def wake(address):
    if len(address) == 12:
        store.add(address)
        return "ok"
    return "len is not 12"  	

@app.route("/delete/<address>")
def delete(address):
    store.delete(address)
    return "delete:"+address

@app.route("/")
@app.route("/<address>", methods=['GET','DELETE', 'PUT'])
def get_wake_list(address=None):
    if request.method == 'GET':
        data = store.get()
        result = ""
        for mac in data:
            result += mac + "\n"
        return result

    if not isMac(address):
        return 'fail'

    if request.method == 'PUT':
        if address is None:
            return 'fail'
        store.add(address)
        return 'OK'

    if request.method == 'DELETE' :
        store.delete(address)
        return 'Del'+address


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
