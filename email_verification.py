import smtplib, os, sys, socket, codecs
from smtplib import SMTPException
# import requests
# from random import choice

# desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
#                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
#                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
#                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
#                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
#                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
#                  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
#                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
#                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
#                  'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

# def random_headers():
#     return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

# r = requests.get('http://edmundmartin.com',headers=random_headers())


emails = codecs.open('file_emails.txt','r','utf-8')
# emails = {}
# dict_domains = {}

# for email in file_emails:
# 	if(len(email)==0):
# 		continue

# 	# items = line.split("|")

# 	# domain = items[0].split('@')[1]

# 	# if domain not in dict_domains:
# 	# 	dict_domains[domain] = list()
# 	# dict_domains[domain].append(items[1])

# 	else:
for email in emails:
	print("______________")
	# email = "carsten@samplesolutions.eu"
	maildomain = email.split("@")[-1]
	nstoken = "mail exchanger = "
	mailserver = ""
	m = []
	print("Check mx server ...")
	plines = os.popen("nslookup -type=mx " + maildomain).readlines()
	for pline in plines:
		if nstoken in pline:
			mailserver = pline.split(nstoken)[1].strip()
			mailserver = mailserver.split(" ")[-1] #no need this line in windows env
			m.append(mailserver)
	 
	 
	if mailserver == "":
		print("Unable to get mx server ...", maildomain)
		exit(1)
	else:
		print("Found mx mail... ", m)

	print("Checking e-mail address ....", email)
	for i in m:
		socket.setdefaulttimeout(8)
		try:
			# print("test here")
			s = smtplib.SMTP(i)
			pass
		except socket.timeout:
			print("This mx server time out ", i)
			pass
		except smtplib.SMTPException:
			print("SMTP Exception")
			pass
		except socket.gaierror:
			print("ignoring failed address lookup")
		except:
			print("General exception here")
		else:
			rep1 = s.ehlo()
			if rep1[0] == 250:
				rep2 = s.mail("test@test.com")
				if rep2[0] == 250:
					rep3 = s.rcpt(email)
					if rep3[0] == 250:
						print(email, " valid - mxserver: ", i)
					# if server isn't allowing e-mail add. verification, it's showing the NameError: name 'rep3' is not defined error
					elif rep3[0] == 550:
						print(email, " invalid")
					# added here
					elif rep3[0] == 421:
						print(email, " misdirected request")