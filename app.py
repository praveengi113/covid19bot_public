from threading import Thread, Event
from statusInd import Status
from datetime import datetime
from pytz import timezone


def covidBot():
    time = datetime.now(timezone('Asia/Kolkata'))
    time = time.strftime("%d/%m/%Y %H:%M:%S")
    status = Status()
    status_now = status.scraper()
    statusCheck = status.status_check()

    console_log = " Time : {0} \n Old Record : {1} \n New Record : {2}".format(time, status.status_old(),
                                                                               status.scraper())

    body = """Hi, This is COVID-19@IndBot
    This is a simple bot to notify about
    the COVID19 cases in India.
    _Created By: Praveen_
    *Data Source: MoHFW*
   
    *Status*
    Status on = {0}
    Confirmed cases = {1}
    Cured cases = {2}
    Total Deaths = {3}

    _Be safe at home..._
    _Save Humanity..._
    """
    mess = body.format(time, status_now[0], status_now[1], status_now[2])
    if statusCheck:
        status.save_to_file()
        print(console_log)
        status.whatsapp(mess)
    else:
        print("{} --->  No Change".format(time))


class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(1800):
            covidBot()


covidBot()
stopFlag = Event()
thread = MyThread(stopFlag)
thread.start()
