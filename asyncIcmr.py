from bs4 import BeautifulSoup
import requests
import asyncio
import time
import aiohttp
import traceback

class AsyncIcmr:
	already_exist = 0
	submitted = 0
	total_data_count = 0
	record_data = {'rec_collected':[],'rec_not_collected':[],'precount':0}
	headers = {
		"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36",
	}
	auth = {
		'username': 'GDHHNKTN',
		'password': 'GMCHNKL2021'}
	authURL = "https://cvstatus.icmr.gov.in/authentication.php"
	submitUrl = 'https://cvstatus.icmr.gov.in/submit.php'
	def __init__(self,log=False,data=[],page='add_record',batch=100):
		self.session = requests.Session()
		if log: self.login()
		self.datalist = data
		self.total_data_count = len(data)
		self.page = page
		self.disconnected = []
		self.finaldata = []
		self.record_id=[]
		self.count = 1
		self.batch = batch

	def separator(func):
		def wrapper(*args,**kargs):
			line = ['-']*20
			print('-'.join(line))
			func(*args,**kargs)
			print('-'.join(line))
		return wrapper

	def exceptions(func):
		def wrapper(*args,**kargs):
			try:
				func(*args,**kargs)
			except Exception:
				traceback.print_exc()
		return wrapper
	def loginMessage(self, text):
		if str(text).lower().find('yes') >= 0:
			print("login successful")
			return
		print("err loginMessage: ",text, "try again !!!")
	async def asyncGetCdId(self, index):
		data = self.datalist[index]
		try:
			url = 'https://cvstatus.icmr.gov.in/edit_record.php'
			fetch = {
				'record_id': data['record_id'],
				'patient_id': data['patient_id']
			}
			async with self.session.post(url, data=fetch, headers=self.headers) as res:
				if res.status != 200:
					print('Response Failed')
					return
				res = await res.text()
				soup = BeautifulSoup(str(res), "html.parser")
				cdid = soup.find(
					'input', {'name': 'clinical_data_id'}).get('value')
				# print('cdid:', cdid)
				return {'index': index, 'value': cdid}
		except Exception as e:
			print("err asyncGetCdId:", e)
		return {'index': index, 'value': None}

	async def asyncGetRecordId(self, index, read_timeout=15.9):
		data = self.datalist[index]
		try:
			url = 'https://cvstatus.icmr.gov.in/get_patient_data.php'
			fetch = {
				'patient_id': data['patient_id'],
				'page': 'search_record',
				'records': 'own'
			}
			async with self.session.post(url, data=fetch, headers=self.headers) as res:
				if res.status != 200:
					print('Response Failed')
					return
				response = await res.text()

				soup = BeautifulSoup(response, "html.parser")
				record_id = soup.find(
					'a', {'class': 'edit_record'}).get('key1')
				# print('record_id:', record_id)
				return {'index': index, 'value': record_id}
		except Exception as e:
			if str(e).find("no attribute 'get'") > 0:
				self.record_data['rec_collected'].append(self.datalist[index])
			else:
				self.record_data['rec_not_collected'].append(
					self.datalist[index])
		return {'index': index, 'value': None}

	async def collect_record_id(self):
		try:
			tasks = []
			for index, data in enumerate(self.datalist):
				if data['record_id'] == '':
					tasks.append(
						asyncio.ensure_future(self.asyncGetRecordId(index))
					)
			recordIdList = await asyncio.gather(*tasks)
			for rec in recordIdList:
				if rec['value']:
					self.datalist[rec['index']]['record_id'] = rec['value']
					self.record_data['rec_collected'].append(
						self.datalist[rec['index']])
			print('record_id Collected')
		except Exception as e:
			print('err:', self, e)
			traceback.print_exc()

	async def collect_clinical_id(self):
		while True:
			try:
				tasks = []
				for index, data in enumerate(self.datalist):
					if data['record_id'] != '' and data['clinical_data_id'] == '' and data['page'] == 'edit':
						tasks.append(
							asyncio.ensure_future(self.asyncGetCdId(index))
						)
				cIdList = await asyncio.gather(*tasks)
				for cdict in cIdList:
					if cdict['value']:
						self.datalist[cdict['index']
									  ]['clinical_data_id'] = cdict['value']
					else:
						self.datalist[cdict['index']]['page'] = 'add_record'
				print(cIdList)
				print('clinical_data_id Collected')
				return
			except Exception as e:
				print('err:', self, e)
				traceback.print_exc()

	async def asyncPost(self, url, data):
		try:
			responseText = ''
			if data['page'] == '':
				return
			async with self.session.post(url, data=data, headers=self.headers) as res:
				if res.status != 200:
					print('Response Failed')
					return
				res = await res.text()
				if str(res).strip() == '':
					return 'No Response'
				print(self.count, '.) ', data['patient_id'], str(res))
				# print(str(res).find('Server disconnected')!=-1 or str(res).find('aborted')!=-1)
				if str(res).find('Server disconnected') != -1 or str(res).find('aborted') != -1:
					print(str(res))
					self.disconnected.append(data)
				else:
					self.finaldata.append(data)
					if data['page'] != 'edit' or str(res).find('submitted') >= 0:
						self.submitted += 1
					elif data['page'] == 'edit' or str(res).find('already exist') >= 0:
						self.already_exist += 1
				self.count += 1
				responseText = res
			return responseText
		except Exception as e:
			print('err Post', e)
			self.disconnected.append(data)

	async def asynclogin(self):
		async def loginRequest():
			async with self.session.post(self.authURL, data=self.auth, headers=self.headers) as res:
				if res.status != 200:
					print('Response Failed')
					return
				return await res.text()
		res = await loginRequest()
		self.loginMessage(res)
		if str(res).find('Cannot connect') >= 0:
			await self.asynclogin()
		return res

	async def postRequest(self):
		tasks = []
		while True:
			try:
				self.collect_record_id()
				if self.page == 'edit':
					await self.collect_clinical_id()
				for data in self.datalist:
					if data['record_id'] == '' or (data['record_id'] != '' and data['clinical_data_id'] != '' and data['page'] == 'edit'):
						tasks.append(asyncio.ensure_future(
							self.asyncPost(self.submitUrl, data)))
					elif data['record_id'] != '' and data['page'] != 'edit':
						self.already_exist += 1
					elif data['record_id'] == '' and data['page'] == 'edit':
						data['page'] = 'add_record'
						tasks.append(asyncio.ensure_future(
							self.asyncPost(self.submitUrl, data)))
					elif data['record_id'] != '' and data['page'] == 'edit' and data['clinical_data_id'] == '':
						print('Disconneted Data Found')
						self.disconnected.append(data)
				response = await asyncio.gather(*tasks)
				# await self.edit_or_submit_msg(response)
				return response
			except Exception as e:
				print('err postRequest:', e)
				await asyncio.sleep(3)

	async def edit_or_submit_msg(self, response):
		datalist = self.datalist
		count = 1
		print('datalist length:', len(datalist))
		print('response length:', len(response))
		for data, res in zip(datalist, response):
			print(count, '.) ', data['patient_id'], str(res), end='=>')
			print(str(res).find('Server disconnected')
				  != -1 or str(res).find('aborted') != -1)
			if str(res).find('Server disconnected') != -1 or str(res).find('aborted') != -1:
				print(str(res))
				self.disconnected.append(data)
			else:
				self.finaldata.append(data)
				if data['page'] == '':
					return
				if data['page'] != 'edit':
					self.submitted += 1
				elif data['page'] == 'edit':
					self.already_exist += 1
			count += 1
		print('Batch successfully submitted')
		return self

	async def main(self):
		attempt = True
		while attempt:
			mastedatalist = self.datalist
			l = len(mastedatalist)
			start = 0
			n = l//self.batch
			rem = l % self.batch
			print('len =', l, 'batch:', n, 'rem batch:', rem)
			for i in range(1, n+1):
					async with aiohttp.ClientSession() as s:
						self.session = s
						await self.asynclogin()
						print('Batch', i, ':')
						self.datalist = mastedatalist[start:i*self.batch]
						start = i*self.batch
						await self.postRequest()
						# await asyncio.sleep(10)
			if rem > 0:
				async with aiohttp.ClientSession() as s:
					self.session = s
					await self.asynclogin()
					print('Batch Remaining:')
					self.datalist = mastedatalist[start:]
					await self.postRequest()
			print('All Batch executed')
			attempt = len(self.disconnected) > 0
			if attempt:
				print('Retrying Disconnected Data...(len) -',
					len(self.disconnected))
				self.datalist = self.disconnected
				# print('Diconected data:')
				# print(self.disconnected)
				self.disconnected = []

	async def find_record_id(self, pid):
		self.datalist = []
		self.mastedatalist = []
		for id in pid:
			self.datalist.append({
				'record_id': '',
				'patient_id': id,
				'page': self.page
			})
		while True:
			mastedatalist = self.datalist
			l = len(mastedatalist)
			start = 0
			n = l//self.batch
			rem = l % self.batch
			print('len =', l, 'batch:', n, 'rem batch:', rem)
			for i in range(1, n+1):
				async with aiohttp.ClientSession() as s:
					self.session = s
					print('Batch', i, ':')
					await self.asynclogin()
					self.datalist = mastedatalist[start:i*self.batch]
					start = i*self.batch
					await self.collect_record_id()
					# await asyncio.sleep(10)
			if rem > 0:
				async with aiohttp.ClientSession() as s:
					self.session = s
					await self.asynclogin()
					print('Batch Remaining:')
					self.datalist = mastedatalist[start:]
					await self.collect_record_id()
			print('All Batch executed')
			count = len(self.record_data['rec_not_collected'])
			attempt = self.record_data['precount'] != count
			if not attempt:
				break
			self.datalist = self.record_data['rec_not_collected']
			self.record_data['precount'] = len(self.datalist)
			print('Retrying Disconnected Data...(len) -', len(self.datalist))
			# print('Diconected data:')
			# print(self.datalist)
			self.record_data['rec_not_collected'] = []
		self.datalist = self.record_data['rec_collected']
		for data in self.record_data['rec_not_collected']:
			self.datalist.append(data)
		return self.datalist

	def _looper(func):
		def wrapper(self,*args,**kargs):
			start_time = time.time()
			print('args:',args)
			print('kargs:',kargs)
			func(self,*args,**kargs)
			print("----%s----" % (time.time()-start_time))
		return wrapper

	def timer(func):
		def wrapper(*args,**kargs):
			start_time = time.time()
			print('args:',args)
			print('kargs:',kargs)
			loop = asyncio.get_event_loop()
			loop.run_until_complete(asyncio.wait([self.main()]))
			print("----%s----" % (time.time()-start_time))
		return wrapper

	@exceptions
	@_looper
	def create_event_loop(self, datalist=[], process='main', data=[]):
		if len(datalist):
			self.datalist = datalist

		loop = asyncio.get_event_loop()
		if process == 'main':
			start_time = time.time()
			loop.run_until_complete(asyncio.wait([self.main()]))
			self.display_results()
			print("----%s----" % (time.time()-start_time))
		elif process == 'record_id':
			start_time = time.time()
			loop.run_until_complete(asyncio.wait([self.find_record_id(data)]))
			self.display_record_id()
			print("----%s----" % (time.time()-start_time))

	@separator
	def display_record_id(self):
		print('Total New Records', len(list(filter(lambda data:data['record_id']=='',self.record_data['rec_collected']))))
		print('Total Already Exist Records', len(list(filter(lambda data:data['record_id']!='',self.record_data['rec_collected']))))

	@separator
	def display_results(self):
		print('Total Execution Data:', self.total_data_count)
		print('Total Add New Records:', self.submitted)
		print('Total Edited or Already Exist:', self.already_exist)

if __name__=='__main__':
	pid=['C316818AA', 'C316819', 'C316820', 'C316821', 'C316822', 'C316823', 'C316824', 'C316825', 'C316826', 'C316827', 'C316828', 'C316829', 'C316830', 'C316831', 'C316832', 'C316833', 'C316834', 'C316835', 'C316836', 'C316837', 'C316838']
	icmr = AsyncIcmr()
	icmr.create_event_loop(process='record_id',data=pid)
	print(icmr.datalist)