from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests as req
import time
from random import choice
import os
from tqdm.auto import tqdm
import shutil
from sys import argv
columns = shutil.get_terminal_size().columns


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

class Pints:

	def __init__(self,search,amount,headless=True):
		self.opt = Options()
		# self.opt.add_experimental_option('mobileEmulation',mobile_emulation)
		self.opt.add_argument('--incognito')
		if headless:
			self.opt.add_argument('--headless')
		self.opt.add_argument('--disable-gpu')
		self.opt.add_experimental_option('excludeSwitches', ['enable-logging'])
		self.search = search
		self.amount = amount

		self.loc='drivers/chromedriver'
		self.link = 'https://id.pinterest.com/search/pins/?q=%s&rs=typed'%(self.search)
		self.alf = webdriver.Chrome(self.loc, options=self.opt)
		self.alf.get(self.link)
		# self.alf.execute_script('window.open(""), "new window"')
		# self.alf.switch_to.window(driver.window_handles[0])

	def mkdirs(self):
		try:
			os.mkdir('result')
			os.mkdir('result/%s'%(self.search))
		except:
			try:
				os.mkdir('result/%s'%(self.search))
			except:
				print('',end='')

	def scan(self):
		alink = []
		cln = []
		i = 1
		while True:
			elem = self.alf.find_elements_by_tag_name('img')

			for k in elem:
				try:
					if '75x75_RS' in k.get_attribute('src'):
						k = k.get_attribute('src').replace('75x75_RS','originals')
					else:
						k = k.get_attribute('src').replace('236x','originals')

					named = k.split('/')[-1]
					print('%s/%s : %s'%(i,self.amount, named))

					i+=1

					# self.alf.switch_to.window(self.alf.window_handles[1])

					if k not in alink:
						alink.append(k)
						if 'i.pinimg.com' not in req.get(k).text:
							k = k.replace('jpg','png')
							if 'i.pinimg.com' not in req.get(k).text:
								k = k.replace('png','gif')
								
						cln.append(k)

					if len(cln) >= self.amount:
						break

				except:
					print("\nCheck Your Connection, Try Again !")
					# print("Skip",end=" ")
					self.quit()
					exit()
					# continue

			if len(cln) >= self.amount:
				print('\n')
				break
			else:
				self.alf.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		self.quit()

		return cln	

	def save(self,link):
		# link = self.clean()
		self.mkdirs()
		for i in tqdm(range(len(link)),desc='Downloading',unit_scale=True):
			k = link[i]
			imgs = req.get(k,headers=headers).content
			rename = k.split('/')[-1:][0]
			with open('result/%s/%s'%(self.search,rename),'wb+') as p:
				p.write(imgs)
				p.close()
		print('\n')

	def quit(self):
		self.alf.quit()

def start():
	os.system('cls')
	print()
	print('| [github.com/algatra] - pinterest scraper |'.center(columns,'-'))
	search = str(input("-> Search For : "))
	amount = int(input("   -> Amount : "))
	print('| Scanning . . . |'.center(columns,'-'))

	try:
		if 'false' in str(argv).lower():
			run = Pints(search,amount,False)
		else:
			run = Pints(search,amount)
	except:
		print("Check Your Connection")
		exit()

	pas = run.scan()
	print('| Downloading . . . |'.center(columns,'-'))
	run.save(pas)

	print('| Done ! |'.center(columns,'-'))

if __name__ == '__main__':
	start()