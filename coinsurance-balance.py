#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from babel.numbers import format_currency

np.warnings.filterwarnings('ignore')
pd.options.display.float_format = '{:,.2f}'.format

gl_balance = pd.read_csv("UIIC - ICR - Client.csv")
gl_balance.columns = gl_balance.columns.str.replace(' ','_')

coinsurance = gl_balance[gl_balance.GL_Desc.str.contains('CO-INS')]

coinsurance.loc[coinsurance['GL_Desc'].str.contains('DUE TO'), 'Type'] = 'Due to'
coinsurance.loc[coinsurance['GL_Desc'].str.contains('DUE FROM'), 'Type'] = 'Due from'

coinsurance['Net'] = coinsurance['Debit'] - coinsurance['Credit']

coinsurance.loc[coinsurance['Type'] == "Due to", "Net"] = coinsurance['Net'] * -1

coinsurance['GL_Desc'] = coinsurance['GL_Desc'].str.replace(r"^.*CO-INS ","",regex=True)
coinsurance['GL_Desc'] = coinsurance['GL_Desc'].str.replace(r"Insurance.*","",regex=True)

table = pd.pivot_table(coinsurance, values = 'Net', index=['GL_Desc'], columns='Type')

table["Net payable"] = table['Due to'] - table['Due from']
table = table.dropna()
table = table[table['Net payable']!=0]
table.loc['Total']= table.sum(numeric_only=True,axis=0)

table.to_excel('file.xlsx')
table[['Due to', 'Due from','Net payable']] = table[['Due to', 'Due from', 'Net payable']].applymap(
    lambda v: format_currency(v, 'INR'),
)

print(table)
