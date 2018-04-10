import smtplib, os, sys, socket, codecs
from smtplib import SMTPException
import pandas as pd
from time import sleep
import requests
import random
from itertools import cycle

user_agent_list = [
	#Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

proxies_list = [
	'167.99.42.6', 
    '147.135.210.114', 
    '162.246.200.100', 
    '52.187.144.187',
    '213.136.77.246', 
    '35.200.137.2'
]

emails_res = []
mx_records = []
statuses = []

proxy_pool = cycle(proxies_list)

emails = codecs.open('file_emails.txt','r','utf-8')

filename = "result_emails.csv"

try:
	f = open(filename, "a")
	f.seek(0)
	f.truncate()
except IOError:
    print("Please close the .csv file in order for changes to append")

# for i in range(1,6):
# 	user_agent = random.choice(user_agent_list)

def verify_emails():
	for email in emails:
		proxy = next(proxy_pool)
		print("______________")
		# email = "carsten@samplesolutions.eu"
		maildomain = email.split("@")[-1]
		nstoken = "mail exchanger = "
		mailserver = ""
		m = []
		print("Checking MX Server")
		# Checking for domain names
		# Command: nslookup -q=mx [mx server here]
		plines = os.popen("nslookup -type=mx " + maildomain).readlines()
		for pline in plines:
			if nstoken in pline:
				mailserver = pline.split(nstoken)[1].strip()
				mailserver = mailserver.split(" ")[-1] # No need this line in windows env
				m.append(mailserver)
		 
		 
		if mailserver == "":
			print("Unable to get MX Server: ", maildomain)
			# exit(1)
			pass
		else:
			print("Found MX mail: ", m)

		print("Checking e-mail address: ", email)
		for i in m:
			socket.setdefaulttimeout(8)
			sleep(3)
			try:
				s = smtplib.SMTP(i)
				pass
			except socket.timeout:
				print("This MX Server time out ", i)
				pass
			except smtplib.SMTPException:
				print(email)
				print("SMTP Exception")
				pass
			except socket.gaierror:
				# GAI - getaddrinfo() 
				# This exception means that given hostname is invalid
				print(email, "Ignoring failed address lookup")
				pass
			except smtplib.SMTPServerDisconnected:
				print("SMTP Server Disconnected")
				pass
			else:
				# Identifying to an ESMTP server
				# Command helo hi / ehlo hi
				rep1 = s.ehlo()
				print(rep1)
				if rep1[0] == 250:
					rep2 = s.mail("test@test.com")
					if rep2[0] == 250:
						rep3 = s.rcpt(email)
						print(rep3)
						if rep3[0] == 250:
							print(email, " valid - mxserver: ", i)
							status = "OK"
							emails_res.append(email)
							statuses.append(status)
							mx_records.append(mailserver)
						# if server isn't allowing e-mail add. verification, it's showing the NameError: name 'rep3' is not defined error
						elif rep3[0] == 550:
							print(email, " invalid")
							status = "Bad"
							emails_res.append(email)
							statuses.append(status)
							mx_records.append(mailserver)
						# added here
						elif rep3[0] == 421:
							print(email, " misdirected request")
							status = "421"
							emails_res.append(email)
							statuses.append(status)
							mx_records.append(mailserver)
							pass
						else:
							status = "on else"
							emails_res.append(email)
							statuses.append(status)
							mx_records.append(mailserver)
							pass
					else:
						status = "on else 2"
						emails_res.append(email)
						statuses.append(status)
						mx_records.append(mailserver)
						pass

	raw_data = {'E-mail': emails_res,
				'Status': statuses,
				'MX Record': mx_records}

	df = pd.DataFrame(raw_data, columns=['E-mail','Status','MX Record'])
	df = df.drop_duplicates('E-mail')
	df.to_csv(f, index=False)

verify_emails()
print(emails_res)
print(statuses)

f.close()