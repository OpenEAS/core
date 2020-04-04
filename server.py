from flask import Flask, request, render_template, Markup
from datetime import datetime

def time():
    return datetime.now().strftime("%H:%M:%S %m/%d/%Y")

alerts = []

app = Flask(__name__)

@app.route("/report", methods=["POST"])
def route_report():
    id = str(request.form["id"])
    message = str(request.form["message"])
    alerts.append([id, message, time()])

    return "OK"


@app.route("/", methods=["GET"])
def route_index():
    _alerts = ""
    for alert in alerts[::]:
        _alerts += """
        <div class="pre">""" + alert[1] + """
        </div>
        <small class="text-muted">Reported by """ + alert[0] + " at " + alert[2] + """</small>
        <hr>
        """

    return render_template("index.html", server_name="US-OR-SRV-1", alerts=Markup(_alerts))

@app.route("/about", methods=["GET"])
def route_about():
    return render_template("about.html")
    
app.run("0.0.0.0", port=5000, debug=True)
