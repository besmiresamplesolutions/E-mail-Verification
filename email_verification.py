import codecs
from time import sleep
import os
import socket
import smtplib
import pandas as pd
# from fake_useragent import UserAgent


user_agent_list = [
	# Chrome
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
    # Firefox
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
    # Source: https://free-proxy-list.net/
	'167.99.42.6', 
    '147.135.210.114', 
    '162.246.200.100', 
    '52.187.144.187',
    '213.136.77.246', 
    '35.200.137.2'
]

# emails = [
#     'josmarlie@swinkelsverhoijsen.nl',
#     'hanskroon@home.nl',
#     'rijthove@xs4all.nl', 
#     'bto@kliksafe.nl'
# ]

mail_servers = []
emails_res = []
statuses = []
mx_records = []

emails = codecs.open('file_emails.txt','r','utf-8')
filename = "result_emails.csv"

try:
    f = open(filename, "a")
    f.seek(0)
    f.truncate()
except IOError:
    print("Please close the .csv file in order for changes to append")

def verify_emails():
    for email in emails:
        # First, we get the mail domain from each email
        maildomain = email.split('@')[-1]
        # print(maildomain)

        nstoken = "mail exchanger = "
        mailserver = ""
        # Then, we look for result 
        # Command: nslookup -q=mx [mx server here]
        plines = os.popen("nslookup -type=mx " + maildomain).readlines()

        # If nstoken "mail exchanger = " exists in plines, it means that we found mail server
        for pline in plines:
            if nstoken in pline:
                # We want the 2nd element of plines and that's where mail server is
                mailserver = pline.split(nstoken)[1].strip()
                # No need for this line in windows environment 
                mailserver = mailserver.split(" ")[-1] 
                # Saving our mail servers in a list
                mail_servers.append(mailserver)

        print("E-mail address: ", email)

        # Checking for existing mail servers
        if mailserver == "":
            print("Mail server not found")
        else:
            print("Mail servers: ", mail_servers)

        # After checking for mail server first, then we want to verify e-mails
        
        for element in mail_servers:
            try:
                sleep(3)
                s = smtplib.SMTP(element)
                # HELO method for identifying yourself to SMTP server
                # EHLO - identify yourself to an ESMTP (Enhanced SMTP - protocol extensions) server
                server_respond = s.ehlo()
                if(server_respond[0] == 250):
                    # After getting the respond from server we test if we can send mail
                    mail_respond = s.mail("test@test.com")
                    # print("Mail respond: ", mail_respond)
                    if(mail_respond[0] == 250):
                        resp = s.rcpt(email)
                        print("Response: ", resp)
                        if(resp[0] == 250):
                            status = "OK"
                            print("Status: ", status)
                            emails_res.append(email)
                            statuses.append(status)
                        elif(resp[0] == 550):
                            status = "BAD"
                            print("Status: ", status)
                            emails_res.append(email)
                            statuses.append(status)
                            pass
                        elif(resp[0] == 421):
                            status = "Misdirected Request"
                            print("Status: ", status)
                            emails_res.append(email)
                            statuses.append(status)
                            pass
                        else:
                            status = "Unknown"
                            # print(resp[0])
                            print(resp[0], "Status: ", status)
                            pass
            except socket.timeout:
                print("This MX Server time out ", element)
                continue
            except smtplib.SMTPServerDisconnected:
                print("SMTP Server Disconnected")
                continue
            except socket.gaierror:
                # GAI - getaddrinfo() 
                # This exception means that given hostname is invalid
                print("Ignoring failed address lookup")
                continue
            except smtplib.SMTPException:
                print("SMTP Exception")
                continue
            except:
                print("Probably connection timeout")
            continue

    raw_data = {'E-mail': emails_res,
                'Status': statuses}

    df = pd.DataFrame(raw_data, columns=['E-mail','Status'])
    df = df.drop_duplicates('E-mail')
    df.to_csv(f, index=False)

verify_emails()

# s.close()
f.close()