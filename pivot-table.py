import pandas as pd
import numpy as np
import os

cwd = os.path.abspath('')
files = os.listdir(cwd)

file_name = ''

for f in files:
    if f.endswith('.xlsx'):
        excel_file = pd.ExcelFile(f)
        file_name = f

df1 = pd.read_excel(excel_file,'CR')
df2 = pd.read_excel(excel_file, 'PP')

pd.set_option('display.float_format', '{:,.2f}'.format)

CR = pd.pivot_table(df1,index='Follower Office Code',values='Total claim amount',aggfunc=np.sum)#,margins=True)
PP = pd.pivot_table(df2,index='Follower Office Code',values='Net Premium payable',aggfunc=np.sum)#,margins=True)


all_pivot = pd.merge(PP,CR,left_index=True,right_index=True,how='outer')
all_pivot.fillna(0,inplace=True)

all_pivot['Net Payable by UIIC'] = all_pivot['Net Premium payable'] - all_pivot['Total claim amount']

all_pivot.rename({'Total claim amount': 'Claims receivable'},axis=1,inplace=True)

all_pivot.loc['Total']= all_pivot.sum(numeric_only=True,axis=0)
#pd.set_option('display.float_format','{:.2f}'.format)

all_pivot.style.format({'Net Payable by UIIC':'{0:,.2f}'})

print(all_pivot)
#all_pivot.style.format({'Net Payable by UIIC':'${0:,.0f}'})



writer_1 = pd.ExcelWriter("pivot-table.xlsx",engine='xlsxwriter')
all_pivot.to_excel(writer_1,sheet_name="Net")
#writer_1.save()
workbook_1 = writer_1.book
worksheet_1 = writer_1.sheets['Net']

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


writer_1.save()

#file_name_new = file_name+"- pivot.xlsx"
#all_pivot.to_excel(file_name_new)
