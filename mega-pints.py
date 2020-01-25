from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests as req
from colorama import Fore
import time
from random import choice
import os

uagent = [
			'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/79.0.3945.73 Mobile/15E148 Safari/605.1',
			'Mozilla/5.0 (Linux; Android 8.0.0;) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 Mobile Safari/537.36',
			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36', ##
			'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/72.0',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/72.0',
			'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/72.0',
			'Mozilla/5.0 (Android 8.0.0; Mobile; rv:61.0) Gecko/61.0 Firefox/68.0',
			'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/21.0 Mobile/16B92 Safari/605.1.15'
		 ]
headers = {'User-Agent':choice(uagent)}
mobile_emulation = { "deviceName": "Nexus 10" }

opt = Options()
opt.add_experimental_option('mobileEmulation',mobile_emulation)
opt.add_argument('--incognito')
opt.add_argument('--headless')
opt.add_argument('--disable-gpu')

search = str(input('%sSearch For : %s'%(Fore.LIGHTYELLOW_EX,Fore.LIGHTCYAN_EX)))
n = int(input('%s ↳ How Much Photos : %s'%(Fore.LIGHTYELLOW_EX,Fore.LIGHTCYAN_EX)))
mega = 'https://id.pinterest.com/search/pins/?q=%s&rs=typed'%(search)
loc = 'drivers/chromedriver'
alf = webdriver.Chrome(loc, options=opt)
alf.get(mega)

try:
	os.mkdir('mega-pints')
	os.mkdir('mega-pints/%s'%(search))
except:
	try:
		os.mkdir('mega-pints/%s'%(search))
	except:
		print('',end='')

t = 1
alink = []
op = 0
while True:
	elem = alf.find_elements_by_tag_name('img')
	op += len(elem)
	for k in elem:
		k = k.get_attribute('src').replace('236x','originals')
		if k not in alink:
			alink.append(k)
			if 'AccessDenied' in req.get(k).text:
				k = k.replace('jpg','png')
				if 'AccessDenied' in req.get(k).text:
					k = k.replace('png','gif')
		else:
			continue
		try:
			imgs = req.get(k,headers=headers).content
			rename = k.split('/')[-1:][0]
			with open('mega-pints/%s/%s'%(search,rename),'wb+') as p:
				p.write(imgs)
				p.close()
			if t == 1:
				print('  %s↳ %s. Download %s%s %sCompleted'%(Fore.LIGHTYELLOW_EX,t,Fore.LIGHTCYAN_EX,rename,Fore.LIGHTYELLOW_EX))
			else:
				print('    %s%s. Download %s%s %sCompleted'%(Fore.LIGHTYELLOW_EX,t,Fore.LIGHTCYAN_EX,rename,Fore.LIGHTYELLOW_EX))
			if t >= n:
				break
			op -= 1
			t+=1
		except:
			print('Timeout Waiting 10sec')
			time.sleep(10)
	if t >= n:
		alf.quit()
		break
	else:
		alf.execute_script("window.scrollTo(0, document.body.scrollHeight);")

import pdb; pdb.set_trace()


# '''
# Script By github.com/megatruh
# Credit me for share thanks
# '''
