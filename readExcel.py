import pandas as pd
from fileData import FileData
from covidData import CovidData
from icmrData import IcmrData
from datetime import datetime
import traceback
import re
import os
from basedir import BaseDir
import json

class ReadExcel:
	df = pd.DataFrame()
	patientdf = pd.DataFrame()
	fdlist = []

	def __init__(self, fdlist=[], columns=[],results='all',page='add_record'):
		if len(fdlist):
			self.fdlist = fdlist
		else:
			self.fdlist = [FileData()]
		with open('column.json') as json_data:
			self.matchcol = json.load(json_data)
		if len(columns):
			self.columns = columns
		self.matchcol = {key:list(map(lambda val:str(val).strip().lower(),value)) for key,value in self.matchcol.items()}
		self.results = results
		self.page = page
		self.dflist = []
		self.processedDataPath = BaseDir+'DataFolder//Processed'

	def getSlice(self, fd, df):
		start, end = fd.start, fd.end
		if start >= 0 and end >= 0 and start < end:
			print('start & end:')
			return df.iloc[start:end]
		elif start >= 0:
			print('start only')
			return df.iloc[start:]
		elif end > 0:
			return df.iloc[:end]
		print('All dates are going to be process')
		return df

	def iscol_cno(self, cno, df):
		colname = re.search(
			r"^c[\w\s.\-]*((no)|(number))[\w\s.\-]*",
			str(cno).strip().lower()
		)
		cd = CovidData()
		print([1 if cd.isPid(cval) else 0 for cval in self.getList(
			cno, df=df, frac=0.05)])
		return True

	def validate_cno(self, cno, df):
		if self.iscol_cno(cno, df):
			return self.columns[0]

	def tolower(self,x):
		return str(x).lower().strip()

	def vaidateColumnByName(self, df):
		collist = df.columns
		should_match = {col:False for col,_ in self.matchcol.items()}
		finded = {col:False for col in collist}
		for col in collist:
			col_trans = self.tolower(col)
			for key,mlist in self.matchcol.items():
				if finded[col]:
					break
				if col_trans in mlist:
					finded[col] = key
					should_match[key]=True
					break
		if not all(should_match.values()):
			not_found = [key for key,value in should_match.items() if not value]
			print(not_found, "columns are not found!!!")
			print(df.head(10))
			print(collist)
			for nfd in not_found:
				crt = input('Enter alternative for {} :'.format(nfd))
				self.matchcol[nfd].append(crt)
				print(self.matchcol)
				finded[crt] = nfd
			with open('column.json','w') as data:
				json.dump(self.matchcol,data)
		return {key:value for key,value in finded.items() if value}

	def readExcelData(self,fname,type="excel"):
		if not os.path.isfile(fname):
			return pd.DataFrame()
		if type=="excel":
			return pd.read_excel(fname, header=1)
		elif type=="csv":
			return pd.read_csv(fname)

	def fileExist(self,fpath):
		return os.path.isfile(fpath)

	def getdf(self, fd, fname):
		print('Processing on',fname,'!!!')
		df = self.readExcelData(fd.join(fname))
		try:
			rename_col = self.vaidateColumnByName(df)
			if not rename_col:
				return pd.DataFrame()
			df = self.getSlice(fd, df)
			df = df[rename_col.keys()]
			df.rename(columns=rename_col, inplace=True)
			df = df[~df['patient_id'].apply(self.tolower).isin(['null', 'na', 'nan', ''])]
			pid = self.getList('patient_id',df)

			# ppath = self.processedDataPath+'\\'+fname
			# if os.path.isfile(ppath):
			# 	procdf = self.readExcelData(ppath)
			# 	procdf = procdf[rename_col.keys()]

			icmr = IcmrData(page=self.page,batch=500)
			icmr.create_event_loop(process='record_id',data=pid)
			datalist = {data['patient_id']:[data['record_id'],data['page']] for data in icmr.datalist}
			df['record_id'] = df['patient_id'].transform(lambda x: datalist[x][0] if x in list(datalist.keys()) else '')
			
			if self.page!='edit':
				df = df[df['record_id']=='']
			else:
				df['page'] = df['patient_id'].transform(lambda x: datalist[x][1] if x in list(datalist.keys()) else '')
			# self.writeDataList(df,self.processedDataPath+'/',fname)
			df = df[~df['final_result_of_sample'].apply(self.tolower).isin(['null', 'na', 'nan', ''])]
			if self.results != 'all':
				print('Select Data which Results:',self.results)
				df = df[df['final_result_of_sample'].apply(self.tolower).apply(str(self.results).find)>=0]			
		except Exception as e:
			print(fname, e)
			traceback.print_exc()
		return df

	def to_df(self,datadict):
		return pd.DataFrame(datadict)

	def readDataList(self):
		for fd in self.fdlist:
			for fname in fd.filenames:
				df = self.getdf(fd, fname)
				self.writeDataList(df,'DataFolder\\Processed',fname)
				# print(df.head(20))
				if df.empty:
					print("Empty datafram in",fname)
				else:
					self.df = self.df.append(df)
					self.dflist.append(df)
		return self.dflist

	def getList(self, column, df=None, frac=0):
		if df.empty:
			print('filenames : ', self.fdlist[0].filenames)
			df = pd.read_excel(
				self.fdlist[0].filenames[0], header=1,
				index_col=0)
		if frac:
			df = df.sample(frac=frac)
		df = df[column]
		return list(df)

	
	def writeDataList(self,df,path,fname):
		try:
			if not os.path.isdir(path):
				print('Path Created.')
				os.mkdir(path)
			print(path,fname)
			df.to_excel(path+'\\'+fname,startrow=1,startcol=0)
			print('file successfully Saved')
		except Exception:
			print('While creating file something went wrong')
			traceback.print_exc()

	


if __name__ == '__main__':
	fd = FileData(path='DataFolder//May 1 to 27')
	read = ReadExcel([fd],page='edit')
	df = read.readDataList()
	# read.vaidateColumnsByName(df)
	# print(df.transpose().to_dict())
	# read = ReadExcel()
	# read.vaidateColumnByName(
	# 	[' CNUMBER  ', 'SAMPLE DATE', 'NAME ', 'AGE', 'SEX', 'COMPLETE ADDRESS', 'MOBILE NUMBER', 'HOSPITAL', 'ANC/PNC', '<5 YEARS', 'ILI', 'SARI', 'COMORBITITY', 'PROFESSION/  OCCUPATION', 'SRF ID', 'RESULT', 'DATE OF RESULT', 'NG VALUE', 'RDRP VALUE', 'SGENE', 'KIT USED']
	# )
	# print(read.validate_cno('COVID NUMBER',df))
	print(df)
