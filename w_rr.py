from flask import Flask, request
import requests
import os
import socket
import sys, psutil
import random

app = Flask(__name__)

w=[0]*2
s=[1,2]
count=0

ipaddr_Srv1 = "20.234.120.66"
ipaddr_Srv2 = "23.102.46.168"

@app.route("/")

def hello():
    html = "<h3> You are being redirected by {name}, Stay Tuned </h3> <b> Hostname:</b> {hostname} <br/>"
    return html.format( name=os.getenv("NAME", "WeightedRoundRobin"), hostname=socket.gethostname() )

@app.route('/wrr')

def wrr():

    global random_srv, count, s

    random_srv = random.choice(s)
    result = wrr_alg(random_srv)
    count = count + 1

    if count==10:
        count = 0
    return result

def wrr_alg(random_srv):

    global w

    if random_srv == 1:
        getserver(random_srv)

        if sum(w) < 10:
            if w[0] < 7:
                w[0] = w[0] + 1
                response = getresponse(ipaddr_Srv1)
            else:
                equalw(random_srv)
                w[0] = 0
                w[1] = w[1] + 1
                response = getresponse(ipaddr_Srv2)
        else:
            getlimit(random_srv)
            w[0] = 1
            response = getresponse(ipaddr_Srv1)

    elif random_srv == 2:
        getserver(random_srv)

        if sum(w) < 10:
            if w[1] < 3:
                w[1] = w[1] + 1
                response = getresponse(ipaddr_Srv2)
            else:
                equalw(random_srv)
                w[1] = 0
                w[0] = w[0] + 1
                response = getresponse(ipaddr_Srv1)
        else:
            getlimit(random_srv)
            w[1] = 1
            response = getresponse(ipaddr_Srv2)
    else:
        response = geterror()

    return response

def getload(ipaddr):
    global load_srv
    load_srv = requests.get("http://{}:8080/load".format(ipaddr)).content
    return float(load_srv)

def getresponse(ipaddr):
    global srv_response
    srv_response = requests.get("http://{}:8080/".format(ipaddr)).content
    return srv_response

def getserver(val):

    if val == 1:
        html = "<h3> You are being redirected to {name}, Stay Tuned </h3>"
        return html.format( name="Server 1")
    if val == 2:
        html = "<h3> You are being redirected to {name}, Stay Tuned </h3>"
        return html.format( name="Server 2")

def geterror():
    html = "<h3> Invalid Choice, Please, Reload </h3>"
    return html

def equalw(val):

    if val == 1:
        html = "<h3> {name1} full, Redirecting request through {name2} </h3>"
        return html.format( name1="Server 1", name2="Server 2" )
    if val == 2:
        html = "<h3> {name1} full, Redirecting request through {name2} </h3>"
        return html.format( name1="Server 2", name2="Server 1" )

def getlimit(val):

    if val == 1:
        html = "<h3> Both servers full, Redirecting request through {name1} </h3>"
        return html.format( name1="Server 1" )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
