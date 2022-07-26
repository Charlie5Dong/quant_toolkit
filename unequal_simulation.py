 `python
"""
1000个人抛1000次均匀的硬币，正面赢20%，反面赢10%，初始资本1万元，每次都全部押注，问：
1000次以后，每个人的资产分布？
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

rand_list1 = np.random.randint(1,3,size = (1000,1000)) #模拟每一次下注的收益
rand_list2  = pd.DataFrame(rand_list1)
rand_list2 = rand_list2/10 +1
rand_list2['1000'] = 1 #用于计算最终的资产分布

rand_list2 = rand_list2.cumprod(axis=1) #计算每一次下注后的资产变化

final_sum = rand_list2['1000'].sum()#全部人最终资产之和
rand_list2 = rand_list2.sort_values(by='1000',ascending=False, inplace=False)#对最终资产排序
rand_list2['cumsum']=rand_list2['1000'].cumsum()#计算前面N个人的资产累计和

rand_list2['percentile'] = rand_list2['cumsum']/final_sum #计算最富有的前x%占有全部财富的比例
print("前x%占有全部财富的比例是:\n",rand_list2['percentile'].quantile([0.01,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]))
print('最富有的1%的人占有全部资产的比例为：',round(rand_list2['percentile'].quantile(0.01),2))
print('最富有的5%的人占有全部资产的比例为：',round(rand_list2['percentile'].quantile(0.05),2))
print('最富有的10%的人占有全部资产的比例为：',round(rand_list2['percentile'].quantile(0.1),2))
print('最富有的20%的人占有全部资产的比例为：',round(rand_list2['percentile'].quantile(0.20),2))
print('最富有的50%的人占有全部资产的比例为：',round(rand_list2['percentile'].quantile(0.50),2))
print('最贫穷的50%的人占有全部资产的比例为：',round(1-rand_list2['percentile'].quantile(0.50),3))
print('最贫穷的20%的人占有全部资产的比例为：',round(1-rand_list2['percentile'].quantile(0.8),3))
print('最贫穷的10%的人占有全部资产的比例为：',round(1-rand_list2['percentile'].quantile(0.9),3))


wealth_average = rand_list2['1000'].mean()#低于平均资产的人的比例（多少人被平均）
below_average = rand_list2[rand_list2['1000'] < wealth_average]
below_average_percentile = below_average['1000'].count()/1000
print('资产低于平均值的人的比例为：',below_average_percentile)

plt.figure(figsize =(8,4))#资产分布的直方图
sns.displot(rand_list2['1000'],bins=30,color='r',label='wealth_distribution')
plt.legend()

plt.figure(figsize =(8,4))#累计分布
sns.kdeplot(rand_list2['1000'],cumulative=True,label='wealth_cum_distribution')
plt.legend()

plt.figure(figsize =(8,4))#将最终资产对数化后，分布的直方图
sns.histplot(rand_list2['1000'],bins=100,color='r',label='log_wealth_distribution',log_scale = 10)
plt.legend()

plt.figure(figsize =(8,4))#将最终资产对数化后，累计分布
sns.kdeplot(rand_list2['1000'],cumulative=True,log_scale = 10,label='log_wealth_cum_distribution')
plt.legend()

rand_list2['1000'].describe()
