import pandas as pd
import os

cwd = os.path.abspath('')
files = os.listdir(cwd)

sheet_names = ["CR","PP"]

with pd.ExcelWriter(cwd+'.xlsx') as writer:
    i = 0
    for f in files:
        if f.endswith('_Claims.xlsx'):
            df = pd.read_excel(f)
            df.to_excel(writer, sheet_name = sheet_names[0], index=False)
      #      i = i + 1
        elif f.endswith('_Premium.xlsx'):
            df = pd.read_excel(f)
            df.to_excel(writer, sheet_name = sheet_names[1], index=False)
       #     i = i + 1
