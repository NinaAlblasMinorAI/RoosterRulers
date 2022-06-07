import pandas as pd

zalen_data = pd.read_csv("../data/zalen.csv", delimiter=";")
vakken_data = pd.read_csv("../data/vakken.csv", delimiter=";")

# TODO: sommige namen geven error
# studenten_data = pd.read_csv("data/studentenvakken.csv", delimiter=",")

tijdslots = ["Maandag 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
            "Dinsdag 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
            "Woensdag 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
            "Donderdag 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
            "Vrijdag 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", ]

data = pd.DataFrame(index = tijdslots, columns=zalen_data["Zaalnummber"], data=0)

# # welke lokalen vrij op maandag 9-11?
# sub_df = (data.iloc[0] == 0)
# print(sub_df)

data.to_csv("../data/roosterdata.csv")