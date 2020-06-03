import pandas as pd

df = pd.read_excel('TEMP.xlsx')
lst = ['jmywsale','钓鱼之家']

lstin = df['tmfp'].to_list
df2 = df.loc[(df['order_type']=='地址不详' )& (df['finished'] == '未回复') & (df['tmfp'].isin(lst))]

print(df2)