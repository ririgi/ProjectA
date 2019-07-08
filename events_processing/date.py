import warnings
warnings.filterwarnings("ignore")

import sys
sys.path.append("../")

import re
import os
import time
import pandas as pd
import numpy as np

from preprocessing.utils import readChunk, toCSV

data_dir = "../../events/2018/12"
cols = ["USERID", "SESSIONID", "SESSION_STARTDT", "SESSION_ENDDT"]
def removeNotLoggedIn(df):
	df["loggedin"] = df[["USERID", "PRIMARY_FINGERPRINT"]].apply(lambda x: 0 if re.search(x[1], x[0]) else 1, axis = 1)
	return df

s = time.time()
count = 0
for f in os.listdir(data_dir):
	count = count+1
	print("Extracting cols for: ", f)
	df = readChunk(os.path.join(data_dir, f))
	df["USERID"] = df["USERID"].astype(str)
	df["PRIMARY_FINGERPRINT"] = df["PRIMARY_FINGERPRINT"].astype(str)
	df = removeNotLoggedIn(df)
	print("all users: ", len(df))
	df = df.loc[df.loggedin == 1]
	print("logged in users: ", len(df))
	df = df[cols]
	outfile = os.path.join("../../events/rfm/december", f[-12:])
	toCSV(df, outfile)
e = time.time()
total_time = time.strftime("%H:%M:%S", time.gmtime(e-s))
print("Finish extracting all cols: ", total_time)

# userid = "9479A9C164A4C32676CBD502BE91664B_175.158.211.49"
# primary_fingerprint = "9479A9C164A4C32676CBD502BE91664B"

# if re.search(primary_fingerprint, userid):
# 	print(0)
# else:
# 	print(1)