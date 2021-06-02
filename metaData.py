from datetime import datetime
from readExcel import ReadExcel
from covidData import CovidData
from fileData import FileData
from icmrData import IcmrData

class MetaData:
	fdlist = []
	cdlist = []
	finaldata = []
	excel_data_list = []	
	page = 'add_record'

	modifiedDate = datetime.now()
	def __init__(self,filedatalist=[],page='add_record',results='all',datacount='all'):
		self.fdlist = filedatalist
		self.page = page
		self.icmr = None
		self.results = results
		self.datacount = datacount
		self.covidresult = {}

	def addfdlist(self,fd):
		self.fdlist.append(fd)
	
	def addcdlist(self,cd):
		self.cdlist.append(cd)

	def excel_dd(self):
		if not len(self.fdlist):
			self.fdlist = [FileData()]
		read = ReadExcel(fdlist=self.fdlist,results=self.results,page=self.page)
		dflist = read.readDataList()
		for df in dflist:
			if self.datacount!='all':
				if self.datacount<=df.shape[0]:
					df = df.iloc[:self.datacount,:]
			self.excel_data_list.append(df.transpose().to_dict())
		return self
	
	def covid_data(self):
		for datadict in self.excel_data_list:
			for _,dd in datadict.items():
				cd = CovidData(dd,self.page)
				self.addcdlist(cd)
				try:
					self.covidresult[cd.final_result_of_sample]+=1
				except:
					self.covidresult[cd.final_result_of_sample]=1
				datadict = cd.getdatadict()
				if datadict:
					self.finaldata.append(datadict)
			
		return self
	
	def postIcmr(self):
		icmr = IcmrData(data=self.finaldata,page=self.page,batch=200)
		icmr.create_event_loop()
		for key,value in self.covidresult.items():
			print(key,":",value)
		return self
	

if __name__ == '__main__':
	# fd = FileData('11.05.2021')
	# meta = MetaData([fd],results='negative',page='edit',datacount=400)
	# # meta.excel_dd().covid_data().postIcmr()
	# meta.excel_dd()
	# print(meta.df)
	# meta.covid_data().postIcmr()
	# print(meta.finaldata)

	fd = FileData('12.5.21',path='DataFolder//May 1 to 27',end=10)
	meta = MetaData([fd],results='all',page='edit')
	meta.excel_dd().covid_data().postIcmr()
# 7339374574