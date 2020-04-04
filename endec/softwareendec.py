# serialendec.py
#
# OpenEAS software ENDEC driver
#
# Author: Nate Sales

import feedparser
import serial
import requests

class SoftwareEndec:
    def __init__(self, id, server, cap_server="https://alerts.weather.gov/cap/or.php?x=0"):
        self.id = str(id)
        self.server = server.strip("/")
        self.cap_server = cap_server

        self.alert_ids = []

        print("Verifying connectivity to CAP server...", end="", flush=True)

        try:
            r = requests.get(self.cap_server)
        except requests.exceptions.ConnectionError as e:
            print("ERROR")
            print(e)
        else:
            print("SUCCESS")

            print("Verifying CAP format...................", end="", flush=True)
            if r.status_code == 200:
                if r.text.split("<id>")[1].split("</id>")[0] == cap_server:
                    print("SUCCESS")
                    print("Recieved CAP data in " + str(round(r.elapsed.total_seconds(), 2)) + " seconds.")
                else:
                    print("FAIL")
                    print("Error detecting CAP data.")
            else:
                print("FAIL")
                print("Invalid HTTP status code. Server reported " + str(r.status_code))


    def monitor(self):
        feed = feedparser.parse(self.cap_server)

        for entry in feed["items"]:
            try:
                title = entry["title"]
                summary = entry["summary"]
                id = entry["id"]

                # Time data
                published = entry["published"]
                updated = entry["updated"]
                effective = entry["cap_effective"]
                expires = entry["cap_expires"]

                # CAP Data
                event = entry["cap_event"]
                urgency = entry["cap_urgency"]
                severity = entry["cap_severity"]
                certainty = entry["cap_certainty"]
                area = entry["cap_areadesc"]

                value = entry["value"]

                raw = title + "\n"
                for x in summary.split(" * "):
                    raw += x + "\n"
                raw += value

                mini = event + "\n"
                mini += "Effective " + effective + "\n"
                mini += "Urgency: " + urgency + "\n"
                mini += "Severity: " + severity + "\n"
                mini += "Certainty: " + certainty + "\n"
                mini += "Area: " + area
            except KeyError:
                pass
            else:
                if not id in self.alert_ids:
                    requests.post(self.server + "/report", data={"id": self.id, "message": raw})
                    self.alert_ids.append(id)
