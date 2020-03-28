from datetime import datetime
import uuid
import json
import requests
from bs4 import BeautifulSoup
from pytz import timezone
from twilio.rest import Client


class Status(object):
    def __init__(self, id=None, date=datetime.now(timezone('Asia/Kolkata'))):
        self.cases = self.scraper()[0]
        self.cured = self.scraper()[1]
        self.death = self.scraper()[2]
        self.id = uuid.uuid4().hex if id is None else id
        self.time = date.strftime("%d/%m/%Y %H:%M:%S")

    def save_to_file(self):
        with open("src/data.json") as f:
            data = json.load(f)
            temp = data['status']
            temp.append(self.json_upd)
        self.write_json(data)

    def write_json(self, data, filename='src/data.json'):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @property
    def json_upd(self):
        return {
            "cases": self.cases,
            "cured": self.cured,
            "death": self.death,
            "id": self.id,
            "time": self.time
        }

    def status_old(self):
        temp_list = []
        with open("src/data.json") as f:
            data = json.load(f)
            temp = data['status']
        for te in temp[-1]:
            temp_list.append(temp[-1][te])
            
        return temp_list

    def status_check(self):
        temp = self.status_old()
        if int(temp[0]) == int(self.scraper()[0]):
            return False
        elif int(temp[1]) == int(self.scraper()[1]):
            return False
        elif str(temp[2]) == str(self.scraper()[2]):
            return False
        else:
            return True

    def scraper(self):
        url = "https://www.mohfw.gov.in/"
        request = requests.get(url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        elements = soup.findAll("span", {"class": "icount"})
        status_var = []
        for e in elements[1:]:
            el = e.text.strip()
            status_var.append(el)
        return status_var

    def whatsapp(self, body):
        sid = "YOUR_ACC-SID"
        token = "YOUR_ACC_TOKEN"

        client = Client(sid, token)
        fr_num = "whatsapp:+14155238886"
        to_num = "whatsapp:" + YOUR_NUMBER
        client.messages.create(body=body, from_=fr_num, to=to_num)
        
