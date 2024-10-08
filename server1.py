from flask import Flask
import os, psutil
import socket

app = Flask(__name__)
@app.route("/")

def hello():
    html = "<h3>You are logged into {name}!</h3> <b>Hostname:</b> {hostname} <br/> <b>Load on {name}:</b> {loadpercent} <br/>"
    return html.format(name=os.getenv("NAME", "Server1"), hostname=socket.gethostname(), loadpercent = load() )


@app.route("/load")
def load():
    load = psutil.cpu_percent()
    return str(load)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
