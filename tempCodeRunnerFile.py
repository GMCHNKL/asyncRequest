import subprocess
from datetime import datetime
gitadd = subprocess.run(["git","add","."])
print(gitadd)
gitcommit = subprocess.run(["git", "commit",'-m','file save'+str(datetime.now())])
print(gitcommit)
gitpush = subprocess.run(["git","push"])
print(gitpush)