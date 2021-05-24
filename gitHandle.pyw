import os
from datetime import datetime
import win32gui, win32con

the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)
os.chdir('C:\\Users\\Hp\\Documents\\heroku\\ICMRinsert')
os.system('git remote add origin git@github.com:GMCHNKL/asyncRequest.git')
os.system('git status')
os.system('git add .')
os.system('git commit -m "file saveed on '+str(datetime.now())+'"')
os.system('git push origin main')
print('Git pushed')


