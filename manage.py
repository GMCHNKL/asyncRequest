from __future__ import unicode_literals
import pandas as pd
import os
from os import path
from os import listdir
from os.path import isfile, join
from xlwt import Workbook
import io
import sys
from bs4 import BeautifulSoup
from seleniumrequests import Chrome
from selenium import webdriver
from datetime import datetime  
from datetime import timedelta
import time
import random
from random import randint
from basedir import BaseDir

 
def login():
  op = webdriver.ChromeOptions()
  # op.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
  op.add_argument('--headless')
  op.add_argument('--no-sandbox')
  op.add_argument('--disable-dev-shm-usage')
  br = Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'),chrome_options=op)
  auth = {
  'username': 'GDHHNKTN',
  'password': 'GMCHNKL2021'}
  response = br.request('POST', 'https://cvstatus.icmr.gov.in/authentication.php',data=auth)
  print('login done')
  return br
 
 
def get_repair(filename):
  file1 = io.open(filename, "r", encoding="utf-8")
  data = file1.readlines()
  xldoc = Workbook()
  sheet = xldoc.add_sheet("Sheet1", cell_overwrite_ok=True)
  for i, row in enumerate(data):
      for j, val in enumerate(row.replace('\n', '').split('\t')):
          sheet.write(i, j, val)
 
  xldoc.save(filename)
 
 
def read_data(br,from_date='',to_date='',fpath='',fname=''):
  try:
    today = (datetime.now().strftime('%d-%m-%Y'))
    
    if (from_date=='' and to_date==''):
      from_date = today
      to_date = today
    elif from_date!='' and to_date=='':
      to_date = today
    elif from_date=='' and to_date!='':
      from_date = to_date

   
    if fpath == '':
      fpath = BaseDir+'Icmr_Data'
    if fname == '':
      fname = from_date+'_'+to_date+'.xlsx'
    jfname = join(fpath,fname)

    data = {
        'export_hidden_data': 'export_hidden_data',
        'from_date': from_date,
        'to_date': to_date,
        }
    print(data)
    response = br.request('POST','https://cvstatus.icmr.gov.in/download_export_deo.php',data=data)
    output = open(jfname, 'wb')
    output.write(response.content)
    output.close()
    get_repair(jfname)
    print('Successfuly Readed')
  except Exception as e:
    print(e)
    return ('something went wrong')
  return fname
 
 
# Date Generrator
def str_time_prop(start, end, sformat, eformat, prop):
    stime = time.mktime(time.strptime(start, sformat))
    etime = time.mktime(time.strptime(end, eformat))
    ptime = stime + prop * (etime - stime)
    return time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(ptime))
 
def random_date(start, end,sformat,eformat):
    return str_time_prop(start, end, sformat ,eformat,random.random())
 
def upto_today_random(sdate,format='%d-%m-%Y %H:%M:%S'):
    systime = datetime.now().strftime(eformat)
    sdate = pd.to_datetime(sdate,format=format)
    return random_date(str(sdate), str(systime), sformat, eformat)
 
def add_2hr(sdate,format='%d.%m.%Y',limit=2):
    date = pd.to_datetime(sdate,format=format)
    slimit = 0
    if int(date.strftime('%H'))<9:
      slimit = 9
    startdate = date + timedelta(hours=slimit)
    enddate = date + timedelta(hours=slimit+limit)
    return random_date(str(startdate), str(enddate), sformat, sformat)
 
sformat = '%Y-%m-%d %H:%M:%S'
eformat = '%d-%m-%Y %H:%M:%S'
 
 
# Random mobile no.
def rand_ndigits(n=9):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)