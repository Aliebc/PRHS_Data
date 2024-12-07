import pandas as pd
import os

# 判断Clean文件夹是否存在，不存在则创建

if not os.path.exists('Clean'):
    os.makedirs('Clean')

#Clean City Data
# 把前三行合并为一行Sources/CRE_Gdpct/CRE_Gdpct.xlsx
data_city = pd.read_excel('./Sources/CRE_Gdpct/CRE_Gdpct.xlsx')
data_city.rename(
    columns={
        'Sgnyea': 'year',
        'Ctnm': 'cityName',
        'Ctnm_id': 'cityCode',
        'Cttyp': 'cityType',
        'Prvcnm_id': 'provCode',
        'Prvcnm': 'provName',
    },
    inplace=True
)

# 前两行作为label, 合并label为一行
data_city_labels = data_city.iloc[:2, :]
data_city_labels = data_city_labels.apply(lambda x: x.str.cat(sep='|'))
# 取第二列所有作为label
data_city_labels_stata = dict(data_city_labels)
#print(data_city_labels_stata)
data_city = data_city.iloc[2:, :]
data_city.reset_index(drop=True, inplace=True)
data_city.fillna(-1, inplace=True)

data_city = data_city.astype({
    'year': 'int',
    'cityName': 'str',
    'cityCode': 'str',
    'cityType': 'str',
})

print(data_city.head())
print(data_city.dtypes)
data_city.to_excel('Clean/CRE_Gdpct.xlsx', index=False)
data_city.to_stata('Clean/CRE_Gdpct.dta', write_index=False, version=118, variable_labels=data_city_labels_stata)
print('Cleaned data saved to Clean/CRE_Gdpct')

# 建立CityCode和CityName的对应关系
data_city_code = data_city[['cityName', 'cityCode', 'cityType']]
data_city_code.drop_duplicates(inplace=True)
data_city_code_dict = dict(zip(data_city_code['cityCode'], data_city_code['cityName']))
data_city_type_dict = dict(zip(data_city_code['cityCode'], data_city_code['cityType']))

#Clean House Price Data
data_hp = pd.read_excel('./Sources/HousePrice.xlsx', sheet_name='面板数据')

data_hp.rename(
    columns={
        '省份': 'provName',
        '城市': 'cityName',
        '年份': 'year',
        '单价（元每平方米）': 'unitHousePrice',
    },
    inplace=True
)

data_city_code = data_city[['cityName', 'cityCode']]
data_city_code.drop_duplicates(inplace=True)
data_hp = data_hp.merge(data_city_code, on='cityName', how='left')

#打印出没有匹配到的城市
print(data_hp[data_hp['cityCode'].isnull()]['cityName'].unique())
# 删除没有匹配到的城市
data_hp = data_hp[data_hp['cityCode'].notnull()]

data_hp.fillna(-1, inplace=True)

data_hp = data_hp.astype({
    'provName': 'str',
    'cityName': 'str',
    'cityCode': 'str',
    'year': 'int',
    'unitHousePrice': 'float',
})

data_hp.drop('id', inplace=True, axis=1)

print(data_hp.head())

data_hp.to_excel('Clean/HousePrice.xlsx', index=False)

data_hp.to_stata('Clean/HousePrice.dta', write_index=False, version=118, variable_labels={
    'provName': '省份名称',
    'cityName': '城市名称',
    'cityCode': '城市代码',
    'year': '年份',
    'unitHousePrice': '房价（元每平方米）'
})
print('Cleaned data saved to Clean/HousePrice.xlsx')

# 打印出城市总数
print('城市总数:', data_city['cityName'].nunique())


# 合并面板数据
data_hp = data_hp[['cityCode', 'year', 'unitHousePrice']]
data_panel = data_city.merge(data_hp, on=['cityCode', 'year'], how='left')
#data_panel.fillna(-1, inplace=True)
# 列排序
columns_original = data_panel.columns.tolist()
# cityName, cityCode, year, unitHousePrice 在前
columns_sorted = ['cityName', 'cityCode', 'provName', 'provCode', 'year', 'unitHousePrice']
columns_sorted.extend([col for col in columns_original if col not in columns_sorted])
data_panel = data_panel[columns_sorted]

# 按cityCode, year排序
data_panel.sort_values(['cityCode', 'year'], inplace=True)
print(data_panel.head())

# 更新cityName
data_panel['cityName'] = data_panel['cityCode'].map(data_city_code_dict)
# 更新cityType
data_panel['cityType'] = data_panel['cityCode'].map(data_city_type_dict)

data_city_labels_stata['unitHousePrice'] = '房价|元每平方米'

data_panel.dropna(subset=['unitHousePrice'], inplace=True)
data_panel = data_panel[data_panel['unitHousePrice'] > 0]

data_panel.to_excel('Clean/PanelData.xlsx', index=False)
data_panel.to_stata('Clean/PanelData.dta', write_index=False, version=118, variable_labels=data_city_labels_stata)

print('Cleaned data saved to Clean/PanelData')

# 打印出CityCode到CityCode.txt
with open('Clean/CityCode.txt', 'w') as f:
    for k, v in data_city_code_dict.items():
        f.write(f'{k} {v}\n')