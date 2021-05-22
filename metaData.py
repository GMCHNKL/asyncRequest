from datetime import datetime
from readExcel import ReadExcel
from covidData import CovidData
from fileData import FileData
from icmrData import IcmrData

class MetaData:
	fdlist = []
	cdlist = []
	finaldata = []
	excel_data_dict = ''
	
	page = 'add_record'

	modifiedDate = datetime.now()
	def __init__(self,filedatalist=[],page='add_record',results='all',datacount='all'):
		self.fdlist = filedatalist
		self.df = None
		self.page = page
		self.icmr = None
		self.results = results
		self.datacount = datacount

	def addfdlist(self,fd):
		self.fdlist.append(fd)
	
	def addcdlist(self,cd):
		self.cdlist.append(cd)

	def excel_dd(self):
		if not len(self.fdlist):
			self.fdlist = [FileData()]
		read = ReadExcel(fdlist=self.fdlist,results=self.results)
		df = read.readDataList()
		if self.datacount!='all':
			if self.datacount<=df.shape[0]:
				df = df[:self.datacount]
		self.df = df
		self.excel_data_dict = df.transpose().to_dict()
		return self
	
	def covid_data(self):
		for _,dd in self.excel_data_dict.items():
			cd = CovidData(dd,self.page)
			# print(cd.final_result_of_sample)
			cd.assign_validate()
			self.addcdlist(cd)
			self.finaldata.append(cd.getdatadict())
		return self
	
	def postIcmr(self):
		icmr = IcmrData(data=self.finaldata,page=self.page)
		icmr.create_event_loop()
		return self
	

if __name__ == '__main__':
	fd = FileData('11.05.2021')
	meta = MetaData([fd],results='negative',page='edit',datacount=400)
	# meta.excel_dd().covid_data().postIcmr()
	meta.excel_dd()
	print(meta.df)
	meta.covid_data().postIcmr()
	# print(meta.finaldata)
