import pandas as pd
from fileData import FileData
from covidData import CovidData
import re


class ReadExcel:
	df = pd.DataFrame()
	patientdf = pd.DataFrame()
	fdlist = []
	columns = ['COVID NUMBER',
			   'SAMPLE DATE', 'NAME ',
			   'AGE', 'SEX', 'COMPLETE ADDRESS',
			   'MOBILE NUMBER',
			   'SRF ID', 'RESULT']
	renamed_col = {'COVID NUMBER': 'patient_id',
				   'SAMPLE DATE': 'sample_cdate', 'NAME ': 'patient_name',
				   'AGE': 'age', 'SEX': 'gender', 'COMPLETE ADDRESS': 'address',
				   'MOBILE NUMBER': 'contact_number',
				   'SRF ID': 'srf_id', 'RESULT': 'final_result_of_sample', }

	def __init__(self, fdlist=[], columns=[],results='all'):
		if len(fdlist):
			self.fdlist = fdlist
		else:
			self.fdlist = [FileData()]
		if len(columns):
			self.columns = columns
		self.results = results

	def findHeader(self):
		return 1

	def findIndexCol(self):
		return 0

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

	def vaidateColumnByName(self, collist):
		print([col for col in collist if self.iscol_cno(col)])

	def getdf(self, fd, fname):
		df = pd.read_excel(
			fname, header=self.findHeader(),
			index_col=self.findIndexCol())
		try:
			# self.vaidateColumnsByName(df.columns)
			df = self.getSlice(fd, df)
			df = df[self.columns]
			df = df[~df['RESULT'].apply(
				lambda x: str(x).lower().strip()).isin(['null', 'na', 'nan', ''])]
			if self.results != 'all':
				print('Select Data which Results:',self.results)
				df = df[df['RESULT'].apply(lambda x: str(x).lower()) == self.results]
			df.rename(columns=self.renamed_col, inplace=True)
		except Exception as e:
			print(fname, e)
		return df

	def readDataList(self):
		for fd in self.fdlist:
			for fname in fd.filenames:
				self.df = self.df.append(self.getdf(fd, fname))
		return self.df

	def getList(self, column, df=None, frac=0):

		if not df:
			print('filenames : ', self.fdlist[0].filenames)
			df = pd.read_excel(
				self.fdlist[0].filenames[0], header=1,
				index_col=0)
		if frac:
			df = df.sample(frac=frac)
		df = df[column]
		return list(df)


if __name__ == '__main__':
	fd = FileData('11.05.2021')
	read = ReadExcel([fd],results="positive")
	df = read.readDataList()
	# read.vaidateColumnsByName(df)
	# print(df.transpose().to_dict())
	# read = ReadExcel()
	# read.vaidateColumnByName(
	# 	[' CNUMBER  ', 'SAMPLE DATE', 'NAME ', 'AGE', 'SEX', 'COMPLETE ADDRESS', 'MOBILE NUMBER', 'HOSPITAL', 'ANC/PNC', '<5 YEARS', 'ILI', 'SARI', 'COMORBITITY', 'PROFESSION/  OCCUPATION', 'SRF ID', 'RESULT', 'DATE OF RESULT', 'NG VALUE', 'RDRP VALUE', 'SGENE', 'KIT USED']
	# )
	# print(read.validate_cno('COVID NUMBER',df))
	print(df)
