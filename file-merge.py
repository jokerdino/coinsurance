import pandas as pd

import glob
import os

cwd = os.path.abspath('')
files = glob.glob(cwd + "/*.csv")

df = pd.concat(map(pd.read_csv,files))

df.to_csv('commission-merge.csv',index=False)
