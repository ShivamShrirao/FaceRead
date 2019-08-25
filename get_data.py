import json
import requests
from threading import Thread, RLock
from time import sleep

THREADS = 50
lk=RLock()

with open("Face_Recognition.json","r") as f:
	dd=f.readlines()

dt=[]
for i in dd:
	dt.append(json.loads(i))

IDD=0
TOTAL=len(dt)
print("Total:",TOTAL)

def download(ltt):
	try:
		ret = requests.get(ltt['content'])
		global IDD,TOTAL
		lk.acquire()
		IDD+=1
		lk.release()
		if ret.status_code==200:
			print("[+]",ret,",",IDD,'/',TOTAL)
			name = ltt['content'].split('/')[-1][39:]
			ltt["path"] = "Images/"+name
			with open(ltt["path"],"wb") as f:
				f.write(ret.content)
		else:
			print("[!]",ret,",",IDD)
	except Exception as e:
		print(e)

thrds=[]
for uu in dt:
	thrds.append(Thread(target=download,args=(uu,)))
	thrds[-1].setDaemon(True)
	thrds[-1].start()
	while len(thrds)>=THREADS:
		sleep(1)
		for ix,t in enumerate(thrds):
			if not t.isAlive():
				thrds.pop(ix)

try:
	print("[*] Waiting to finish threads.")
	for t in thrds:
		t.join()
except KeyboardInterrupt:
	print("[!] KeyboardInterrupt detected!\n[*] Exitting....")

with open("downloaded.json","w") as f:
	json.dump(dt,f)