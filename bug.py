import os
import pandas as pd
from os import path,listdir
from os.path import isfile, join
import sys
from basedir import BaseDir
from manage import login,read_data
from bs4 import BeautifulSoup
import time

def editData(br,datalist):
  count = 0
  for data in datalist:
    id = str(data[0]).strip()
    pid = str(data[1]).strip()
    cdate = str(data[2]).strip()
    rdate = str(data[3]).strip()
    try:
      fetch = {
          'record_id': id,
          'patient_id': pid
      }
      # print('fetch :' ,fetch)
      try:
        response = br.request('POST','https://cvstatus.icmr.gov.in/edit_record.php',data=fetch)
        # print(response.text)
        soup = BeautifulSoup(response.text,"lxml")
        cdid = soup.find('input',{'name':'clinical_data_id'}).get('value')
      except Exception as e:
        print(e)
        cdid = ''
 
      edit = {
      'record_id': id,
      'patient_id': pid,
      'clinical_data_id': cdid,
      'community_hospital': 'hospital',
      'patient_id': pid,
      'nationality': 'India',
      'state': '33',
      'district': '580',
      'patient_category': 'NCat18',
      'sample_cdate': cdate,
      'final_result_of_sample': 'Negative',
      'sample_rdate': rdate,
      'testing_kit_used': 'LabGun-tm_ExoFast',
      # 'repeat_sample': 'No',
      'page': 'edit'
      }
      response = br.request('POST','https://cvstatus.icmr.gov.in/submit.php',data=edit)
      count+=1
      print(count,id,response.text)
    except:
      print(id,'not edited')
 
 
def get_specified_data(fname):
  df = pd.read_excel(fname,header=1)
  sdf = df.groupby([' Date of Sample Received'])['Icmr ID'].nunique()
  sample_date = dict(sdf)
  sample_date = {d:sample_date[d] for d in sample_date if sample_date[d]>6}
  print(sample_date)
  grouped = df.groupby(' Date of Sample Received')
  datalist = []
  for s in sample_date:
    specificdf = grouped.get_group(s)
    specificdf = specificdf[specificdf[' Patient Name']!=' ']
    # print(dict(specificdf[' Patient Name']))
    for index,row in specificdf.iterrows():
      datalist.append([row[0],
                       row[2],
                       pd.to_datetime(row[' Date of Sample Collection']).strftime('%d-%m-%Y %H:%M:%S'),
                       pd.to_datetime(row[' Date of Sample Received']).strftime('%d-%m-%Y %H:%M:%S')
                       ])
  return datalist

def process(from_date='',to_date='',itr=1,delay=10):
  br = login()
  for i in range(itr):
    fpath = BaseDir+'Icmr_Data'
    fname = read_data(br,from_date=from_date,to_date=to_date,fpath=fpath)
    jfname = join(fpath,fname)
    datalist = get_specified_data(jfname)
    print('Count: ',len(datalist))
    editData(br,datalist)
    time.sleep(delay)

if __name__=='__main__':
    process()