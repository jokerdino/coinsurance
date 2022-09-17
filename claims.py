import pandas as pd

df_claims_reports = pd.read_csv('claims-receivable.csv')
df_claims_data = pd.read_csv('claims_data.csv')

df_claims_data["Policy Number"] = df_claims_data["Policy Number"].str.replace("#","")

df_claims_data = df_claims_data.drop_duplicates(subset=["Policy Number"])
# rearranging the columns to our preference

df_claims = df_claims_reports.merge(df_claims_data,left_on=("TXT_POLICY_NO_CHAR"),right_on=("Policy Number"),how="left")

#df_claims['Total claim amount'] = df_claims['LOSS_AMOUNT'] + df_claims['EXPENSE_AMOUNT']


df_claims['Total claim amount'] = df_claims['CUR_DEBIT_BALANCE'] - df_claims['CUR_CREDIT_BALANCE']


df_claims['DAT_LOSS_DATE'] = pd.to_datetime(df_claims['DAT_LOSS_DATE'], infer_datetime_format=True)
df_claims['DAT_ACCOUNTING_DATE'] = pd.to_datetime(df_claims['DAT_ACCOUNTING_DATE'], infer_datetime_format=True)
df_claims['Policy From'] = pd.to_datetime(df_claims['Policy From'], infer_datetime_format=True)
df_claims['Policy Upto'] = pd.to_datetime(df_claims['Policy Upto'], infer_datetime_format=True)

df_claims['COMPANYNAME'] = df_claims['COMPANYNAME'].str.replace(".",'',regex=True)
df_claims["COMPANYNAME"] = df_claims['COMPANYNAME'].str.rstrip()


df_claims['DAT_LOSS_DATE'] = df_claims['DAT_LOSS_DATE'].dt.date
df_claims['DAT_ACCOUNTING_DATE'] = df_claims['DAT_ACCOUNTING_DATE'].dt.date
df_claims['Policy From'] = df_claims['Policy From'].dt.date
df_claims['Policy Upto'] = df_claims['Policy Upto'].dt.date

df_claims = df_claims[['TXT_UIIC_OFF_CODE','COMPANYNAME','TXT_LEADER_OFFICE_CODE','Customer Name','TXT_DEPARTMENTNAME','TXT_POLICY_NO_CHAR','Policy From','Policy Upto','NUM_SHARE_PCT','TXT_MASTER_CLAIM_NO','DAT_LOSS_DATE','TXT_NATURE_OF_LOSS','Total claim amount','NUM_VOUCHER_NO','DAT_ACCOUNTING_DATE','TXT_URN_CODE']]

df_claims = df_claims.set_axis(['UIIC Office Code','Name of coinsurer','Follower Office Code','Name of insured','Department','Policy Number','Policy start date','Policy end date','Percentage of share','Claim Number','Date of loss','Cause of loss','Total claim amount','Settlement voucher number','Voucher date','URN Code'],axis=1,inplace=False)

df_claims['Settlement voucher number'] = '\''+ df_claims['Settlement voucher number'].astype(str)

# All unique values in "Name of coinsurer" column to be split into individual excel files
coinsurer_name = df_claims["Name of coinsurer"].unique()


for i in coinsurer_name:
    a = df_claims[df_claims["Name of coinsurer"].str.contains(i)]
    a.to_excel(i+"_Claims.xlsx",index=False)
