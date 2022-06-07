import pandas as pd

vakken_data = pd.read_csv('../data/vakken.csv', delimiter=";")
vakken = list(vakken_data["Vakken voor periode 4"])
print(vakken) 

rooster_data = pd.read_csv('../data/roosterdata.csv')
print(rooster_data) 

x = 1
y = 0
for vak in vakken:
    rooster_data.iloc[y,x]= vak
    x += 1
    if x == 8:
        y += 1
        x = 1

print(rooster_data) 

rooster_data.to_csv("../data/roosterdata_baseline.csv")