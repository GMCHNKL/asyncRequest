from basedir import BaseDir
from datetime import datetime
from readExcel import ReadExcel
from covidData import CovidData
from fileData import FileData
from icmrData import IcmrData
from collections import defaultdict
import pandas as pd
import os


class MetaData:
	fdlist = []
	cdlist = []
	finaldata = []
	excel_data_list = []
	page = 'add_record'

	modifiedDate = datetime.now()

	def __init__(self, filedatalist=[], page='add_record', results='all', datacount='all'):
		self.fdlist = filedatalist
		self.page = page
		self.icmr = None
		self.results = results
		self.datacount = datacount
		self.covidresult = {}
		self.covidresultlist = []

	def addfdlist(self, fd):
		self.fdlist.append(fd)

	def addcdlist(self, cd):
		self.cdlist.append(cd)

	def excel_dd(self):
		if not len(self.fdlist):
			self.fdlist = [FileData()]
		read = ReadExcel(fdlist=self.fdlist,
						 results=self.results, page=self.page)
		dflist = read.readDataList()
		for df in dflist:
			if self.datacount != 'all':
				if self.datacount <= df.shape[0]:
					df = df.iloc[:self.datacount, :]
			self.excel_data_list.append(df.transpose().to_dict())
		return self

	def covid_data(self):
		for datadict in self.excel_data_list:
			length = 0
			covidresult = {}
			for _, dd in datadict.items():
				cd = CovidData(dd, self.page)
				self.addcdlist(cd)
				datadict = cd.getdatadict()
				if datadict:
					try:
						covidresult[cd.final_result_of_sample] += 1
					except:
						covidresult[cd.final_result_of_sample] = 1
					length += 1
					self.finaldata.append(datadict)
			covidresult['Total count'] = length
			self.covidresultlist.append(covidresult)
		return self

	def postIcmr(self):
		icmr = IcmrData(data=self.finaldata, page=self.page, batch=200)
		icmr.create_event_loop()
		for key, value in self.covidresult.items():
			print(key, ":", value)
		logfilepath = BaseDir+'LogFile//' + \
			str(datetime.now().strftime("%B.%Y"))+'.xlsx'
		read = ReadExcel()
		df = read.readExcelData(logfilepath)
		# data = defaultdict(list)
		for fdate, covidresult in zip(self.fdlist[0].datelist, self.covidresultlist):
			data = {}
			data["Data"] = str(datetime.now().strftime('%d-%m-%Y'))
			data['Time'] = str(datetime.now().strftime('%I:%M:%S %p'))
			data["filename"] = fdate
			data['page'] = self.page
			for key, result in covidresult.items():
				data[str(key).upper()] = result
			print(data)
			# dictdf = pd.DataFrame(data=data)
			df = df.append(data, ignore_index=True)
		print(df)
		df.to_excel(logfilepath, startrow=1, index=False)
		return self


if __name__ == '__main__':
	# fd = FileData('11.05.2021')
	# meta = MetaData([fd],results='negative',page='edit',datacount=400)
	# # meta.excel_dd().covid_data().postIcmr()
	# meta.excel_dd()
	# print(meta.df)
	# meta.covid_data().postIcmr()
	# print(meta.finaldata)

	fd = FileData('11.5.21', path='DataFolder//May 1 to 27', end=10)
	meta = MetaData([fd], results='all', page='edit')
	meta.excel_dd().covid_data().postIcmr()
# 7339374574
