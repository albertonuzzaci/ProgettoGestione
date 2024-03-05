import requests
from bs4 import BeautifulSoup

#url = "https://www.booking.com/reviewlist.en.html?cc1=al&pagename=virginia&dist=1&offset=0&rows=10"
url = "https://www.airbnb.com/rooms/15400/reviews"
#originalUrl = "https://www.booking.com/reviewlist.it.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaHGIAQGYARS4ARfIAQzYAQHoAQH4AQuIAgGoAgO4AtDXka8GwAIB0gIkZjRmNTEzY2EtNjZhOC00ZDhkLWI2MDEtZTA4NzYyYjQxMmJm2AIG4AIB&;cc1=it&pagename=campo-di-marte-80&type=total&dist=1&offset=0&rows=100"

payload = {}
headers = {
  #'authority': 'www.booking.com',
  #'accept': '*/*',
  #'accept-language': 'it-IT,it;q=0.6',
  #'cookie': 'px_init=0; bkng_sso_auth=CAIQsOnuTRpmV2k+envtkbKuVw2/Xd0DCVowrqTYz2am7wEyWmzKB6m6Jl29NeVffHUTYZgLnj6cTovhHqmWXU8xYJEzefX5hpdrQciZig0rNQqyu0/vVnby4ZD3DlkYeJWEOGOJUy/ta7ZnxCoC; pcm_consent=analytical%3Dfalse%26countryCode%3DIT%26consentId%3Dec191ee5-4353-43c7-bb84-5bf45792a87d%26consentedAt%3D2024-03-03T12%3A23%3A44.002Z%26expiresAt%3D2024-08-30T12%3A23%3A44.002Z%26implicit%3Dtrue%26marketing%3Dfalse%26regionCode%3D45%26regulation%3Dgdpr%26legacyRegulation%3Dgdpr; cors_js=1; bkng=11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLbca8KLfxLPecqsLgaWy1uTC17wFMG9V9anRSt6fKI6hqZvPJW4oWW6cx%2F6WAXuw5YvZqXT9%2FECYNACdxUaDZPe1KadQmlKbthTOR8DLx2DKXQ6kwfmv6G%2FudyLv4UrhPB%2F78O59iC0RB0KIAo74T2YaCOq%2FtSOJZERdTE%2B7Lv2dw%3D; aws-waf-token=e6e5440a-ac63-4a52-995d-85c2142e6e95:DgoAdF9WABMAAQAA:VAm+FyAs2+Vu/LQfm/cwUQESKoDnJZmJeU+pDsFdIhaAWn8Blj0BZk6ycRJxgLhp6CQj7s7qouyQndWyuN7Fi4riXzGqgWf84DvfkB+KqJ42POuDYE4Y18mj2FYpCKw1qdedlaCrSeiQ5oXGiS/KzQKyNbMOIe+yPSzb9PXdzcUyI3gaHzmw7zqSTIZMhaTuLefDGKg9CnumrCMRSg34zYW5jgUW4zR6YOOD3LeytH8D75V+uinaoZX9tXIQ/XvBjQqhabGs; lastSeen=0; bkng=11UmFuZG9tSVYkc2RlIyh9Yaa29%2F3xUOLbnmKTRaewPBsuMQ0XSfpL3Jb7DPLKSFEzD54w%2Fr%2Br1BwY8W9iYZ4bSVd%2F%2B6rEqB8xI34xhtHd1SazKZuffNbgsLdZRR53akQhs7aKBffqAtQerdemsuNEiUKxUS9w26A4vZOtzo3sDSYvYf%2Bwnn7CUUyHUfqpQOQaj11Ci%2BS%2F7Q0%3D; pcm_consent=analytical%3Dtrue%26countryCode%3DUS%26consentId%3D33c1a0fa-65b7-4e55-b4f5-cd4e4166afc0%26consentedAt%3D2024-03-03T12%3A34%3A17.940Z%26expiresAt%3D2024-08-30T12%3A34%3A17.940Z%26implicit%3Dtrue%26marketing%3Dtrue%26regulation%3Dnone%26legacyRegulation%3Dnone; px_init=0',
  #'referer': 'https://www.booking.com/hotel/it/campo-di-marte-80.it.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaHGIAQGYARS4ARfIAQzYAQHoAQH4AQuIAgGoAgO4AtDXka8GwAIB0gIkZjRmNTEzY2EtNjZhOC00ZDhkLWI2MDEtZTA4NzYyYjQxMmJm2AIG4AIB&sid=2682f93c222e0a70efb60a29915eee9d&dest_id=-126693;dest_type=city;dist=0;group_adults=2;group_children=0;hapos=5;hpos=5;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;srepoch=1709468642;srpvid=3fbf572c67d80208;type=total;ucfs=1&',
  #'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
  #'sec-ch-ua-mobile': '?0',
  #'sec-ch-ua-platform': '"Windows"',
  #'sec-fetch-dest': 'empty',
  #'sec-fetch-mode': 'cors',
  #'sec-fetch-site': 'same-origin',
  #'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  #'x-booking-aid': '2311236'
  #'x-booking-client-info': 'TDXbETfZHfLebbMIGDC|1,TDXbETfZHfLebbMIGDC|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|1,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|5,NAREFeDUfJTcfODbLWZHOfYO|2,eWHMeDUfTLKGBfSeCXYTZccCcCcCC|1,eWHMeDUfTLKGBfSeCXYTZccCcCcCC|2,adUAAIFacafWbBMRVSUPebBGRTdZSGEBYJO|1,adUAAIFacafWbBMRVSUPebBGRTdZSGEBYJO|6',
  #'x-booking-csrf': 'IqTkZQAAAAA=MkVzuG7G8Cd2x29EfqPTziyfN2pdcymuCVbJ3A7e_6nfYm-yrQAaGi8av_eJgdHToHnEWEc6pQGZqr0inXKSgouE7PiQiykl42q_EopUKMRp8UGWQs96uw6hyuMTeYgG6xxLpFrZnHqOzJoWi9GtTeCVupTXI6YlVZNlaGNflvTgNeF_HHO7Xr0_18Fjv7wzo_sjUAPGUNK9xo1I',
  #'x-booking-info': '1870450,1897690,1899310,1906250,1909040,1914350,1916800,1921930,1922810,1923100,1926080,1927060,1928220,1932480,eWHMeDUbWNPUWRFKYOeeIXCDAPSHGZTLbQOUJBNRAZYGHVODKe|1,TDXbETfZHfLebbMIGDC|1,TDXbETfZHfLebbMIGDC|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|1,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|3,THHSOFRURURYNYHIYTLRQJRbWdWOGVO|5,NAREFeDUfJTcfODbLWZHOfYO|2,eWHMeDUfTLKGBfSeCXYTZccCcCcCC|1,eWHMeDUfTLKGBfSeCXYTZccCcCcCC|2,adUAAIFacafWbBMRVSUPebBGRTdZSGEBYJO|1,1932480|1,1922810|1,1927060|2,1928220|1,1927060|4,adUAAIFacafWbBMRVSUPebBGRTdZSGEBYJO|6,YTBUIHOdVMYCMTdXSbDbFCeVO|1,YTBUIHOdVMYCMTdXSbDbFCeVO|3,YTBUIHOdVMYCMTdXSbDbFCeVO|4,YTTHbXeeVJWcFKJPFNJQVVEbMKXe|1,YTTHbXeeVJWcFKJPFNJQVVEbMKXe|5,bPFPOKZfHfVaAFZKVHJbdYeNeHT|1,bPFPOKZfHfVaAFZKVHJbdYeNeHT|2,aXTfOFJZMYeKTcBUTeSSTUPIMLefNDRYTfUWRC|1,TZUfONebEWAUFccRMVIZdRRT|1,OOGbIFBUEDUJfYcPBPUObeZFZVTHT|1,OOGbIFBUbTdNDNQJYBXe|1,eWHMcCcCcCSYeJTUDXJEBfPDIbEfKFWUC|1,YTTHbXeeVeCFZAcbRbROfLMTeCYHDRFcO|4,cCHObTPeVaAJDbGSRaPSZYPRbdDXO|1,cCHObTPeVaAJDbGSRaPSZYPRbdDXO|2,aXTfOFJZMYeKTcBUABVYUdBNETOJabeQcJPQPVacDAPVFfC|1,HINZJLeUXSaZbdKNKNKHYYfPNRAPLSIfJdYO|1,HINZJLeUXSaZbdKNKNKHYYfPNRAPLSIfJdYO|3,OOGbIFBUbTdNDNQJYBXe|3,OOGbIFBUbTdNDNQJYBXe|4,OOGbIFBUbTdNDNQQAC|3,OOGbIFBUEDUJfYcPBPUObeZFZVTHT|3,OOGbIFBUbTdNDNQQAC|6,YTTHbXeeVJWcFKJPFNJQVVEbMKXe|6,adUAVYCIFBUYWBbQCeLFKMOAEXaDBUcRe|3,eWHMcCcCcCSYeJTUDXJEBfPDIbEfKFWUC|2,eWHMcCcCcCSYeJTUDXJEBfPDIbEfKFWUC|3,eWHMcCcCcCSYeJTUDXJEBfPDIbEfKFWUC|4,YdXfMObWJZLBKBaUecUUWe|1,YdXfMObWJZLBKBaUecUUWe|2,aXTfOFJZMYeKTcBUABVYUdBNETOJabeQcJPQPVacDAPVFfC|2,eWfaQJVfYceDFbZNRTKeeHRbdFIKe|1,NAREFeDUaRHCSAZeODMQHO|1,NAREFeDUaRHCSAZeODMQHO|3,NAREFeDUaRHCSAZeODMQHO|4',
  #'x-booking-label': 'gen173nr-1FCAEoggI46AdIM1gEaHGIAQGYARS4ARfIAQzYAQHoAQH4AQuIAgGoAgO4AtDXka8GwAIB0gIkZjRmNTEzY2EtNjZhOC00ZDhkLWI2MDEtZTA4NzYyYjQxMmJm2AIG4AIB',
  #'x-booking-language-code': 'it',
  #'x-booking-pageview-id': 'db055731abff00a6',
  #'x-booking-session-id': '2682f93c222e0a70efb60a29915eee9d',
  #'x-booking-sitetype-id': '1',
  #'x-partner-channel-id': '3',
  #'x-requested-with': 'XMLHttpRequest'
}

response = requests.request("GET", url, headers=headers, data=payload)

'''
soup = BeautifulSoup(response.text, 'html.parser')


reviews = []
for i in soup.find_all("li", {"class":"review_list_new_item_block"}):
	
	reviewTxt = "Name " + i.find("span",{"class":"bui-avatar-block__title"}).get_text()

	for k in i.find_all("span", {"class":"c-review__body"}):
		reviewTxt += "\n"+ k.get_text() + " "
	reviews.append(reviewTxt)

for c, i in enumerate(reviews):
	print(f"----------Recensione {c}----------")
	print(i)
	print("\n")

print(len(reviews))
'''
with open("risposta.txt","w", encoding="utf-8") as f:
	f.write(response.text)