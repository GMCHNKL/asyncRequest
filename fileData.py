import re
import os
import os.path
from os import path
from os import listdir
from os.path import isfile, join
from manageDates import ManageDates


class FileData:
	path = 'DataFolder'
	start = -1
	end = -1
	sufix = ''
	issrf = ''
	date = ''
	def __init__(self, sdate=None,edate=None, days=0, path='DataFolder',filenames=[], start=0, end=-1, issrf='', sufix=''):
		self.filenames = filenames
		self.md = ManageDates(sdate)
		if not sdate:
			try:
				if len(filenames):
					_,self.md.date= self.string_date(filenames[0])
				else:
					_,self.md.date= self.string_date(self.getFiles()[0])
				self.md.date = self.md.setDate(self.md.date)
			except:
				self.md.date = self.md.yesterday()

		self.datelist = self.md.daterange(
			start=sdate,
			end=edate
		)
		print('date taken :',self.md.date)
		self.path = path
		self.start = start-1
		self.end = end
		self.sufix = sufix
		self.issrf = issrf
		self.validFileName()
		self.setFileNames()

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
			rename = file.replace(fdate,mdate)
			os.rename(join(mypath, file), join(mypath, rename))

	def setFileNames(self):
		filelist = self.getFiles()
		if not len(self.filenames):
			datelist=  self.datelist
			self.datelist = []
			for f in filelist:
				for d in datelist:
					if f.find(d)>=0:
						self.filenames.append(self.path+'/'+f)
						self.datelist.append(d)
			if len(self.datelist)==0:
				print('No files where selected')
		else:
			filenames = self.filenames
			self.filenames = []
			for f in filenames:
				if f in filelist or (self.path+'/'+f) in filelist:
					self.filenames.append(f.replace(f,(self.path+'/'+f)))
			if len(self.filenames)==0:
				print('No files where selected')
		return self

	


if __name__ == '__main__':
	fd = FileData('11.5.21')

	print(fd.date)
	print(fd.filenames)
	
