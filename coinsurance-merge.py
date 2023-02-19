import pandas as pd
import glob
import os

cwd = os.path.abspath('')
filenames = glob.glob(cwd + "/*.xlsx")

output_premium = pd.DataFrame()
output_claims = pd.DataFrame()

for file in filenames:
    try:
        df_premium = pd.read_excel(file, sheet_name = "PP", converters={'Follower Office Code':str})

        output_premium = pd.concat([output_premium, df_premium])
    except ValueError as e:
        print("No PP")
    try:
        df_claims = pd.read_excel(file, sheet_name = "CR", converters={'Follower Office Code':str})
        output_claims = pd.concat([output_claims, df_claims])
    except ValueError as e:
        print("No CR")

with pd.ExcelWriter("File_merge.xlsx") as writer:
    output_premium.sort_values('Accounting date').to_excel(writer, sheet_name="PP", index=False)
    output_claims.sort_values('Voucher date').to_excel(writer, sheet_name="CR",index=False)
