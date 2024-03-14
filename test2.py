import pandas as pd
import matplotlib.pyplot as plt
#1
df = pd.read_csv('elections_selected.csv')

result = df.groupby(['VCF0004']).agg(respondentCounts=('VCF0004','value_counts'),VCF0707=('VCF0707','count'),VCF0704A=('VCF0704A','count'))
# 民主党总统候选人的选民数量
counts = df[df['VCF0704A'] == 1].groupby('VCF0004')['VCF0704A'].count()
# 投给民主党候选人的西班牙裔选民
counts2 = df[(df['VCF0106A'] == 5) & (df['VCF0704A'] == 1)].groupby('VCF0004')['VCF0106A'].count()
# 合并统计结果到一个DataFrame
result = pd.DataFrame({'respondentCounts': result['respondentCounts'],'VCF0707': result['VCF0707'],'VCF0704A': result['VCF0704A'], 'countOfDemocraticCandidates': counts,'countOfHispanicVoters':counts2})


# 添加一列并计算值
# 计算总统选票中投给民主党候选人的比例
result['radioOfDemocraticCandidates'] = result['countOfDemocraticCandidates'] / result['VCF0704A']
# 计算投给民主党候选人的西班牙裔选民比例
result['radioOfHispanicVoters'] = result['countOfHispanicVoters'] / result['VCF0704A']

# 删除一列
result = result.drop('countOfHispanicVoters', axis=1)
print(result)

# 保存为Excel文件
result.to_excel('output.xlsx')
#2
# # 删除包含缺失值的行
df_cleaned = result.dropna()
# first_key = list(df_cleaned.groups.keys())[0]
print(list(df_cleaned.index))
# 绘制折线图
plt.figure(figsize=(10, 6))
plt.plot(list(df_cleaned.index), df_cleaned['radioOfDemocraticCandidates'], marker='o', linestyle='-', color='b', label='Democratic presidential vote ratio')
plt.title('Changes in Democratic presidential vote percentage')
plt.xlabel('year')
plt.ylabel('ratio')
plt.legend()
plt.grid(True)
plt.show()

# # 绘制柱状图
plt.figure(figsize=(10, 6))
plt.bar(list(df_cleaned.index), df_cleaned['radioOfDemocraticCandidates'], color='b', label='Democratic presidential vote ratio')
plt.title('Changes in Democratic presidential vote percentage')
plt.xlabel('year')
plt.ylabel('ratio')
plt.legend()
plt.grid(axis='y')
plt.show()

#3
# 删除包含缺失值的行
df_cleaned = df.dropna()

# 或者删除包含缺失值的列
df_cleaned = df.dropna(axis=1)

# 用平均值填充缺失值
df_filled = df.fillna(df.mean())
df_filled = df.fillna()
print(df_filled)
# 用中位数填充缺失值
df_filled = df.fillna(df.median())

# 用众数填充缺失值
df_filled = df.fillna(df.mode().iloc[0])


# 假设df是包含所有相关变量的DataFrame

# 选择1992年和2004年的数据
selected_years = [1992, 2004]
selected_data = df[df['VCF0004'].isin(selected_years)]

# 对于连续变量，计算均值、标准差、最小值、最大值和观测数量
continuous_variables = ['VCF0101']
summary_continuous = selected_data.groupby('VCF0004')[continuous_variables].describe()

# 对于分类变量，计算变量的分布
categorical_variables = ['VCF0104', 'VCF0106A', 'VCF0110', 'VCF0111']
summary_categorical = pd.DataFrame()

for variable in categorical_variables:
    summary_categorical[variable] = selected_data.groupby(['VCF0004', variable])[variable].count()

# 对于分类变量，创建虚拟变量并计算均值、标准差、最小值、最大值和观测数量
dummy_variables = pd.get_dummies(selected_data[categorical_variables])
summary_dummy = pd.concat([selected_data['VCF0004'], dummy_variables], axis=1).groupby('VCF0004').describe()

# 打印结果
print("连续变量的汇总统计：")
print(summary_continuous)
summary_continuous.to_excel('summary_continuous.xlsx')
print("\n分类变量的分布：")
print(summary_categorical)
summary_categorical.to_excel('summary_categorical.xlsx')
print("\n虚拟变量的汇总统计：")
print(summary_dummy)

# 根据年份选择数据
df_1992 = df[df['VCF0004'] == 1992]
df_2004 = df[df['VCF0004'] == 2004]

# 连续变量的描述统计
continuous_vars = ['VCF0101']
continuous_stats_1992 = df_1992[continuous_vars].describe().T[['mean', 'std', 'min', 'max', 'count']]
continuous_stats_2004 = df_2004[continuous_vars].describe().T[['mean', 'std', 'min', 'max', 'count']]


# 分类变量的分布
categorical_vars = ['VCF0104', 'VCF0106A', 'VCF0110', 'VCF0111']
categorical_stats_1992 = (df_1992[categorical_vars].value_counts(normalize=True).round(2) * 100).reset_index().rename(columns={0: '1992年 分类变量分布'})
categorical_stats_2004 = (df_2004[categorical_vars].value_counts(normalize=True).round(2) * 100).reset_index().rename(columns={0: '2004年 分类变量分布'})

# 创建虚拟变量
dummy_vars_1992 = pd.get_dummies(df_1992[categorical_vars]).mean().to_frame().T
dummy_vars_2004 = pd.get_dummies(df_2004[categorical_vars]).mean().to_frame().T

# 输出1992年表格
output_table_1992 = pd.concat([continuous_stats_1992, categorical_stats_1992, dummy_vars_1992], axis=1)
print("1992年数据:")
print(output_table_1992)
# # 保存为Excel文件
output_table_1992.to_excel('1992.xlsx')
# 输出2004年表格
output_table_2004 = pd.concat([continuous_stats_2004, categorical_stats_2004, dummy_vars_2004], axis=1)
print("\n2004年数据:")
print(output_table_2004)
output_table_2004.to_excel('2004.xlsx')
#4
# 假设df是包含所有相关变量的DataFrame

# 选择2004年的数据
data_2004 = df[df['VCF0004'] == 2004]
data_2004['VCF0154B'].fillna('DK',inplace=True)
replacement_dict = {1:'Executive, administrative and managerial', 
                    2:'Professional specialty occupations', 
                    3:'Technicians and related support occupations',
                    4:'Sales occupations',
                    5:'Administrative support, including clerical',
                    6:'Private h7',
                    7:'Protective service',
                    8:'Service except protective and household',
                    9:'Farming, forestry and fishing occupations',
                    10:'Precision production, craft and repair occupations',
                    11:'Machine operators, assemblers and inspectors',
                    12:'Transportation and material moving occupations',
                    13:'Handlers, equipment cleaners, helpers and laborers',
                    14:'Member of the armed forces'
                    }
data_2004['VCF0154B'].replace(replacement_dict, inplace=True)
print(data_2004)
# 根据职业划分，计算民主选民百分比
democrat_voters_by_occupation = data_2004[data_2004['VCF0704A'] == 1].groupby('VCF0154B')['VCF0704A'].count()
# total_voters_by_occupation = data_2004.groupby('VCF0154B').agg(VCF0704A=('VCF0704A','count'))
result_2004 = pd.DataFrame({'countOfDemocraticCandidates': democrat_voters_by_occupation})
result_2004['radioOfDemocraticCandidates'] = result_2004['countOfDemocraticCandidates'] / data_2004[data_2004['VCF0704A'] == 1]['VCF0704A'].count() * 100
print(result_2004['countOfDemocraticCandidates'].sum())
print(data_2004[data_2004['VCF0704A'] == 1]['VCF0704A'].count())

# 根据百分比绘制柱状图
plt.figure(figsize=(14, 8))
# plt.bar(list(result_2004.index), result_2004['radioOfDemocraticCandidates'], color='b', label='民主党总统选票比例')

# 设置x轴为水平显示
plt.barh(range(len(list(result_2004.index))), result_2004['radioOfDemocraticCandidates'])
plt.yticks(range(len(list(result_2004.index))), list(result_2004.index))

# percentage_democrat_voters.sort_values(ascending=True).plot(kind='barh', color='blue')
plt.title('The percentage of democratic voters in 2004 was divided by occupation')
plt.xlabel('Percentage of democratic voters')
plt.ylabel('Occupation category')
plt.grid(axis='x')
plt.tight_layout()
plt.show()

