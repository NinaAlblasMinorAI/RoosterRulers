import pandas as pd

zalen_data = pd.read_csv("../data/zalen.csv", delimiter=";")
vakken_data = pd.read_csv("../data/vakken.csv", delimiter=";")

# TODO: sommige namen geven error
# studenten_data = pd.read_csv("data/studentenvakken.csv", delimiter=",")

data = pd.DataFrame(index = zalen_data["Zaalnummber"], columns=vakken_data["Vakken voor periode 4"], data=0)

data.to_csv("../data/roosterdata.csv")