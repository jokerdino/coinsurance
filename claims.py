import pandas as pd

df_claims = pd.read_csv('CR.csv')

# rearranging the columns to our preference

df_claims['Total claim amount'] = df_claims['LOSS_AMOUNT'] + df_claims['EXPENSE_AMOUNT']

df_claims['DAT_LOSS_DATE'] = pd.to_datetime(df_claims['DAT_LOSS_DATE'], infer_datetime_format=True)
df_claims['DAT_ACCOUNTING_DATE'] = pd.to_datetime(df_claims['DAT_ACCOUNTING_DATE'], infer_datetime_format=True)

df_claims['COMPANYNAME'] = df_claims['COMPANYNAME'].str.replace(".",'',regex=True)

df_claims['DAT_LOSS_DATE'] = df_claims['DAT_LOSS_DATE'].dt.date
df_claims['DAT_ACCOUNTING_DATE'] = df_claims['DAT_ACCOUNTING_DATE'].dt.date

df_claims = df_claims[['TXT_UIIC_OFF_CODE','COMPANYNAME','TXT_LEADER_OFFICE_CODE','TXT_NAME_OF_INSURED','TXT_DEPARTMENTNAME','TXT_POLICY_NO_CHAR','TXT_MASTER_CLAIM_NO','DAT_LOSS_DATE','TXT_NATURE_OF_LOSS','LOSS_AMOUNT','EXPENSE_AMOUNT','Total claim amount','NUM_VOUCHER_NO','DAT_ACCOUNTING_DATE','TXT_URN_CODE']]

df_claims = df_claims.set_axis(['UIIC Office Code','Name of coinsurer','Follower Office Code','Name of receiver','Department','Policy Number','Claim Number','Date of loss','Cause of loss','Loss amount','Expense amount','Total claim amount','Settlement voucher number','Voucher date','URN Code'],axis=1,inplace=False)

df_claims['Settlement voucher number'] = '\''+ df_claims['Settlement voucher number'].astype(str)

# All unique values in "Name of coinsurer" column to be split into individual excel files
coinsurer_name = df_claims["Name of coinsurer"].unique()


for i in coinsurer_name:
    a = df_claims[df_claims["Name of coinsurer"].str.contains(i)]
    a.to_excel(i+"_Claims.xlsx",index=False)
