import requests 
from bs4 import BeautifulSoup
import unicodedata


class SoFIFAScrape(object):

	def __init__(self, url):
		self.url = url
		self.root_url = url
		self.num_page = 1
		

	def get_all_rows(self, url):
		
		website = requests.get(url)
		self.soup = BeautifulSoup(website.content, 'html.parser')
		table = self.soup.find('table', attrs = {'class':'table table-hover persist-area'}) 


		body = table.find('tbody', attrs = {'class':'list'})
		all_rows = body.find_all("tr")
		return all_rows


	def get_row(self, row):
		
		name = row.find("div", attrs={"class":"ellipsis"}).text
		pos = row.find("a", attrs={"rel":"nofollow"}).span.text
		age = row.find("td", attrs={"data-col":"ae"}).text
		ova = row.find("td", attrs={"data-col":"oa"}).span.text
		pot = row.find("td", attrs={"data-col":"pt"}).span.text
		team = row.find_all("div", attrs={"class":"ellipsis"})[-1].find("a").text
		contract = row.find_all("div", attrs={"class":"ellipsis"})[-1].find("div", attrs={"class":"sub"}).text
		val = row.find("td", attrs={"data-col":"vl"}).text
		wage = row.find("td", attrs={"data-col":"wg"}).text
		tot = row.find("td", attrs={"data-col":"tt"}).span.text
		

		return (name, pos, age, ova, pot, team, contract, val, wage, tot)


	def get_page_num(self, root_url):
		num_page = 1
		print(root_url)

		while True:
			print(num_page)
			url = root_url if num_page == 1 else f"{root_url}&offset={60*num_page}"
			
			website = requests.get(url)
			soup = BeautifulSoup(website.content, 'html.parser')
			pag = soup.find('div', attrs={'class': 'pagination'})
			#print(pag.find_all("span", attrs={"class": "bp3-button-text"}))
			if pag.find("span", attrs={"class": "bp3-button-text"}):
				if pag.find_all("span", attrs={"class": "bp3-button-text"})[-1].text == "Next": 
					print(pag.find_all("span", attrs={"class": "bp3-button-text"}))
					num_page += 1
				else: 
					break
				
			else: 
				break
				
				
				
		return num_page

	def get_data(self):
		data = {"Name":[],
					 "Positions":[],
					 "Age":[],
					 "OVA":[],
					 "Potential":[],
					 "Team":[],
					 "Contract":[],
					 "Value":[],
					 "Wage":[],
					 "Total":[]
					 }

		for a in  range(self.num_page):
			# print(f"Getting data from page {a+1}")
			# print()
			if a == 0:
				URL = self.url
			else:

				URL = f"{self.url}&offset={60*a}"

			all_rows = self.get_all_rows(URL)
			for i in all_rows:
				a = self.get_row(i)
				#a = map(lambda x : unicodedata.normalize('NFKD', x).encode('ascii', 'ignore'), a)
				(name, pos, age, ova, pot, team, contract, val, wage, tot) = a
				data["Name"].append(name)
				data["Positions"].append(pos)
				data["Age"].append(age)
				data["OVA"].append(ova)
				data["Potential"].append(pot)
				data["Contract"].append(contract.strip("\n"))
				data["Value"].append(val)
				data["Wage"].append(wage)
				data["Total"].append(tot)
				data["Team"].append(team)
		return data