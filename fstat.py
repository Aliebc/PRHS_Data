# 描述性统计

import pandas as pd
from plotnine import *

import stata_setup
stata_setup.config("/Applications/Stata", "mp")

from pystata import stata

# 读取数据
data_panel = pd.read_excel('Clean/PanelData.xlsx')
stata.run(f'use Clean/PanelData.dta, clear')
stata.run(f'describe')
print(data_panel.head())

## 测试作图, 所有地级市的房价/工资

data_city_code = data_panel[['cityCode', 'cityName', 'provName']].drop_duplicates()
data_city_code_city = dict(zip(data_city_code['cityCode'], data_city_code['cityName']))
data_city_code_prov = dict(zip(data_city_code['cityCode'], data_city_code['provName']))

for code in data_city_code_city.keys():
    stata.run(f'scatter realHousePrice realWage if cityCode == "{code}", mlabel(year)')
    cityName = data_city_code_city[code]
    provName = data_city_code_prov[code]
    stata.run(f'graph export "Output/Test_img/Price_Wage_{provName}_{cityName}.svg", replace width(800) height(600)')

## 图1: 河南省房价