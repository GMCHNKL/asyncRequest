from os import access
from bs4 import BeautifulSoup
import requests
import asyncio
import time
from requests import auth
import aiohttp
import json

class IcmrData:
	already_exist = 0
	submitted = 0
	total_data_count = 0
	headers = {
		"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36",
	}
	auth = {
		'username': 'GDHHNKTN',
		'password': 'GMCHNKL2021'}
	authURL = "https://cvstatus.icmr.gov.in/authentication.php"
	submitUrl = 'https://cvstatus.icmr.gov.in/submit.php'
	def __init__(self,log=False,data=[],page='add_record'):
		self.session = requests.Session()
		if log: self.login()
		self.datalist = data
		self.total_data_count = len(data)
		self.page = page
		self.disconnected = []
		if page=='edit':
			self.batch = 100
		else:
			self.batch = 100

	def request(self, url, data):
		return self.session.post(url, data=data, headers=self.headers)

	def loginMessage(self, text):
		if str(text).lower().find('yes') >= 0:
			print("login successful")
			return
		print("err loginMessage: ",text, "try again !!!")

	def login(self):
		res = self.request(self.authURL, self.auth)
		self.loginMessage(res.text)
		return self


	def getRecordId(self, pid):
		try:
			fetch = {
				'patient_id': pid,
				'page': 'search_record',
				'records': 'own'
			}
			response = self.request(
				'https://cvstatus.icmr.gov.in/get_patient_data.php', fetch)
			soup = BeautifulSoup(response.text, "html.parser")
			record_id = soup.find('a', {'class': 'edit_record'}).get('key1')
			# print('record_id:', record_id)
			return record_id
		except Exception as e:
			print("err getRecordId:",e)
		return None

	def getCdId(self, record_id, pid):
		try:
			fetch = {
				'record_id': record_id,
				'patient_id': pid
			}
			response = self.request(
				'https://cvstatus.icmr.gov.in/edit_record.php', data=fetch)
			# print(response.text)
			soup = BeautifulSoup(response.text, "html.parser")
			cdid = soup.find(
				'input', {'name': 'clinical_data_id'}).get('value')
			# print('cdid:', cdid)
			return cdid
		except Exception as e:
			print('err getCdId:',e)
		return None

	async def asyncGetCdId(self,index):
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
				return {'index':index,'value':cdid}
		except Exception as e:
			print("err asyncGetCdId:",e)
		return {'index':index,'value':None}
		
	async def asyncGetRecordId(self,index,read_timeout=15.9):
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
				record_id = soup.find('a', {'class': 'edit_record'}).get('key1')
				# print('record_id:', record_id)
				return {'index':index,'value':record_id}
		except Exception as e:
			print("err asyncGetRecordId:",e)
		return {'index':index,'value':None}

	async def collect_record_id(self):
		try:
			tasks = []
			for index,data in enumerate(self.datalist):
				if data['record_id']=='':
					tasks.append(
						asyncio.ensure_future(self.asyncGetRecordId(index))
						)
			recordIdList = await asyncio.gather(*tasks)
			for rec in recordIdList:
				if rec['value']:
					self.datalist[rec['index']]['record_id'] = rec['value'];
				else:
					self.datalist[rec['index']]['page'] = 'add_record'
			print(rec)
			print('record_id Collected')
		except Exception as e:
			print('err:',self.__class__,e)

	async def collect_clinical_id(self):
		while True:
			try:
				tasks = []
				for index,data in enumerate(self.datalist):
					if data['record_id']!='' and data['clinical_data_id']=='' and data['page']=='edit':
						tasks.append(
									asyncio.ensure_future(self.asyncGetCdId(index))
								)		
				cIdList = await asyncio.gather(*tasks)
				for cdict in cIdList:
					if cdict['value']:
						self.datalist[cdict['index']]['clinical_data_id'] = cdict['value'];
				print(cIdList)
				print('clinical_data_id Collected')
				return
			except Exception as e:
				print('err:',self.__class__,e)

	async def addRecordId_CId(self,datalist=[]):
		if len(datalist):
			self.datalist = datalist
		try:
			async with aiohttp.ClientSession() as s:
				self.session = s
				await self.asynclogin()
				await self.collect_record_id()
				await self.collect_clinical_id()

		except Exception as e:
			print('err addRecordId_CId:',e)
		return datalist

	def create_edit_loop(self):
		start_time = time.time()
		loop = asyncio.get_event_loop()
		loop.run_until_complete(asyncio.wait([self.addRecordId_CId()]))
		print("----%s----"%(time.time()-start_time))
	
	
	
	async def asyncPost(self, url, data):
		try:
			async with self.session.post(url, data=data, headers=self.headers) as res:
				if res.status != 200:
					print('Response Failed')
					return 
				return await res.text()
		except Exception as e:
			return e

	async def asynclogin(self):
		res = asyncio.ensure_future(self.asyncPost(self.authURL, self.auth))
		log = await res
		self.loginMessage(log)
		if str(log).find('Cannot connect')>=0:
			await self.asynclogin()
		return log

	async def postRequest(self):
		tasks = []
		# print(self.datalist)
		accept = True
		while accept:
			try:
				if self.page=='edit':
					await self.collect_clinical_id()
				for data in self.datalist:
					if (data['record_id']!='' and data['clinical_data_id']!='' and  data['page']=='edit') or (data['record_id']=='' and data['page']!='edit'):
						tasks.append(
							asyncio.ensure_future(self.asyncPost(self.submitUrl,data))
							)
					elif data['record_id']=='' or data['clinical_data_id']=='':
						self.disconnected.append(data)
					elif data['record_id']!='':
						self.already_exist+=1

				response = await asyncio.gather(*tasks)
				await self.edit_or_submit_msg(response)
				accept = False
			except Exception as e:
				print(e)
				await asyncio.sleep(3)

			return response

	async def edit_or_submit_msg(self,response):
		datalist = self.datalist
		count = 1
		for data,res in zip(datalist,response):
			print(count,'.) ',data['patient_id'], res)
			if str(res).find('Server disconnected')!=-1 or str(res).find('aborted')!=-1:
				self.disconnected.append(data)
			else:
				if data['page']!='edit':
					self.submitted+=1
				else:
					self.already_exist+=1
			count+=1
		print('Batch successfully submitted')
		return self

	async def main(self):
		try:
			attempt = True
			async with aiohttp.ClientSession() as s:
				self.session = s
				await self.asynclogin()
				await self.collect_record_id()
			while attempt:
				mastedatalist = self.datalist
				l = len(mastedatalist)
				start = 0
				n = l//self.batch
				rem = l%self.batch
				for i in range(1,n+1):
					async with aiohttp.ClientSession() as s:
						self.session = s
						await self.asynclogin()
						print('Batch',i,':')
						self.datalist = mastedatalist[start:i*self.batch]
						start = i*self.batch
						await self.postRequest()
						# await asyncio.sleep(10)
				if rem!=0:
					async with aiohttp.ClientSession() as s:
						self.session = s
						await self.asynclogin()
						print('Batch Remaining:')
						self.datalist = mastedatalist[start:]
						await self.postRequest()
				print('All Batch executed')
				attempt = len(self.disconnected)!=0
				if attempt:
					print('Retrying Disconnected Data...')
					self.datalist = self.disconnected
					self.disconnected = []
		except Exception as e:
			print(e)
		finally:
			print('Executed successfully!!!!')

	def create_event_loop(self,datalist=[]):
		if len(datalist):
			self.datalist = datalist
		try:
			start_time = time.time()
			loop = asyncio.get_event_loop()
			loop.run_until_complete(asyncio.wait([self.main()]))
			self.display_results()
			print("----%s----"%(time.time()-start_time))
		except Exception as e:
			print('err create_event_loop: ',e)
	
	def display_results(self):
		line = ['-']*20
		print('-'.join(line))
		print('Total Execution Data:',self.total_data_count)
		print('Total Add New Records:',self.submitted)
		print('Total Edited or Already Exist:',self.already_exist)
		print('-'.join(line))
if __name__ == '__main__':
	data = [
		{'patient_name': 'dr kotteeswari', 'patient_id': 'C327879', 'sample_id': 'C327879', 'age': '33', 'gender': 'F', 'contact_number': '9486315143', 'address': 'w/o leeletheran kondisettipatti namakkal', 'final_result_of_sample': 'positive', 'srf_id': '', 'sample_cdate': '18-05-2021 09:58:20', 'sample_rdate': '18-05-2021 10:17:27', 'sample_tdate': '19-05-2021 12:39:31', 'page': '', 'record_id': '', 'clinical_data_id': '', 'community_hospital': 'hospital', 'age_in': 'Years', 'contact_number_belongs_to': 'patient', 'nationality': 'India', 'state': '33', 'district': '580', 'hospitalized': 'No', 'mode_of_transport': 'Walk', 'testing_kit_used': 'LabGun-tm_ExoFast', 'repeat_sample': 'No', 'otp_verified_srf': 'S', 'patient_occupation': 'OTHER', 'aarogya_setu_app_downloaded': 'No', 'contact_with_lab_confirmed_patient': 'No', 'patient_category': 'NCat18', 'sample_type': 'Nasopharyngeal_Oropharyngeal', 'status': 'Asymptomatic', 'sample_collected_from': 'Non-containment area', 'covid19_result_egene': 'positive', 'rdrp_confirmatory': 'positive'}, {'patient_name': 'ruban', 'patient_id': 'C327885', 'sample_id': 'C327885', 'age': '35', 'gender': 'M', 'contact_number': '9891824412', 'address': 's/o isravel,tcode', 'final_result_of_sample': 'positive', 
'srf_id': '', 'sample_cdate': '19-05-2021 13:57:20', 'sample_rdate': '19-05-2021 15:06:56', 'sample_tdate': '20-05-2021 17:33:46', 'page': 'edit', 'record_id': '', 'clinical_data_id': '', 'community_hospital': 'hospital', 'age_in': 'Years', 'contact_number_belongs_to': 'patient', 'nationality': 'India', 'state': '33', 'district': '580', 'hospitalized': 'No', 'mode_of_transport': 'Walk', 'testing_kit_used': 'LabGun-tm_ExoFast', 'repeat_sample': 'No', 'otp_verified_srf': 'S', 'patient_occupation': 'OTHER', 'aarogya_setu_app_downloaded': 'No', 'contact_with_lab_confirmed_patient': 'No', 'patient_category': 'NCat18', 'sample_type': 'Nasopharyngeal_Oropharyngeal', 'status': 'Asymptomatic', 'sample_collected_from': 'Non-containment area', 'covid19_result_egene': 'positive', 'rdrp_confirmatory': 'positive'}, {'patient_name': 'murali shankar', 'patient_id': 'C327887', 'sample_id': 'C327887', 'age': '36', 'gender': 'M', 'contact_number': '9823114793', 'address': 's/o parashivam,mohanur road,nkl', 'final_result_of_sample': 'positive', 'srf_id': '', 'sample_cdate': '19-05-2021 02:45:20', 'sample_rdate': '19-05-2021 13:25:09', 'sample_tdate': '19-05-2021 17:26:47', 'page': 'edit', 'record_id': '', 'clinical_data_id': '', 'community_hospital': 'hospital', 'age_in': 'Years', 'contact_number_belongs_to': 'patient', 'nationality': 'India', 'state': '33', 'district': '580', 'hospitalized': 'No', 'mode_of_transport': 'Walk', 'testing_kit_used': 'LabGun-tm_ExoFast', 'repeat_sample': 'No', 'otp_verified_srf': 'S', 'patient_occupation': 'OTHER', 'aarogya_setu_app_downloaded': 'No', 'contact_with_lab_confirmed_patient': 'No', 'patient_category': 'NCat18', 'sample_type': 'Nasopharyngeal_Oropharyngeal', 'status': 'Asymptomatic', 'sample_collected_from': 'Non-containment area', 
'covid19_result_egene': 'positive', 'rdrp_confirmatory': 'positive'}]
	icmr = IcmrData(
		log=True,
		data=data,page='edit'
	)
	res = icmr.request(icmr.submitUrl,data=data[0])
	print(res.text)