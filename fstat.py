# 描述性统计

import pandas as pd
from plotnine import *
import os

import stata_setup
stata_setup.config("/Applications/Stata", "mp")

from pystata import stata

# 读取数据
data_panel = pd.read_excel('Clean/PanelData.xlsx')
stata.run(R'use Clean/PanelData.dta, clear')
stata.run(R'describe')
stata.run(R'set scheme tufte')
print(data_panel.head())

## 测试作图, 所有地级市的房价/工资

data_city_code = data_panel[['cityCode', 'cityName', 'provName']].drop_duplicates()
data_city_code_city = dict(zip(data_city_code['cityCode'], data_city_code['cityName']))
data_city_code_prov = dict(zip(data_city_code['cityCode'], data_city_code['provName']))

# label 修改为英文
stata.run(R'label variable realHousePrice "Real House Price (yuan/m^2)"')
stata.run(R'label variable realWage "Real Wage (yuan/year)"')

for code in data_city_code_city.keys():
    stata.run(f'scatter realHousePrice realWage if cityCode == "{code}", mlabel(year) ')
    cityName = data_city_code_city[code]
    provName = data_city_code_prov[code]
    stata.run(f'graph export "Output/Test_img/Price_Wage_{provName}_{cityName}.pdf", replace')

## 作图 210100

#os.system('mv Output/Test_img/Price_Wage_辽宁省_沈阳市.svg Output/Test_img/Price_Wage_210100.png')