from django.db.models import F
from schedule import Scheduler
import threading
import time
from . import server
from .config import config
from .models import ServerPing, ServerStatistic
import datetime

def controllServerFromAllocations():   
    desiredServerState = server.get_serverAllocation(server.now()).exists()
    if server.ping(config["serverIp"]) == desiredServerState:
        return
    
    if not config["controllServer"] :
        return

    if desiredServerState:
        print("attempting server start.")
    else:
        print("attempting server shutdown.")
    try:
         result = server.controllServer(desiredServerState)
    except server.alreadyOff:
        print("already OFF")
        return
    except server.alreadyOn:
        print("already ON")
        return
    except server.alreadyStarting:
        print("already starting")
        return
    print("success") if result else print("failure")
    # turns the server on if it should be on and off if it should be off

def getPingOnPercent(hoursAgo:int):
    beginTime = server.now() - datetime.timedelta(hours=hoursAgo)
    endTime = server.now() - datetime.timedelta(hours=hoursAgo-1)
    pings = list(ServerPing.objects.filter(timestamp__gte = beginTime, timestamp__lt = endTime).all())
    if not pings: return 0
    
    sum = 0
    for ping in pings:
        sum += int(ping.successful)
    percent = sum * 100 / len(pings)
    return int(percent)

def createDayStatistic():
    hourlyPercent = [None] * 24
    for i in range(24):
        hourlyPercent[i] = getPingOnPercent(24-i)
    # as this function is called everyday at 00:00 and calculate the statistic the day prior, it will substract 1 day to save the statistic in the db
    date = server.now().date() - datetime.timedelta(days=1)
    ServerStatistic.objects.create(
        date=date,
        h_00=hourlyPercent[0],
        h_01=hourlyPercent[1],
        h_02=hourlyPercent[2],
        h_03=hourlyPercent[3],
        h_04=hourlyPercent[4],
        h_05=hourlyPercent[5],
        h_06=hourlyPercent[6],
        h_07=hourlyPercent[7],
        h_08=hourlyPercent[8],
        h_09=hourlyPercent[9],
        h_10=hourlyPercent[10],
        h_11=hourlyPercent[11],
        h_12=hourlyPercent[12],
        h_13=hourlyPercent[13],
        h_14=hourlyPercent[14],
        h_15=hourlyPercent[15],
        h_16=hourlyPercent[16],
        h_17=hourlyPercent[17],
        h_18=hourlyPercent[18],
        h_19=hourlyPercent[19],
        h_20=hourlyPercent[20],
        h_21=hourlyPercent[21],
        h_22=hourlyPercent[22],
        h_23=hourlyPercent[23],
    )
    
def dbCleanup():
    ServerPing.objects.filter(timestamp__lt = server.now() - datetime.timedelta(days=7)).all().delete()
        

def run_continuously(self, interval=1):
    """Continuously run, while executing pending jobs at each elapsed
    time interval.
    @return cease_continuous_run: threading.Event which can be set to
    cease continuous run.
    Please note that it is *intended behavior that run_continuously()
    does not run missed jobs*. For example, if you've registered a job
    that should run every minute and you set a continuous run interval
    of one hour then your job won't be run 60 times at each interval but
    only once.
    """

    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):

        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                self.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.setDaemon(True)
    continuous_thread.start()
    return cease_continuous_run

Scheduler.run_continuously = run_continuously

def start_scheduler():
    scheduler = Scheduler()
    scheduler.every(config["Interval"]).seconds.do(controllServerFromAllocations)
    scheduler.every().day.at("00:00").do(createDayStatistic)
    scheduler.every().day.at("00:00").do(dbCleanup)
    scheduler.run_continuously()