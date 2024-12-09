import pandas as pd
import numpy as np
import os
import json

# 判断Clean文件夹是否存在不存在则创建

if not os.path.exists('Clean'):
    os.makedirs('Clean')
    
# 标签
data_city_labels_stata = {}

# Clean restrict policy data
data_restrict = dict(json.load(open('./Sources/restriction.json')))
ctCode = data_restrict.keys()
isRestrict = data_restrict.values()
data_restrict = pd.DataFrame({
    'cityCode': ctCode,
    'isRestrict': isRestrict
})
data_restrict = data_restrict.astype({
    'cityCode': 'str',
    'isRestrict': 'int'
})
data_city_labels_stata.update({
    'isRestrict': '是否限购(2011)'
})
print(data_restrict.head())

# Clean City Data
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
data_city_labels_stata.update(dict(data_city_labels))
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

#建立ProvCode和ProvName的对应关系
data_prov_code = data_city[['provName', 'provCode']]
data_prov_code.drop_duplicates(inplace=True)
data_prov_code_dict = dict(zip(data_prov_code['provCode'], data_prov_code['provName']))

# Clean Wage Data
data_wage = pd.read_excel('./Sources/CRE_Eplwagct/CRE_Eplwagct.xlsx')
data_wage.rename(
    columns={
        'Ctnm': 'cityName',
        'Ctnm_id': 'cityCode',
        'Sgnyea': 'year',
        'Eect01': 'totalPopulationYearEnd',
        'Eect02': 'nonAgriculturalPopulationYearEnd',
        'Eect03': 'naturalPopulationGrowthRate',
        'Eect04': 'populationDensity',
        'Eect05': 'employedPersons',
        'Eect06': 'urbanSelfEmployedWorkers',
        'Eect08': 'primaryIndustryEmploymentShare',
        'Eect09': 'secondaryIndustryEmploymentShare',
        'Eect10': 'tertiaryIndustryEmploymentShare',
        'Eect11': 'annualAverageNumberOfEmployees',
        'Eect12': 'totalWagesOfAllEmployees',
        'Eect13': 'averageWageOfEmployees',
    },
    inplace=True
)

data_wage_labels = data_wage.iloc[:2, :]
data_wage_labels = data_wage_labels.apply(lambda x: x.str.cat(sep='|'))
data_wage_labels_stata = dict(data_wage_labels)
# 合并data_city_labels_stata
data_city_labels_stata.update(data_wage_labels_stata)
data_wage = data_wage.iloc[2:, :]
data_wage.reset_index(drop=True, inplace=True)
data_wage.fillna(-1, inplace=True)

data_wage = data_wage.astype({
    'year': 'int',
    'cityName': 'str',
    'cityCode': 'str',
    'totalPopulationYearEnd': 'int',
    'nonAgriculturalPopulationYearEnd': 'int',
    'naturalPopulationGrowthRate': 'float',
    'populationDensity': 'float',
    'employedPersons': 'int',
    'urbanSelfEmployedWorkers': 'int',
    'primaryIndustryEmploymentShare': 'float',
    'secondaryIndustryEmploymentShare': 'float',
    'tertiaryIndustryEmploymentShare': 'float',
    'annualAverageNumberOfEmployees': 'int',
    'totalWagesOfAllEmployees': 'float',
    'averageWageOfEmployees': 'float',
})

print(data_wage.head())
print(data_wage.dtypes)
data_wage.to_excel('Clean/CRE_Eplwagct.xlsx', index=False)
data_wage.to_stata('Clean/CRE_Eplwagct.dta', write_index=False, version=118, variable_labels=data_wage_labels_stata)

# Clean LAND Data
data_land = pd.read_excel('./Sources/URC_UrbPopConLandCY/URC_UrbPopConLandCY.xlsx')
data_land.rename(
    columns={
        'SgnYear': 'year',
        'CityName': 'cityName',
        'CityCode': 'cityCode',
        'UrbanConLandArea': 'landArea',
        'ResidentialLand': 'landAreaResidential',
    },
    inplace=True
)
data_land = data_land[['cityCode', 'year', 'landArea', 'landAreaResidential']]
data_land_labels = data_land.iloc[:2, :]
data_land_labels = data_land_labels.apply(lambda x: x.str.cat(sep='|'))
data_land_labels_stata = dict(data_land_labels)
data_city_labels_stata.update(data_land_labels_stata)
data_land = data_land.iloc[2:, :]
data_land.reset_index(drop=True, inplace=True)
data_land.fillna(-1, inplace=True)
data_land = data_land.astype({
    'year': 'int',
    'cityCode': 'str',
    'landArea': 'float',
    'landAreaResidential': 'float',
})
print(data_land.head())
data_land.to_excel('Clean/URC_UrbPopConLandCY.xlsx', index=False)
data_land.to_stata('Clean/URC_UrbPopConLandCY.dta', write_index=False, version=118, variable_labels=data_land_labels_stata)

# Clean CPI Data
data_cpi = pd.read_excel('./Sources/CRE_Pi01/CRE_Pi01.xlsx')
data_cpi.rename(
    columns={
        'Sgnyea': 'year',
        'Prvcnm': 'provName',
        'Prvcnm_id': 'provCode',
        'Pi0101': 'CPI',
    },
    inplace=True
)
#print(data_cpi.head())
data_cpi = data_cpi[['provCode', 'year', 'CPI']]
data_cpi_labels = data_cpi.iloc[:2, :]
data_cpi_labels = data_cpi_labels.apply(lambda x: x.str.cat(sep='|'))
data_cpi_labels_stata = dict(data_cpi_labels)
data_cpi = data_cpi.iloc[2:, :]
data_cpi.reset_index(drop=True, inplace=True)
data_cpi.fillna(-1, inplace=True)
data_cpi = data_cpi.astype({
    'year': 'int',
    'provCode': 'str',
    'CPI': 'float',
})
# 同一省份的CPI去年是100, 所以以2000年为基准, 重新校准CPI
# 比如2002年的CPI是按照2001为100计算的, 所以要重新计算,实际上是2002年的CPI/2001年的CPI*100

def calibrate_cpi(df):
    df.sort_values(['year'], inplace=True)
    # 删除2000年以前的数据
    df = df[df['year'] >= 2000]
    # 将2000年的CPI设为100
    df.loc[df['year'] == 2000, 'CPI'] = 100
    # 循环计算CPI
    for i in range(1, len(df)):
        df.loc[df.index[i], 'CPI'] = df.loc[df.index[i], 'CPI'] * df.loc[df.index[i - 1], 'CPI'] / 100
    return df

data_cpi = data_cpi.groupby('provCode').apply(calibrate_cpi, include_groups=True).reset_index(drop=True)
print(data_cpi.head())
data_cpi.to_excel('Clean/CRE_Pi01.xlsx', index=False)
data_cpi.to_stata('Clean/CRE_Pi01.dta', write_index=False, version=118, variable_labels=data_cpi_labels_stata)

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


# 合并面板数据
data_hp = data_hp[['cityCode', 'year', 'unitHousePrice']]
data_wage = data_wage[['cityCode', 'year', 'averageWageOfEmployees', 
                       'primaryIndustryEmploymentShare', 'secondaryIndustryEmploymentShare', 
                       'tertiaryIndustryEmploymentShare', 'totalPopulationYearEnd']]
data_panel = data_city.merge(data_hp, on=['cityCode', 'year'], how='left')
data_panel = data_panel.merge(data_wage, on=['cityCode', 'year'], how='left')
data_panel = data_panel.merge(data_cpi, on=['provCode', 'year'], how='left')
data_panel = data_panel.merge(data_land, on=['cityCode', 'year'], how='left')
data_panel = data_panel.merge(data_restrict, on=['cityCode'], how='left')
    
print(data_panel.columns)
#data_panel.fillna(-1, inplace=True)
# 列排序
columns_original = data_panel.columns.tolist()
# cityName, cityCode, year, unitHousePrice 在前
columns_sorted = ['cityName', 'cityCode', 'provName', 'provCode', 'year', 'unitHousePrice', 'averageWageOfEmployees']
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
data_panel = data_panel[data_panel['averageWageOfEmployees'] > 0]

#生成真实房价和真实工资
data_panel['realHousePrice'] = data_panel['unitHousePrice'] / data_panel['CPI'] * 100
data_panel['realWage'] = data_panel['averageWageOfEmployees'] / data_panel['CPI'] * 100

data_city_labels_stata['realHousePrice'] = '真实房价|元每平方米'
data_city_labels_stata['realWage'] = '真实工资|元'
data_city_labels_stata['CPI'] = '省份消费者物价指数|%'

# 人均GDP修正
def gdp_fix(d: pd.Series):
    if d['GDP_PerCapita'] < 0:
        #print("Fixing GDP_PerCapita for", d['cityName'])
        d['GDP_PerCapita'] = d['Gdpct01'] / d['totalPopulationYearEnd'] * 10000
    return d
data_panel = data_panel.apply(gdp_fix, axis=1)

# 对房价、工资、真实房价、真实工资、建设用地面积、住宅用地面积生成log变量，命令为l+变量名
for col in ['unitHousePrice', 
            'averageWageOfEmployees', 
            'realHousePrice', 
            'totalPopulationYearEnd',
            'realWage', 'landArea', 
            'landAreaResidential', 'GDP_PerCapita']:
    data_panel[f'l{col}'] = np.log(data_panel[col])
    # 无穷处理成缺失值
    data_panel.replace([np.inf, -np.inf], np.nan, inplace=True)
    # 更新label
    data_city_labels_stata[f'l{col}'] = f'ln({col})'
    
# 处理为平衡面板数据
data_panel = data_panel[data_panel['year'] >= 2000]
data_panel = data_panel[data_panel['year'] <= 2020]
def calibrate_panel(df):
    if len(df) < (2020 - 2000 + 1):
        return None
    return df
#data_panel = data_panel.groupby('cityCode').apply(calibrate_panel, include_groups=True).reset_index(drop=True)

data_panel.to_excel('Clean/PanelData.xlsx', index=False)
data_panel.to_stata('Clean/PanelData.dta', write_index=False, version=118, variable_labels=data_city_labels_stata)
print('Cleaned data saved to Clean/PanelData')

# 打印出城市总数
print('城市总数:', data_panel['cityName'].nunique())

# 打印出CityCode到CityCode.txt
with open('Clean/CityCode.txt', 'w') as f:
    for k, v in data_city_code_dict.items():
        f.write(f'{k} {v}\n')
        
# 按省份生成一份数据
data_prov = data_panel[[
    'provCode', 
    'year', 
    'unitHousePrice', 
    'averageWageOfEmployees', 
    'CPI', 
    'landArea', 
    'landAreaResidential',
    'realHousePrice',
    'realWage',
    ]]
data_prov = data_prov.groupby(['provCode', 'year']).mean().reset_index()
# 加上省份名称
data_prov['provName'] = data_prov['provCode'].map(data_prov_code_dict)
data_prov.to_excel('Clean/PanelDataProv.xlsx', index=False)
data_prov.to_stata('Clean/PanelDataProv.dta', write_index=False, version=118, variable_labels=data_city_labels_stata)