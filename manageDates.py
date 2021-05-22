from datetime import datetime,date,timedelta  
import time
import pandas as pd
import re
import random

class ManageDates:
    date = ''
    def __init__(self,sdate=None):
        self.format = '%d-%m-%Y %H:%M:%S'
        self.cformat = '%d-%m-%Y'
        self.date = self.setDate(sdate)

    def setDate(self,sdate=None):
        sdate = str(sdate)
        if sdate: 
            if self.isdate(sdate):
                if self.isstd(sdate):
                    return sdate
                return self.mk_std(sdate)
        print(sdate,"is Invalid date so today date is taken")
        return self.mk_std((datetime.today()).strftime(self.format))

    def assignDate(self,sdate=None): #assignDate assign self.date or set given date
        return self.setDate(sdate) if sdate else self.date

    def isstd(self,sdate):
        return re.search(r'^\d{2}\-\d{2}\-\d{4} (:?\d{1,2}){3}$',sdate)

    def isdate(self,sdate):
        return re.search(r'^(\d{1,2}|\d{4})([.\-/]){1}\d{1,2}([.\-/]){1}(\d{1,2}|\d{4}) ?(\d{1,2}:?)*$',sdate)

    def datetimeobj(self,sdate):
        return datetime.strptime(sdate, self.format)

    def mk_std(self,sdate):
        sdate = re.sub(r'[.\-/]', '-', sdate)
        stime = ''
        if len(sdate)<=19 and len(sdate)>=15:
            sdate,stime = sdate.split(' ')
        if len(sdate)<10 and len(sdate)>=6:
            datesplit = sdate.split('-')
            if len(sdate)<=8 and len(sdate)>=6:
                if len(datesplit[-1])==2:
                    datesplit[-1]='20'+datesplit[-1]
                elif len(datesplit[0])==2:
                    datesplit[0]='20'+datesplit[0]
            sdate = '-'.join([d.zfill(2) for d in datesplit])
        if len(sdate)==10:
            sdatesplit = sdate.split('-')
            if len(sdatesplit[0])==4:
                sdatesplit[0],sdatesplit[-1] = sdatesplit[-1],sdatesplit[0]
            sdate = '-'.join(sdatesplit)
        if stime!='':
            sdate += ' '+stime
        else: sdate+= ' 00:00:00'
        return sdate

    def str_time_prop(self,start, end, prop):
        stime = time.mktime(time.strptime(start, self.format))
        etime = time.mktime(time.strptime(end, self.format))
        ptime = stime + prop * (etime - stime)
        return time.strftime(self.format, time.localtime(ptime))
 
    def random_date(self,start=None,end=None):
        start = self.assignDate(start) #assign given date or self date
        end = self.setDate(end) #set given date or today date
        return self.str_time_prop(start, end ,random.random())
    
    def addhours(self,sdate=None,hours=0, rand_hr=1):
        sdate = self.datetimeobj(self.assignDate(sdate))
        slimit = 9 if int(sdate.strftime('%H'))<9 else 0  # statr by 9 AM
        slimit += hours
        startdate = sdate + timedelta(hours=slimit)
        enddate = sdate + timedelta(hours=slimit+rand_hr)
        return self.random_date(self.setDate(startdate), self.setDate(enddate))

    def addbyday(self,today=False,days=1):
        if today:
            sdate = date.today()
        else:
            sdate = datetime.strptime(self.date, self.format)
        return (sdate + timedelta(days = days)).strftime(self.format)

    def yesterday(self):
        return self.addbyday(today=True,days=-1)

    def daterange(self,start=None,end=None,step=1):
        start = self.datetimeobj(self.assignDate(start)) #assign given date or self date
        end = self.datetimeobj(self.assignDate(end)) #set given date or today date
        # print('daterange : ',start,end)
        day_count = (end - start).days + 2
        datelist = []
        for single_date in [d for d in (start + timedelta(n) for n in range(day_count)) if d <= end]:
            datelist.append(self.coustomFormat(single_date))
        # print(datelist)
        return datelist

    def coustomFormat(self,sdate=None):
        sdate = self.assignDate(sdate)
        return datetime.strptime(sdate, self.format).strftime(self.cformat)

if __name__ == '__main__':
    md = ManageDates('1-2-21')
    # print(md.isstd('01-02-2021 00:00:00'))
    # print(md.date)
    # print(md.addhours(hours=3))
    # print(md.random_date())
    print(md.daterange(end='1-2-21'))
    # print(md.addbyday(days=-1))
    # md.mk_std('mathu')
    