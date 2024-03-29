import pandas as pd
import numpy as np
import os
import sys

if len(sys.argv) > 1:
    bool_receivable = True

cwd = os.path.abspath('')
files = os.listdir(cwd)

file_name = ''

for f in files:
    if f.endswith('.xlsx'):
        excel_file = pd.ExcelFile(f)
        file_name = f

try:
    df1 = pd.read_excel(excel_file,'CR',converters={'Follower Office Code': str})
except ValueError:
    df1 = pd.DataFrame()
    print("There is no claims receivable sheet for this company.")
try:
    df2 = pd.read_excel(excel_file, 'PP',converters={'Follower Office Code':str})
except ValueError:
    df2 = pd.DataFrame()
    print("There is no premium payable sheet for this company.")
pd.set_option('display.float_format', '{:,.2f}'.format)

if not df1.empty:
    CR = pd.pivot_table(df1,index='Follower Office Code',values='Total claim amount',aggfunc=np.sum)#,margins=True)
else:
    CR = pd.DataFrame()
if not df2.empty:
    PP = pd.pivot_table(df2,index='Follower Office Code',values='Net Premium payable',aggfunc=np.sum)#,margins=True)
else:
    PP = pd.DataFrame()

if not PP.empty:
    if not CR.empty:
        all_pivot = pd.merge(PP,CR,left_index=True,right_index=True,how='outer')

        all_pivot.fillna(0,inplace=True)
        if len(sys.argv) > 1:
            all_pivot['Net Receivable by UIIC'] = all_pivot['Total claim amount'] - all_pivot['Net Premium payable']
            all_pivot.style.format({'Net Receivable by UIIC':'{0:,.2f}'})
        else:
            all_pivot['Net Payable by UIIC'] = all_pivot['Net Premium payable'] - all_pivot['Total claim amount']
            all_pivot.style.format({'Net Payable by UIIC':'{0:,.2f}'})
        all_pivot.rename({'Total claim amount': 'Claims receivable'},axis=1,inplace=True)
    else:
        all_pivot = PP
else:
    all_pivot = CR


all_pivot.loc['Total']= all_pivot.sum(numeric_only=True,axis=0)
#pd.set_option('display.float_format','{:.2f}'.format)

#all_pivot.style.format({'Net Payable by UIIC':'{0:,.2f}'})

print(all_pivot)
#all_pivot.style.format({'Net Payable by UIIC':'${0:,.0f}'})



writer_1 = pd.ExcelWriter("Summary.xlsx",engine='xlsxwriter')
all_pivot.to_excel(writer_1,sheet_name="Summary")
#writer_1.save()
workbook_1 = writer_1.book
worksheet_1 = writer_1.sheets['Summary']

format_currency = workbook_1.add_format({
    "num_format": "##,##,#0"
    })
format_bold = workbook_1.add_format({
    "num_format": "##,##,#","bold":True
    })
format_header = workbook_1.add_format({
    'bold':True,
    'text_wrap':True,
    'valign':'top'

    })



worksheet_1.set_column("D:D",12,format_bold)
worksheet_1.set_column("B:C",12,format_currency)


worksheet_1.set_row(-1,12,format_bold)

worksheet_1.set_row(0,None,format_header)
#for col, value in enumerate(all_pivot.columns.values):
#    worksheet_1.write(0,col,value,format_header)


writer_1.close()
#writer_1.save()

#file_name_new = file_name+"- pivot.xlsx"
#all_pivot.to_excel(file_name_new)
