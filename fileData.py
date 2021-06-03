import re
import os
import os.path
from os import path
from os import listdir
from os.path import isfile, join
from manageDates import ManageDates
from basedir import BaseDir

class FileData:
	start = -1
	end = -1
	sufix = ''
	issrf = ''
	date = ''
	def __init__(self, sdate=None, edate=None, path='DataFolder',filenames=None, start=0, end=-1, issrf='', sufix=''):
		self.path = BaseDir+path
		self.validFileName()
		filearr = self.getFiles()
		filearr.sort()
		constrain={'first':[],'end':[],'all':[]}
		if len(filearr):
			constrain = {'first':[filearr[0]],'end':[filearr[-1]],'all':filearr}
		self.filenames = []
		self.datelist = []
		if str(sdate) in list(constrain.keys()):
			filenames = constrain[sdate]
		if filenames:
			if isinstance(filenames,str):
				if filenames in list(constrain.keys()):
					filenames = constrain[filenames]
				else:
					filenames = self.getFileName(filenames)
			for fname in filenames:
				self.filenames.append(self.getFileName(fname))
		print(self.filenames)
		if len(self.filenames)==0 and sdate:
			if isinstance(sdate,str):
				if sdate and edate:
					sdate = self.assignDates(sdate,edate)
				else:
					sdate = [self.assignDates(sdate,edate)]
					print("sdate Only :",sdate)
			for date in sdate:
				self.datelist.append(self.assignDates(date))
		if not self.setFileNames():
			print("No Data Found in the given directory",self.path,"Nothing to Do please check date and filename in  the specified folder")

		self.start = start-1
		self.end = end
		self.sufix = sufix
		self.issrf = issrf
		
		

	def join(self,fname):
		return join(self.path,fname)

	def getFileName(self,fname):
		filearr = self.getFiles()
		print(fname)
		for file in filearr:
			if fname.find(file)>=0:
				return fname
		if isinstance(fname,int):
			if fname<=len(filearr) and fname>=1:
				return filearr[fname-1]
			print("Given int value is out of range in the given directory")
			return ''
		print('Given file name is not valid')
		return ''
		

	def assignDates(self,sdate,edate=None):
		md = ManageDates(sdate)
		dates = [md.isdate(sdate),md.isdate(edate)]
		formatdate = [md.coustomFormat(sdate),md.coustomFormat(edate)]
		if all(dates):
			return md.daterange(formatdate[0],formatdate[1])
		elif dates[0]:
			return formatdate[0]
		elif dates[1]:
			return formatdate[1]
		print('Provided Dates or Invalid')
		return ''


	def checkfn(self,fname):
		return re.search(
				r"[\D]*([0-3]?[0-9])[/\-.]([0-1]?[0-9])[/\-.](([0-9]{2})?[0-9]{2})[\D\d]*.(xlsx)$", fname)
	
	def getFiles(self):
		mypath = self.path
		return [f for f in listdir(mypath) if isfile(join(mypath, f)) and not(f[0] == '~' or f[0] == '.')]

	def string_date(self,fname):
		redate = self.checkfn(fname)
		try:
			fdate = '{0}.{1}.{2}'.format(
				redate.group(1),redate.group(2),redate.group(3))
			md = ManageDates(fdate)
			return fdate,md.coustomFormat()
		except Exception as e:
			print(e)
			print('date in this fname is wrong:'+fname)
			return fdate,fdate

	def validFileName(self):
		mypath = self.path
		for file in self.getFiles():
			fdate,mdate = self.string_date(file)
			if fdate!=mdate:
				rename = file.replace(fdate,mdate)
				os.rename(join(mypath, file), join(mypath, rename))

	def setFileNames(self):
		filelist = self.getFiles()
		if len(self.filenames)==0 and len(self.datelist):
			print('Selecting by dates:')
			datelist=  self.datelist
			self.datelist = []
			for f in filelist:
				for d in datelist:
					if f.find(d)>=0:
						self.filenames.append(f)
						self.datelist.append(d)
			if len(self.datelist)==0:
				print('No files where selected')
				return False
			return True
		elif len(self.filenames):
			filenames = self.filenames
			self.filenames = []
			self.datelist = []
			for f in filenames:
				for fl in filelist:
					if f!='' and f.find(fl)>=0:
						self.filenames.append(f)
						fd,md = self.string_date(fname=f)
						self.datelist.append(md)
			if len(self.filenames)==0:
				print('No files where selected')
				return False
			return True
		return False

	


if __name__ == '__main__':
	fd = FileData(['27.5.21','30.5.21'],path='DataFolder//May 1 to 27')
	print(fd.date)
	print(fd.filenames)
	print(fd.datelist)
