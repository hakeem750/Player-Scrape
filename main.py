import warnings
warnings.filterwarnings("ignore")
from sofifa import SoFIFAScrape
from tqdm import tqdm
import pandas as pd
from colorama import Fore




all_data = {"Name":[], "Positions":[], "Age":[], "OVA":[], "Potential":[], "Team":[], "Contract":[], "Value":[], "Wage":[],
					 "Total":[]
					 }
df = pd.DataFrame(all_data)
for i in tqdm(range(0, 333, 1),  desc=Fore.GREEN + "collecting data...", ascii=False, ncols=75):
	
	url = "https://sofifa.com/players" if i == 0 else f"https://sofifa.com/players?offset={60*i}"
	sof = SoFIFAScrape(url)	
	data = pd.DataFrame(sof.get_data())
	
	df = pd.concat([df, data])
	if i % 50 == 0: print(df.shape)


print(df.shape)
df.to_csv(f"players.csv", index=False)
print()
print(Fore.GREEN + "Complete. . .") 