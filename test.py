import numpy as np
from sklearn.linear_model import LinearRegression
import xlrd

workbook = xlrd.open_workbook('./data.xls')  # 替换为你的文件路径
# 获取所有工作表的名称
sheet_names = workbook.sheet_names()

dataX = []
dataY1 = []
dataY2 = []

# 遍历每个工作表
for sheet_name in sheet_names:
    print('工作表名:', sheet_name)
    sheet = workbook.sheet_by_name(sheet_name)
    
    # 获取该工作表的行数和列数
    num_rows = sheet.nrows
    num_columns = sheet.ncols
    
    # 遍历每一行
    for row_index in range(num_rows):
        if row_index == 0:
            continue
        # 获取该行的数据列表
        row_values = sheet.row_values(row_index)
        
        # 遍历该行的每个单元格
        for col_index in range(num_columns):
            # 获取单元格的值
            cell_value = row_values[col_index]
            if col_index == 0:
                dataX.append([cell_value])
            if col_index == 1:
                dataY1.append(cell_value)
            if col_index == 2:
                dataY2.append(cell_value)
            # print(cell_value, end='\t')  # 打印单元格值
# 关闭Excel文件
# workbook.close()
# print(workbook)
# print(dataY)
# print(dataX)

# 已知数据
X = np.array(dataX)
y1 = np.array(dataY1)
y2= np.array(dataY2)
# 创建线性回归模型
model = LinearRegression()
# 拟合训练数据
model.fit(X, y1)

# 获取回归方程的斜率和截距
slope = model.coef_[0]
intercept = model.intercept_

print("斜率1:", slope)
print("截距1:", intercept)

# 拟合训练数据
model.fit(X, y2)

# 获取回归方程的斜率和截距
slope = model.coef_[0]
intercept = model.intercept_

print("斜率2:", slope)
print("截距2:", intercept)