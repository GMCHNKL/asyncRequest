# import subprocess
# from datetime import datetime
# gitadd = subprocess.run(["git","add","."])
# print(gitadd)
# gitcommit = subprocess.run(["git", "commit",'-m','file save'+str(datetime.now())])
# print(gitcommit)
# gitpush = subprocess.run(["git","push"])
# print(gitpush)

import os
from datetime import datetime
os.chdir('C:\\Users\\Hp\\Documents\\heroku\\ICMRinsert')
os.system('git remote add origin git@github.com:GMCHNKL/asyncRequest.git')
os.system('git status')
os.system('git add .')
os.system('git commit -m "file saveed on '+str(datetime.now())+'"')
os.system('git push origin main')
print('Git pushed')



