import sys
from seleniumrequests import Chrome
from selenium import webdriver
import pandas as pd
import os
import os.path
from os import path
from os import listdir
from os.path import isfile, join
from manage import login, upto_today_random, add_2hr, rand_ndigits
from basedir import BaseDir
import random
import time
from bs4 import BeautifulSoup

class Meta:
  repeat = 0
  success = 0
  negative = 0
  positive = 0
  rejecte = 0
  total_data = 0


meta = Meta()

def addData(br,datadict,flag=0,page='add_record'):
  record_id = ''
  cdid = ''
  if page=="edit":
    try:
          fetch = {
            'patient_id': datadict['patient_id'],
            'page': 'search_record',
            'records': 'own'
          }
          response = br.request('POST','https://cvstatus.icmr.gov.in/get_patient_data.php',data=fetch)
          soup = BeautifulSoup(response.text, "html.parser" )
          record_id = soup.find('a',{'class':'edit_record'}).get('key1')
          print('record_id:',record_id)
          fetch = {
            'record_id': record_id,
            'patient_id': datadict['patient_id']
          }
          response = br.request('POST','https://cvstatus.icmr.gov.in/edit_record.php',data=fetch)
          # print(response.text)
          soup = BeautifulSoup(response.text, "html.parser" )
          cdid = soup.find('input',{'name':'clinical_data_id'}).get('value')
          print('cdid:',cdid)
    except Exception as e:
      print('err:',e)


  data = {
  'record_id': record_id,
  'community_hospital': 'hospital','age_in': 'Years','contact_number':datadict['contact_number'],'contact_number_belongs_to': 'patient',
  'nationality': 'India','state': '33','district': '580','hospitalized': 'No','mode_of_transport': 'Walk','testing_kit_used': 'LabGun-tm_ExoFast',
  'repeat_sample': 'No','otp_verified_srf': 'S', 'patient_occupation': 'OTHER','aarogya_setu_app_downloaded': 'No','contact_with_lab_confirmed_patient': 'No',
  'patient_category': 'NCat18','sample_type': 'Nasopharyngeal_Oropharyngeal','status': 'Asymptomatic','sample_collected_from': 'Non-containment area',
  'covid19_result_egene': datadict['final_result_of_sample'],
  'rdrp_confirmatory': datadict['final_result_of_sample'],
  'clinical_data_id': cdid,
  'page': page,
  }
  for key,value in datadict.items():  data[key]=value
  response = br.request('POST','https://cvstatus.icmr.gov.in/submit.php',data=data)
  print((response.text))
  # print('flag:',flag,",datadict['srf_id']:",datadict['srf_id'])
  if flag==0 and response.text.find('exist')!=-1 and datadict['srf_id']!='':
    datadict['srf_id']=''
    print('Without srf :')
    addData(br,datadict,1,page)
  elif response.text.find('exist')!=-1 and datadict['srf_id']=='':
    meta.repeat += 1
  else:
    meta.success += 1



def validate(datadict):
  datadict = {key:str('Negative' if value=='nan' else value) for key,value in datadict.items()}
  #name
  name = str(datadict['patient_name']).split('(')
  name = name[0]
  if len(name)<4:
      name = name+'    '
  datadict['patient_name'] = name
  # age
  rand = random.randrange(35,65)
  try:
      datadict['age'] = int(datadict['age'])
  except:
      datadict['age'] = rand
  # gender
  gender = datadict['gender']
  if len(gender)==0 or gender[0]=='M' or gender[0]=='m': datadict['gender'] = 'M'
  elif gender[0]=='F' or gender[0]=='f': datadict['gender'] = 'F'
  else: datadict['gender'] = 'M'
  # contact_number
  contact_number = datadict['contact_number']
  if len(contact_number)<10:
      datadict['contact_number'] = '9'+str(rand_ndigits())
  #address
  add = datadict['address'].rstrip()
  if len(add)==0:
      add = 'NAMAKKAL'
  add = add.replace(';','')
  add = add.replace('\n',' ')
  add = add.replace('\t',' ')
  datadict['address'] = add.upper()
  #srf_id
  srf_id = str(datadict['srf_id'])
  
  if srf_id!='':
      try:
          srf_id = srf_id.replace(' ','')
          n = int(srf_id)
          if len(srf_id)<13:
            prefix = 3358000000000
            if n-prefix<0:
              n += prefix
          datadict['srf_id'] = str(n)
      except Exception as e:
          print('err:',e)
          datadict['srf_id'] = ''
  print(datadict['srf_id'])
  cdate = datadict['sample_cdate']
  if len(cdate)==10:
    cdate = add_2hr(cdate)
  elif len(cdate)==8:
    cdate = add_2hr(cdate,'%d.%m.%y')
  datadict['sample_cdate'] = cdate
  rdate = add_2hr(cdate,'%d-%m-%Y %H:%M:%S')
  tdate = add_2hr(rdate,'%d-%m-%Y %H:%M:%S')
  datadict['sample_rdate'] = rdate
  datadict['sample_tdate'] = upto_today_random(tdate)
  # result
  res = (datadict['final_result_of_sample']).lower()
  if res.find('negative')>=0 or res=='' or res=='nan':
      res = 'negative'
      meta.negative += 1
  elif res.find('positive')>=0:
      res = 'positive'
      meta.positive += 1
  elif res.find("rejecte")>=0 or res.find("resample")>=0:
      res = 'rejected'
      meta.rejecte += 1
  datadict['final_result_of_sample'] = res[0].upper()+res[1:]   
  print(datadict['patient_id'],datadict['patient_name'])
  return datadict

def tointeger(val):
  try:
    return str(int(float(val)))
  except:
    return val

def process(fname='',page='add_record',result='all'):
  
  thread = 1
  threadlist = []
  start,end = -1,-1
  sufix=''
  issrf=True
  try:
    if len(sys.argv)>1: 
      sys.argv = sys.argv[1:]
      for arg in sys.argv:
        arg = arg.split('=')
        print(arg)
        if arg[0]=='edit':
          page = 'edit'
        elif arg[0]=='page':
          try: page = arg[1]
          except: print('Default page is:',page)
        elif arg[0]=='s':
          start = int(arg[1])-1
        elif arg[0]=='e':
          end = int(arg[1])
        elif arg[0]=='thread':
          thread = int(arg[1])
        elif arg[0]=='sufix':
          try: sufix = arg[1]
          except: sufix = input("Enter sufix character: ")
        elif arg[0]=='sampleid':
          try: sample_sufix = arg[1]
          except: sample_sufix = input("Enter sufix sampleid character: ")
        elif arg[0]=='fname':
          try: fname = arg[1]
          except: print('Default fname is: Datafolder/(first).xlsx')
        elif arg[0]=='nosrf':
          issrf = False
        else:
          IPython.display.HTML('<h4 style="color:red">Error:</h4>')
          print(arg[0],'Incorrect argument please try again!!!!')
          return []
    if fname=='':
      mypath = BaseDir+'DataFolder'
      onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and not(f[0]=='~')]
      fname = join(mypath, onlyfiles[0])
      print(fname)
    df = pd.read_excel(fname,header=1,index_col=0)
    print('Total Count:',df.shape[0])
    if start!=-1 and end!=-1 and start<end:
      print('start & end')
      df = df.iloc[start:end]
    elif start!=-1:
      print('start only')
      df = df.iloc[start:]
    else:
      print('All dates are going to be process')
  except Exception as e:
    print(e)
    return threadlist
    
  meta.total_data = df.shape[0]
  print('Total Selected Data Count:',df.shape[0])
  br = login()
  count = 0
  endline = ['-']*10
  for index,row in df.iterrows():
    if str(row[0])=='nan' or str(index)=='nan':
      print('ohhh.....')
      break
    datadict = {}
    datadict['patient_name'] = row[2] 
    datadict['patient_id'] = row[0]+sufix
    datadict['sample_id'] = row[0]+sample_sufix
    datadict['age'] = tointeger(row[3])
    datadict['gender'] = row[4]
    datadict['contact_number'] = tointeger(row[6])
    datadict['address'] = row[5]
    datadict['final_result_of_sample'] = row[15]
    datadict['srf_id'] = tointeger(row[14])  if issrf else ''
    datadict['sample_cdate'] = row[1]
    datadict['sample_rdate'] = ''
    datadict['sample_tdate'] = row[16]
    count+=1
    print('-'.join(endline))
    print(f'{count}.) sno: {index}')
    if (row[15].lower().find(result)>=0 or result=='all'):
      addData(br,validate(datadict),page=page)

      
  print('-'.join(endline))
  print('Already exist samples:',meta.repeat)
  print('Successful samples:',meta.success)
  print('Positive samples:',meta.positive)
  print('Negative samples:',meta.negative)
  print('Rejected samples:',meta.rejecte)
  print('Executed successfuly !!!!!!')

if __name__ == '__main__':
  start_time = time.perf_counter()
  mypath = BaseDir+'DataFolder'
  page='add_record'
  onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and not(f[0]=='~')]
  fname = join(mypath, onlyfiles[0])
  print(fname)
  process(fname,page)
  time_exe = float(time.perf_counter() - start_time)
  print("--- %s seconds ---" % str(time_exe/float(meta.total_data)))
