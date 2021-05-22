import requests
from requests.auth import HTTPBasicAuth
import time
import aiohttp
import asyncio

async def asyncPost(session,url,data,headers):
	try:
		async with session.post(url,data=data,headers=headers) as res:
			assert res.status==200
			return await res.text()
	except Exception as e:
		return e

async def main():
	n = 10
	async with aiohttp.ClientSession() as s:
		headers ={
		"User-Agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36",
		}
		auth = {
		'username': 'GDHHNKTN',
		'password': 'GMCHNKL2021'}
		tasks = []
		url = "https://cvstatus.icmr.gov.in/authentication.php"
		response = asyncio.ensure_future(asyncPost(s,url,auth,headers))
		log = await response
		if str(log).lower().find('yes')>=0:
			print("login successful")
		else:
			print(log,"try again !!!")
		print('login done')
		print(log)
		start = 771
		url = 'https://cvstatus.icmr.gov.in/get_srf_record.php'
		for i in range(n): 
			fetch = {
			'srf_id': '3358000275'+str(start+i),
			'page': 'srf_record'
			}
			tasks.append(asyncio.ensure_future(asyncPost(s,url,fetch,headers)))
		res = await asyncio.gather(*tasks)
		print(res)




start_time = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([main()]))
loop.close()
# asyncio.run(main())
print("----%s----"%(time.time()-start_time))