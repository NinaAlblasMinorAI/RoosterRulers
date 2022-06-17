import time
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")


f = open(f"output_data/test{dt_string}.txt", "w")
f.write("Now the file has more content!")
time.sleep(2)
f.close()