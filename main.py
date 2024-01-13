import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime,timedelta
data=pd.read_excel(r'credit card.xls')
print(data)
#data.to_csv('csvfile.csv',encoding='utf-8')
#data=pd.read_csv("csvfile.csv")

# Provide a meaningful treatment to all values where age is less than 18.
data.loc[(data.Age<18),'Age']=data.Age.mean()
print(data)
#Monthly spend of each customer.
Spend_data=pd.read_excel(r'credit card.xls','Spend')
print(Spend_data)
Spend_data.isnull().sum()
Customer_Spend_Transaction=pd.merge(left=data,right=Spend_data,on='Customer')
print(Customer_Spend_Transaction)


Customer_Spend_Amount=Customer_Spend_Transaction.groupby(['Customer','Month'])[['Amount']].mean().reset_index()
Customer_Spend_Amount['Spend_Month']=Customer_Spend_Amount['Month'].apply(lambda x:x.month)
AvgMonthlySpend=Customer_Spend_Amount.groupby(['Customer','Spend_Month'])[['Amount']].mean().reset_index()
print(AvgMonthlySpend)


#Monthly repayment of each customer.
repayment_data=pd.read_excel(r'credit card.xls','Repayment')
print(repayment_data)

Customer_Repayment_Transaction=pd.merge(left=data,right=repayment_data,on='Customer')
Customer_Repayment_Amount=Customer_Repayment_Transaction.groupby(['Customer','Month'])[['Amount']].mean().reset_index()
Customer_Repayment_Amount['Repayment_Month']=Customer_Repayment_Amount['Month'].apply(lambda x:x.month)
AvgMonthlyRepayment=Customer_Repayment_Amount.groupby(['Customer','Repayment_Month'])[['Amount']].mean().reset_index()
print(AvgMonthlyRepayment)





#Identity where the repayment is more than the spend then give them a credit of 2% of their surplusamount in the next month billing.

Customer_Repayment_Transaction['Amount']=np.where(Customer_Repayment_Transaction.Amount>Customer_Repayment_Transaction.Limit,Customer_Repayment_Transaction.Limit,Customer_Repayment_Transaction.Amount*0.02)
print(Customer_Repayment_Transaction)


#Which age group is spending more money?
age_groups = pd.cut(data['Age'], bins=[0, 18, 25, 65, 150], labels=['Children', 'Youth', 'Adult', 'Senior'])
age_group_spending = data.groupby(age_groups)['Amount'].sum()
print(age_group_spending)


#Highest paying 10 customers.
Hp=Customer_Repayment_Transaction.groupby('Customer').Amount.sum().reset_index().sort_values('Amount',ascending=False)
print(Hp)



#Monthly profit for the bank.
AvgMonthlyCustomers=pd.merge(left=AvgMonthlySpend,right=AvgMonthlyRepayment,left_on=['Customer','Spend_Month'],right_on=['Customer','Repayment_Month'])
AvgMonthlyCustomers['Monthly_Profit']=AvgMonthlyCustomers.Amount_y-AvgMonthlyCustomers.Amount_x
print(AvgMonthlyCustomers)



#Impose an interest rate of 2.9% for each customer for any due amount.
AvgMonthlyCustomers['Profit'] = np.where(AvgMonthlyCustomers['Monthly_Profit'] > 0, AvgMonthlyCustomers['Monthly_Profit'] * 0.029, np.nan)
print(AvgMonthlyCustomers)

#In which category the customers are spending more money?
mc=Customer_Spend_Transaction.groupby('Type').Amount.sum().reset_index().sort_values('Amount',ascending=False)
print(mc.to_string())


#People in which segment are spending more money.
ms=Customer_Spend_Transaction.groupby('Segment').Amount.sum().reset_index().sort_values('Amount',ascending=False)
print(ms)


#Which is the most profitable segment?
profit_by_segment = Customer_Spend_Transaction.groupby('Segment')['Amount'].sum()
most_profitable_segment = profit_by_segment.idxmax()
print("The most profitable segment is:", most_profitable_segment)




#momthly spend of customer
monthly_spend = Customer_Spend_Transaction.groupby('Customer')['Amount'].sum()
print(monthly_spend)



#Monthly repayment of each customer.
monthly_repayment = Customer_Repayment_Transaction.groupby('Customer')['Amount'].sum()
print(monthly_repayment)









