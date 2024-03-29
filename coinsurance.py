import pandas as pd


# reading files from the saved directory and saving it into pandas dataframe

df_1 = pd.read_csv('premium-payable.csv',converters={'TXT_FOLLOWER_OFF_CD':str})

df_1["COMPANYNAME"] = df_1["COMPANYNAME"].astype('category')
df_2 = pd.read_csv('commission-merge.csv')
df_3 = pd.read_csv('tpa-register.csv')
df_premium_data  = pd.read_csv('premium_data.csv')

# deleting the # character from the Policy no. column
df_premium_data["Policy No."] = df_premium_data["Policy No."].str.replace("#","")

df_1["COMPANYNAME"] = df_1["COMPANYNAME"].str.replace(".","")
df_1["COMPANYNAME"] = df_1["COMPANYNAME"].str.rstrip()

# filling the percentage column with no values with "Deleting" and then identifying the policy numbers which have that values and deleting them

# reason: these policies likely were underwritten with coinsurance share and subsequently were removed. hence, we are removing them from the dataframe itself
# note: we are still exporting them to an excel file for reference: deleted_first.xlsx

df_1['NUM_SHARE_PCT'].fillna("Deleting",inplace=True)

df_deleting = df_1[df_1['NUM_SHARE_PCT'] == "Deleting"]

list_policy = df_deleting['TXT_POLICY_NO_CHAR'].unique()

for i in list_policy:
    #df_1 = df_1[df_1["TXT_POLICY_NO_CHAR"] != i]
    df_delete = df_1[df_1["TXT_POLICY_NO_CHAR"] == i]
    df_1 = df_1[df_1["TXT_POLICY_NO_CHAR"] != i]

# dropping duplicate rows in file 2 and file 3

#df_2 = df_2.drop_duplicates(["Policy No"])
#df_3 = df_3.drop_duplicates(["Policy No"])

#df_premium_data.rename({"End. S.No." : "Endorsement No"}, inplace=True)

# converting the accounting date column and transaction date column to datetime format
df_1['DAT_ACCOUNTING_DATE'] = pd.to_datetime(df_1['DAT_ACCOUNTING_DATE'], format="mixed")

df_premium_data['Trn Date'] = pd.to_datetime(df_premium_data['Trn Date'])

# merging the four dataframes based on policy numbers, endorsement numbers and accounting date
df_combine = df_1.merge(df_premium_data,left_on=("TXT_POLICY_NO_CHAR","NUM_ENDT_NO","DAT_ACCOUNTING_DATE"),right_on=("Policy No.","End. S.No.","Trn Date"),how="left")

df_combine = df_combine.merge(df_2, left_on=("TXT_POLICY_NO_CHAR","NUM_ENDT_NO"),right_on=("Policy No","Endorsement No"), how="left")
df_combine = df_combine.merge(df_3,left_on=("TXT_POLICY_NO_CHAR","NUM_ENDT_NO"),right_on=("Policy No","Endorsement No"),how="left")

# using the premium data, we are converting our share into 100% share for further processing

df_combine['Full premium'] = df_combine['Premium W/o Terr'] * 100 / df_combine['Own Share']
df_combine['Full Terr.Premium'] = df_combine['Terr.Premium'] * 100 / df_combine['Own Share']

# Arriving values of TPA service charges, Admin charges and brokerage charges at the end of the pandas dataframe

df_combine.rename(columns={'TPA Service Charge %':'TPA_Rate'},inplace=True)
df_combine['TPA_Rate'] = df_combine.TPA_Rate.astype(float)
df_combine['TPA'] = df_combine['PREMIUM'] * df_combine['TPA_Rate']/100
df_combine['Admin_charges']=df_combine['PREMIUM']*1.18/100

# as we now have terrorism premium and premium except terrorism, it becomes easier to accurately calculate brokerage
# we therefore use the 100% premium data and calculate the brokerage for the coinsurer share
df_combine["Terrorism Premium"] = df_combine['Full Terr.Premium'] * df_combine['NUM_SHARE_PCT'] / 100
df_combine["Other than Terrorism Premium"] = df_combine['PREMIUM'] - df_combine['Terrorism Premium']

df_combine['Terr brokerage']  = df_combine['Full Terr.Premium'] * 5 / 100 * df_combine['NUM_SHARE_PCT'] / 100
df_combine['Brokerage except Terrorism'] = df_combine['Full premium'] * df_combine['Rate'] / 100 * df_combine['NUM_SHARE_PCT'] / 100

# adding brokerage except terrorism and terrorism brokerage
df_combine['Total brokerage'] = df_combine['Terr brokerage'] + df_combine['Brokerage except Terrorism']


# fill empty cells in the dataframe with zeros
# this is done because net premium payable arithmetic is not functioning if the columns have no values

df_combine.fillna(0, inplace=True)

# calculating Net premium payable from subtracting from premium, brokerage charges, TPA service charges and admin charges

df_combine['Net Premium Payable'] = df_combine['PREMIUM'] - df_combine['Total brokerage']-df_combine['TPA']-df_combine['Admin_charges']

# deleting all columns starting with "aggrega"
df_combine.drop(df_combine.filter(regex='Aggrega').columns, axis=1, inplace=True)



# deleting some more columns from the dataframe
df_combine["NUM_VOUCHER_NO"] = '\''+df_combine["NUM_VOUCHER_NO"].astype(str)

df_combine = df_combine.drop(columns=['TXT_LEADER_COMPANY_CODE','TXT_FOLLOWER_COMPANY_CODE','NUM_DEPARTMENT_CODE','NUM_TPA_SER_CHARGE_SHARE','CUR_ADMIN_CHARGE'])

# reordering all the columns in the dataframe

df_combine = df_combine[['TXT_UIIC_OFFICE_CD','COMPANYNAME','TXT_FOLLOWER_OFF_CD','TXT_NAME_OF_INSURED','TXT_DEPARTMENTNAME','TXT_POLICY_NO_CHAR','NUM_ENDT_NO','DAT_POLICY_START_DATE','DAT_POLICY_END_DATE','NUM_VOUCHER_NO','DAT_ACCOUNTING_DATE','NUM_SHARE_PCT','CUR_SUM_INSURED','TXT_URN_CODE','PREMIUM','Terrorism Premium','Other than Terrorism Premium','Rate','Terr brokerage', 'Brokerage except Terrorism','Total brokerage','TPA_Rate','TPA','Admin_charges','Net Premium Payable']]

# Renaming the column names in the dataframe

df_combine = df_combine.set_axis(["UIIC Office Code","Name of coinsurer","Follower Office Code","Name of insured","Department","Policy Number","Endorsement number","Policy start date","Policy end date","Voucher number","Accounting date","Percentage of share","Current sum insured","URN Code","Premium","Terrorism Premium","Other than Terrorism Premium","Brokerage rate","Terrorism brokerage (5%)","Brokerage except Terrorism", "Total Brokerage amount","TPA Service Charges rate","TPA Service Charges amount","Admin charges (incl. GST)","Net Premium payable"],axis=1,copy=False)


# Converting date format for policy start date, end date and voucher date

df_combine['Policy start date'] = pd.to_datetime(df_combine['Policy start date'], format="mixed")
df_combine['Policy end date'] = pd.to_datetime(df_combine['Policy end date'], format="mixed")
df_combine['Accounting date'] = pd.to_datetime(df_combine['Accounting date'], format="mixed")

#df_combine['Policy start date'] = df_combine['Policy start date'].dt.strftime("%d/%m/%Y")

# writing the final excel file to combine.xlsx

#df_combine.to_excel("step.xlsx")

# copying the duplicate rows into an excel file for reference
duplicates = df_combine[df_combine.duplicated() == True]

# deleting the duplicate rows because why not
df_combine.drop_duplicates(keep='first',inplace=True)

# exporting the final dataframe back into excel file
df_combine.to_excel('combine.xlsx')

# exporting the earlier deleted dataframe into excel file for reference

#TODO: Commenting this line out because there are no reverse coinsurance entries in this data lot
#df_delete.to_excel('deleted_first.xlsx')

# exporting duplicate rows into excel file for reference
duplicates.to_excel('deleted.xlsx')

# All unique values in "Name of coinsurer" column to be split into individual excel files


coinsurer_name = df_combine["Name of coinsurer"].unique()


for i in coinsurer_name:
    a = df_combine[df_combine["Name of coinsurer"].str.contains(i)]
    a.to_excel(i+"_Premium.xlsx",index=False)
