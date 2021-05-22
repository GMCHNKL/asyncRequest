import random
from manage import *
import re
import string

# print(isnull('naN'))
def isnull(value):
  value = str(value).lower()
  empty = ['null','na','nan','']
  return value in empty

def comparelen(val1, op, val2):
	res = False
	if op == 'lt':
		res = len(str(val1)) < val2
	elif op == 'gt':
		res = len(str(val1)) > val2
	elif op == 'gte':
		res = len(str(val1)) >= val2
	elif op == 'lte':
		res = len(str(val1)) <= val2
	elif op == 'eq':
		res = len(str(val1)) == val2
	elif op == 'neq':
		res = len(str(val1)) != val2
	return res

def isdigit(value):
	try:
		value = int(value)
	except:
		return False
	return True

def removePunctuations(value,replacewith=''):
	marks = '''!()-[]\{\};?@#$%:'"\.^&*_\n\t'''
	value = str(value).lower()
	for x in value:
		if x in marks:
			value = value.replace(x, replacewith)
	return value

def getrandnamelist():
	return ['SATHYA(IP/LW)', 'palaniammal', 'muthusamy', 'dharneshwaran', 'SUBIKSA', 'VISHWANATHAN', 'GOVIMDASAMY', 'LAKSHMANAN', 'KIRIJAKUMARI', 'PERUMAYEE', 'ELANGO', 'JAYAMANI', 'KRISHNAMOORTHY', 'VEERAMMAL', 'DHANASEKARAN', 'SUGUNTH', 'BALAJI', 'MASILAMANI', 
'SANTHISH', 'PREMNATH', 'NAGENDRAN', 'DHANASEKARAN', 'VENNILA', 'MOUNIKA', 'CHINNAMMAL', 'GOKUL', 'PANDIYAN', 'ARULMOZHI', 'HARIPRAKASH', 'KAVITHA', 'KEERTHIKA', 'PERUMAYEE', 'JEGATHISAN', 'SANGEETHA', 'SELVARAJ', 'PERIYASAMY', 'SRIRANGAN', 'SARAVANAN', 'SRIRAM', 'MALARVIZHI', 'SAGEETHA', 'ARUNKUMAR', 'MALAR', 'MATHIVANAN', 'AANANTH', 'SURESH', 'UMA', 'PERUMAYEE', 'ARUNKUMAR', 'KAVITHA', 'HARINI', 'THAVAMANI', 'SENTHILKUMAR', 'DHANASEKARAN', 'SABITHA', 'VIJAYASEKAR', 'KUPPUSAMY', 'KANDASAMY', 'JEGANATHAN', 'INDARANI', 'SHANMUGAM', 'KUMAR', 'SUGUNA', 'KRISHNAVENI', 'BALAJI', 'KALAISELVI', 'RAJAMANIKAM', 'SURESH', 'AMARAVATHI', 'NAVEEN', 'MOHAN', 'KAMARVNNISHA', 'SATHIYASOORI', 'BIRNDHA', 'RAMAKRISHNAN', 'SELVARAJ', 'SELVARAJ ', 'MUTHUSAMY', 'SAKTHIPRIYA', 'RITHICK', 'HARIDHARSHINI ', 'YUVARANI', 'THENMOZHI ', 'SAKTHIVEL', 'MUNIYAPPAN ', 'KUPPUSAMY ', 'PALANIYAPPAN', 'SANGEETHA', 'SIVAJI', 'GAYATHRI', 'Loganathan', 'Rajagopal', 'Mamthra', 'Kumaresan', 'Jothi ', 'Nishandhini', 'Ramakrishnan', 'Periyasamy', 'Ram pravesh yadav', 'Gopinath', 'Santhiya', 'Marimuthu', 'Ganeshan', 'Sivarangarajan', 'dinesh kumar', 'Madhesh wari', 'Karthi keyan', 'Kiran', 'Sivanath', 'Neelama', 'Bakiya jothi', 'Appu', 'Manikandan', 'Tamil selvan', 'Poonkodi', 'Subramaniyan', 'Mahendran', 'Kaliyappan', 'Anitha', 'Shanthi', 'Chndhru', 'Angamuthu', 'Jothi Lakshmi', 'Dhana bakiyam', 'DR.P.MANIVANNAN', 'DR.ASHOK KUMAR ', 'S.RAJA ', 'TAMILRAJ ', 'RAJESHWARI ', 'SUBRAMANI ', 'PRADEEP ', 'VIGNESHKUMAR ', 'POONMOZHI ', 'NAGULAN ', 'BALASUBRAMANIAM', 'MANI ', 'KARUPAGAVALLI ', 'RANI ', 'JOTHILAKSHMI ', 'SIBIRAJ ', 'ANGAMMAL ', 'KUMARASAMY ', 'KALAISELVAM ', 'VARAKIKA ', 'REEGAN ', 'ANANDHI ', 'BALASUBRAMANI             ', 'KALAIARASI ', 'PRASHATH ', 'ALEX PANDIYAN ', 'SELVAKUMAR ', 'PARAMESHWARAN ', 'GAYATHIRI', 'SURESHKUMAR ', 'CHIRASU ', 'SENTHILKUMAR ', 'NARMADHA ', 'THIRUNAVUKARASU ', 'THANGAMANI ', 'AMSAVELLI ', 'THARUNKUMAR ', 'VANAJA ', 'APPAVU ', 'MONIKA ', 'BAKKIYALAKSHMI ', 'PAVATHAL ', 'SARAVANAKUMAR ', 'KAVITHA ', 'MANOJKUMAR ', 'SENTHIL ', 'TAMILARASI ', 'SHAKTHIVEL ', 'ARUNADEVI ', 'SATHEESH ', 'THANGAVEL ', 'POONKODI ', 'KALPANA ', 'YASWIN BANU ', 'SOUNDAR', 'SHALINI ', 'DURAI ', 'SUGANTHI ', 'JANAVI ', 'PRENGANATH ', 'PRITHIKA ', 'BIRUNTHA ', 'VANITHA ', 'SENTHILNADHAN ', 'KAVITHA ', 'NIKITHA ', 'RAJESHWARI ', 'SELVAM ', 'SIVASURYA ', 'NAVEENKUMAR ', 'AMBLROSE ', 'SURESH', 'THANDAMANI', 'SHAMILI ', 'SAROJA ', 'MURUGESAN ', 'ANANTH ', 'SELLADURAI ', 'GNANASEKARAN ', 'BALAMURUGAN ', 'PAVITHRA ', 
'MATHESHWARI ', 'SANGEETHA ', 'THANGARASU ', 'MUTHUVEERAN ', 'DEVIKALA', 'SIVAKUMAR ', 'SRINIVASA', 'DHARANI', 'KARTHIK', 'MAHESWARI', 'SAKTHIVEL', 'DR.DHANASEKARAN', 'SUBASH', 'JOTHI ', 'SHANTHI', 'SARASU', 'VIJAYALAKSHMI', 'SHANTHI', 'NAVEENKUMAR ', 
'GOKULRAJ ', 'LINGESHWARAN ', 'SURESH  ', 'VIJAYARANI ', 'HARIKRISHNA ', 'ASWATHA ', 'SWETHA ', 'MADESHWARI ', 'DEVIKA', 'MARAYEE ', 'DHARANI ', 'BAGAVATHI ', 'POOVITHA ', 'PRIYADHARANI ', 'KAVITHA ', 'PRABHU ', 'SARAVANAN ', 'TAMILVANAN ', 'SUGANTHI ', 'PARAESHWARY ', 'KUMAR ', 'PALANIYAPPAN', 'NACHIYAPPAN', 'ANBU SELVAN ', 'GOWTHAM ', 'SUMATHI ', 'SELLAPAPPA ', 'ANANDH ', 'PRADEESH', 'PALANISAMY ', 'PARGUNAN ', 'GOVINDRAJ', 'ARUNKUMAR ', 'KRISHNAKUMAR ', 'SAKTHIVEL ', 'RAGURAMAN ', 'NAVEENKUMAR ', 'MARIYAPPAN ', 'PREMKUMAR ', 'THILAGAVATHY', 'MARUTHAYEE', 'SELTHIL VEL', 'ARAVIND', 'MAHONAHAR', 'KATHIRVEL', 'PANNER SELVAM', 'VIJAYAKUMAR', 'PRASANTH', 'MUTHUKUMAR', 'KUPPUSAMY', 'RANI', 'RISHIKA', 'SARAVANAN', 'NATESAN', 'IYYAPPAN', 'MUKILAN', 'RAJASEKAR', 'PRIYADARSHINI', 'GOMATHI', 'THULASIRAMAN', 'VARUTHARAJAN', 'ARUMUGAM', 'ELANGOVAN', 'TAMILARASU', 'PUSHBHA', 'SEKAR', 'DHARANYAN', 'GOWRISANKAR', 'SAROJA', 'KAVIYARASU', 'GAYATHIRI', 'SARAVANAN', 'RAJAGANAPATHI', 'SRIKANTH', 'PAVINKUMAR', 'KARTHIK', 'SARAN', 'KALIDHAS', 'KARTHIKA', 'VELUSAMY', 'ASHOK', 'DINESHKUMAR', 'HARIPRASATH', 'NAVEENKUMAR', 'KALAIVANAN', 'RAJENDRAN', 'JOTHIKA', 'RAVI', 'DHANASELLAN', 'Venkatesh', 'Rajini', 'Sekar', 'Varatharaj', 'Keerthika', 'Sanjay kumar', 'Bharathkumar', 'Punithavadhi', 'Thilagam', 'Madheswaran', 'Ramesh kumar', 'Harini', 'Eswaramoorthy', 'Manikandan', 'Ranganathan', 'Vasantha', 'Paneer selvam', 'Thangammal', 'Kandhasamy', 'Saravanan', 'Rajkumar', 'Paramasivam', 'Venkatesh', 'Karthikeyan', 'Sumathi', 'HEMANTHI', 'SOUNDHARAJAN', 'SOUNDHRIYA', 'VENKATESH', 'YADHWAR', 'VIMALA', 'SANKAR', 'MANIKANDAN', 'GUPUSAMY', 'SEKAR', 'RAJESWARI', 'DRAVIT', 'ANITHA', 'MAHALAKSHMI', 'TAMILSELVAN', 'KARIKALAN', 'JOTHILAKSHMI', 'ALAGARASAN', 'BOOPATHI', 'ARAVINTH', 'POONGODI', 'BOOPATHI', 'VARUTHARAJAN', 'RAJESWARI', 'SELVI', 'PRABHAKARAN', 'SABARI', 'MANICKAM', 'GANAPATHI', 'ARULRAJ', 'VASANTHAKUMARI', 'JAYAGOPAL', 'SENGODAVEL', 'ATHAYEE', 'RANGASAMY', 'NAGAMMAL', 'LATHA', 'BAIRAVI', 'BHARATIDASAN', 'PRABHU', 'ELIZARASAN', 'LALITHA', 'DEEPAN', 'DURAISAMY', 'KALPANA', 'SIVA', 'TAMILSELVI', 'BHARATHKARTHICK', 'BAHARATHI', 'THIYAGARAJAN', 'VAITHALINGAM', 'ATHIYA', 'RAMASAMY', 'CHAMBARAM', 'PERUMAYEE', 'CHINNUSAMY', 'JANANI', 'INDHUJA', 'MASAILAMANI', 'KOMARAYEE', 'KUMUDHA', 'SARASWATHI', 'MALA', 'PALANIYAMMAL', 'PERIYAPILLAI', 'MAYILI', 'RAMASAMY', 'VEERAMANI', 'SATHISH', 'PERIYASAMY', 'KANNUPILLAI', 'AMMAIYAKKAL', 'CHELLAMMAL', 'KAMALAM', 'GANDHIMATHI', 'CHITRA', 'MAGESH', 'THANGAYEE', 'CHELLAMMAL', 'SUSILA', 'KALIYAMMAL', 'KAMALAM', 'MALARMANI', 'JAGADHAMBAL', 'SAROJA', 'RAMESHWARI', 'SAMUNDEESWARI', 'SAKUNTHALA', 'INDHUMATHI', 'MALLIGA', 'CHINNAMMAL', 'PATTU', 'NITHYA', 'MUTHULAKSHMI', 'ANITHA', 'PRIYA', 'RANI', 'SUBRAMANI', 'MANI', 'SARASWATHI', 
'PAPATHI', 'KARIAKKAL', 'SUSILA', 'KAVITHA', 'REVATHI', 'SANTHI', 'AMIRTHAVALLI', 'ILAVARASI', 'VEERAMMAL', 'MANIMEGALAI', 'RUCKMANI', 'VASANTHI', 'AMUTHA', 'VIJAYA', 'PARAMESWARI', 'MAGESHWARI', 'SOWDHAMANI', 'SUDHA', 'SATHYA', 'CHINNAGOUNDER', 'KAMALAM', 'MALLIGA', 'CHITRA', 'CHELLAMMAL', 'RAJESWARI', 'PALANIYAMMAL', 'JAYAMANI', 'DHAVAMANI', 'THILAGAVATHI', 'KAVITHA', 'RAJESWARI', 'SARASWATHI', 'YOGAMBAL', 'MALLIGA', 'NACHAMMAL', 'BABY', 'KARAMBIGAI', 'SARASWATHI', 'VASANTHAKUMARI', 'SUMATHI', 'SELVI', 'MALLIGA', 'LAKSHMI', 'LAVANYA', 'SATHYA', 'BAKKIYALAKSHMI', 'SATHYA', 'NADHAKUMAR', 'LOGITHWARMA', 'RAMAIYA', 'VASANTHA', 'CHELLAMMAL', 'MUNIRA BEGAM', 'BHARATHIDHASAN', 'MAHESWARI', 'PAVITHRA', 'SIVAKUMAR', 'JAGADHAMBAL', 'VISWANATHAN', 'MANORANJITHAM', 'RAJENDRAN', 'ARUL', 'REVATHI', 'SUBRAMANI', 'KAVYA', 'SHABIULLAH', 'BALUSAMY', 'VISWANATHAN', 'Ramasamy', 'Geetha', 'Arul', 'Thavamani', 'Karthi ', 'Ramesh', 'SHANMUGAM', 'Keerthana', 'Gowsalya', 'Murugan', 'Thirunayukkarasu', 'Kamalakkannan', 'Kasilakshmi', 'Nandhakumar', 'Sindhu', 'Chandrasekaran', 'Dr.Saranya', 'Venkadesh', 'Rani', 'Navanthika', 'Kayalvizhi', 'Muthammal', 'Rajenthiran', 'Vijayabaskaran', 'Sandhos', 'Palanivel', 'Saraswathi', 'Palanivel', 'Saraswathi', 'Devarajan', 'Rajan', 'Govindharaj', 'Sundharambal', 'Rajam', 'Mohan', 'Praba', 'Dhanapal', 'Seenivasan', 'Lalitha', 'Varudharajan', 'Vijaya', 
'Suresh ', 'Rajamani', 'Sugunesh', 'Soundharam', 'Hariharasundhar', 'MANI', 'BARATH RAJ', 'KARTHIK', 'PRABHU', 'SELVAM ', 'MANI', 'DEVENDIRAN', 'KARTHIK', 'KAVERY', 'SARASU', 'ARUN HARSHITH', 'DINESH KUMAR', 'SARATH KUMAR', 'MUTHU VEL', 'BOOPATHI', 'NANDHAKUMAR', 'SELVAM ', 'CHANDRAN ', 'ELANGOVAN ', 'ANGURAJ ', 'THANGAMANI ', 'VARUNKUMAR', 'MOHAN ', 'AKILANDESWARI ', 'NITHRAINI', 'PAVITHIRAYINI', 'VIJAY ', 'SURESH', 'SATHISH ', 'KARTHIKEYAN ', 'MUTHUSAMY ', 'SREE SAKTHI ', 'PRABHU', 'GOPAL ', ' PARVESH ', 'SUBRAMANIAM ', 'PALANIVEL ', 'KAVEENA ', 'PREMALATHA ', 'DURAISAMY ', 'LAKSHMI ', 'KARUPPUSAMY ', 'NADARAJAN ', 'LAKSHMI ', 'KATHIRVEL ', 'VIJAYALAKSHMI ', 'SENTHIL ', 'TAMILSELVI ', 'GIRISH', 'HARISH', 'IYAPPAN ', 'VANITHA', 'ISWARYA ', 'RANNAV', 'BALAKRISHNAN ', 'KARTHI ', 'SELVAM ', 'VASUKI ', 'SABARI ', 'DUVARAGA ', 'IYAPPAN ', 'GOMATHI ', 'NITHISH ', 'RITHIKA ', 'MANIKANDAN ', 'SARVESHWARN ', 'SARANYA ', 'RATHIGA', 'CHINNAPILLAI', 'BALASUBRAMANI', 'SIVAKUMAR', 'ANNAKODI', 'INDHIRA JEYANTHI', 'SANGEETHA', 'RAJAVEL', 'DIVYA PRABHA', 'LALITHA', 'KULANTHAIVEL', 'CHANDHIRA', 'MONISHA', 'AJAY', 'CHITRA', 'RAMYA', 'MANIKSHA', 'MANI ', 'SUBANANDHAN ', 'MADHAN ', 'BRINDHA ', 'MADHUMITHA ', 'YOGAPRIYA ', 'KANNIYAMMAL ', 'HARIHARAN ', 'SUMATHI ', 'SALEEM ', 'RUBINA', 'AJEEMJHAN ', 'USHA RANI', 'NITHISH', 'RAGURAMAN', 'RUBINI', 'DINESH KUMAR', 'SARASHWATHI', 'VIJAYALAKSHMI', 'UMADEVI', 'KARTHIK.M ', 'VIJAYAKUMAR', 'MALARVIZHI ', 'VIVEK', 'HEMALATHA', 'LOGESHWARAN ', 'ANNAMALAI ', 'BARATHKUMAR ', 'PRAKASH ', 'JEYAKODI', 'MUTHUKUMAR', 'KANAGARAJ', 'VELLUSAMY', 'GOPAL ', 'VENI', 'SATHISKUMAR', 'SARAVANAN', 'JAHIR', 'DR HEMALATHA', 'MAHESWRI', 'RAJAMANI', 'DHANALAKSHMI', 'MANJUDEVI', 'B/O REJENAI', 'B/O SUGATHE', 'S/N GEETHA', 'THAMOTHARAN', 
'MADHAVAN', 'GOAPALRAM BIRDA', 'KOVALAN', 'DR M SARANYA', 'BANUPRIYA', 'VINITHA']

class CovidData:
	patient_name = ''
	patient_id = ''
	sample_id = ''
	age = ''
	gender = ''
	contact_number = ''
	address = ''
	final_result_of_sample = 'negative'
	srf_id = ''
	sample_cdate = ''
	sample_rdate = ''
	sample_tdate = ''
	record_id = ''
	clinical_data_id = ''
	
	def __init__(self,datadict={},page='add_record'):
		self.dd = datadict
		self.page = page
		if len(datadict):
			self.importdata()
			self.assign_validate()

	def assign_validate(self):
		self.validatePid()
		self.validateName()
		self.validateAge()
		self.validateGender()
		self.validateNumber()
		self.validateAddress()
		self.validateSrf()
		self.assignResult()
		self.assignDate()

	def importdata(self,dd=''):
		if dd=='':
			dd = self.dd
		if dd['patient_id']:
			self.patient_id = dd['patient_id']
			self.sample_id = dd['patient_id']
		if dd['sample_cdate']:
			self.sample_cdate = dd['sample_cdate']
		if dd['patient_name']:
			self.patient_name = dd['patient_name']
		if dd['age']:
			self.age = dd['age']
		if dd['gender']:
			self.gender = dd['gender']
		if dd['contact_number']:
			self.contact_number = dd['contact_number']
		if dd['age']:
			self.age = dd['age']
		if dd['address']:
			self.address = dd['address']
		if dd['srf_id']:
			self.srf_id = dd['srf_id']
		if dd['final_result_of_sample']:
			self.final_result_of_sample = dd['final_result_of_sample']
		return self
		
	def isPid(self,pid):
		return re.search(
			r'^(c\d{6})\w*',
			str(pid).strip().lower()
		)
	def validatePid(self):
		pid = removePunctuations(self.patient_id) 
		if not self.isPid(pid):
			abc = string.ascii_letters.upper()
			pid = 'C'+ str(rand_ndigits(6))+random.choice(abc)+random.choice(abc)
		pid = pid[0].upper()+pid[1:]
		self.patient_id = pid
		self.sample_id = pid
		return pid

	def validateName(self):
		name = self.patient_name
		if isnull(name):
			name = random.choice(getrandnamelist())
		name = removePunctuations(name)
		if comparelen(name, 'lt', 4):
			name = name+'    '
		self.patient_name = name
		return name

	def validateAge(self):
		rand = random.randrange(35, 65)
		age = removePunctuations(self.age)
		if isnull(age) or not isdigit(age):
			age = rand
		self.age = age
		return age

	def validateGender(self):
		gender = removePunctuations(self.gender)
		if isnull(gender):
			gender = random.choice(['M','F'])
		elif gender[0] == 'm':
			gender = 'M'
		else: gender = 'F'
		self.gender = gender
		return gender

	def validateNumber(self):
		contact_number = removePunctuations(self.contact_number)
		if comparelen(contact_number, 'lt', 10) or isnull(contact_number) or isdigit(contact_number):
			contact_number = '9'+str(rand_ndigits(9))
		self.contact_number = contact_number
		return contact_number

	def validateAddress(self):
		address = removePunctuations(self.address)
		if isnull(address):
			address = 'Namakkal NKL'
		self.address = address
		return address

	def validateSrf(self):
		srf = removePunctuations(self.srf_id)
		if isnull(srf) or isdigit(srf):
			self.srf_id = ''
			return ''
		n = int(srf)
		if comparelen(srf, 'lt', 13):
			prefix = 3358000000000
			if n+prefix < 3359000000000:
				srf = n+prefix
		else: srf = ''
		self.srf_id = srf
		return srf

	def validateCdate(self):
		cdate = self.sample_cdate
		if comparelen(cdate, 'eq', 10):
			cdate = add_2hr(cdate)
		elif comparelen(cdate, 'eq', 8):
			cdate = add_2hr(cdate, '%d.%m.%y')
		else:
			cdate = yesterday()
		self.sample_cdate = cdate
		return cdate

	def assignDate(self):
		cdate = self.validateCdate()
		frmt = '%d-%m-%Y %H:%M:%S'
		rdate = add_2hr(cdate, frmt)
		tdate = upto_today_random(add_2hr(rdate, frmt))
		self.sample_cdate,self.sample_rdate,self.sample_tdate = cdate, rdate, tdate
		return cdate, rdate, tdate

	def assignResult(self):
		value = removePunctuations(self.final_result_of_sample)
		if isnull(value):
			return 'negative'
		reslist = {
			'negative': ['negative'],
			'positive': ['positive'],
			'rejected': ['rejecte', 'resample']
		}
		# print(value)
		for res, alternatives in reslist.items():
			for alt in alternatives:
				if value.find(alt) >= 0:
					self.final_result_of_sample = res
					return res
		self.final_result_of_sample = 'negative'
		return 'negative'


	def getdatadict(self):
		return {
			'patient_name': self.patient_name,
			'patient_id': self.patient_id,
			'sample_id': self.sample_id,
			'age': self.age,
			'gender': self.gender,
			'contact_number': self.contact_number,
			'address': self.address,
			'final_result_of_sample': self.final_result_of_sample,
			'srf_id': self.srf_id,
			'sample_cdate': self.sample_cdate,
			'sample_rdate': self.sample_rdate,
			'sample_tdate': self.sample_tdate,
			'page' : self.page,
			'record_id' : self.record_id,
			'clinical_data_id' : self.clinical_data_id,
			'community_hospital': 'hospital', 'age_in': 'Years', 'contact_number_belongs_to': 'patient',
			'nationality': 'India', 'state': '33', 'district': '580', 'hospitalized': 'No', 'mode_of_transport': 'Walk', 'testing_kit_used': 'LabGun-tm_ExoFast',
			'repeat_sample': 'No', 'otp_verified_srf': 'S', 'patient_occupation': 'OTHER', 'aarogya_setu_app_downloaded': 'No', 'contact_with_lab_confirmed_patient': 'No',
			'patient_category': 'NCat18', 'sample_type': 'Nasopharyngeal_Oropharyngeal', 'status': 'Asymptomatic', 'sample_collected_from': 'Non-containment area',
			'covid19_result_egene': self.final_result_of_sample,
			'rdrp_confirmatory': self.final_result_of_sample,
		}

if __name__ == '__main__':
	p1 = CovidData()
	# read = ReadExcel()
	# read.getList('NAME ')
	print(p1.assign_validate())
	print(p1.getdatadict())