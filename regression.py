import pandas as pd
from plotnine import *

import stata_setup
stata_setup.config("/Applications/Stata", "mp")

word_list = {
    'did': 'Policy',
    'L.lrealHousePrice': 'Housing Price(Lagged)',
    'lrealHousePrice': 'Housing Price',
    'lrealWage': 'Wage',
    'Standard errors in parentheses': 'Standard errors in parentheses. Clustered at the provincial level.',
    'nDistance': 'Distance',
    'lGDP_PerCapita': 'GDP Per Capita',
    'llandAreaResidential': 'Residential Land Area',
    'lp': R'Wage $\times$ Post',
}

from pystata import stata

stata.run(R'''
use Clean/PanelData.dta, clear
drop if provCode=="650000"
encode cityCode, gen(cityCodeI)
xtset cityCodeI year
est clear
''')

stata.run(R'''
gen Post = cond(year > 2009, 1, 0)
//keep if year < 2014
//keep if year > 2007
gen pp = isRestrict * Post
gen dp = nDistance * Post

replace nDistance = nDistance / 100

keep if isRestrict == 0

reghdfe lrealHousePrice l.lrealHousePrice lrealWage nDistance lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare, absorb(year) vce(cluster provCode)
estadd local Control "YES"
est store r0
reghdfe lrealHousePrice l.lrealHousePrice lrealWage nDistance, absorb(year) vce(cluster provCode)
estadd local Control "NO"
est store r1
esttab r1 r0 using Output/T2.tex, replace b(%9.3f) star(* 0.1 ** 0.05 *** 0.01) r2 se scalars(Control) booktabs drop(_cons lrealWage lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare) ///
    order(nDistance)
''')

with open('Output/T2.tex', 'r+') as f:
    content = f.read()
    for key, value in word_list.items():
        content = content.replace(key, value)
    f.seek(0)
    f.truncate()
    f.write(content)
    f.close()
    
    
stata.run(R'''
use Clean/PanelData.dta, clear
drop if provCode=="650000"
encode cityCode, gen(cityCodeI)
xtset cityCodeI year
est clear

gen Post = cond(year > 2009, 1, 0)
keep if year < 2017
keep if year > 2002

gen lp = L.lrealWage * Post

reghdfe lrealHousePrice L.lrealHousePrice lrealWage lp lGDP_PerCapita tertiaryIndustryEmploymentShare popDensity, absorb(year cityCode) vce(cluster provCode)
estadd local Control "YES"
est store r0
reghdfe lrealHousePrice L.lrealHousePrice lrealWage lp lGDP_PerCapita tertiaryIndustryEmploymentShare popDensity if isRestrict == 1, absorb(year cityCode) vce(cluster provCode)
estadd local Control "YES"
est store r1
reghdfe lrealHousePrice L.lrealHousePrice lrealWage lp lGDP_PerCapita tertiaryIndustryEmploymentShare popDensity if isRestrict == 0, absorb(year cityCode) vce(cluster provCode)
estadd local Control "YES"
est store r2
reghdfe lrealHousePrice L.lrealHousePrice lrealWage lGDP_PerCapita tertiaryIndustryEmploymentShare popDensity, absorb(year cityCode) vce(cluster provCode)
estadd local Control "YES"
est store r3
reghdfe lrealHousePrice L.lrealHousePrice lrealWage lGDP_PerCapita tertiaryIndustryEmploymentShare popDensity if isRestrict == 1, absorb(year cityCode) vce(cluster provCode)
estadd local Control "YES"
est store r4
reghdfe lrealHousePrice L.lrealHousePrice lrealWage lGDP_PerCapita tertiaryIndustryEmploymentShare popDensity if isRestrict == 0, absorb(year cityCode) vce(cluster provCode)
estadd local Control "YES"
est store r5
esttab r3 r4 r5 r0 r1 r2 using Output/T3.tex, replace b(%9.3f) star(* 0.1 ** 0.05 *** 0.01) r2 se scalars(Control) booktabs drop(_cons lGDP_PerCapita tertiaryIndustryEmploymentShare popDensity) ///
    mtitles("All" "Restricted" "Non-Restricted" "All" "Restricted" "Non-Restricted") ///
    mgroups("Housing Price", span prefix(\multicolumn{@span}{c}{) suffix(}) pattern(0 0 0 0 0) erepeat(\cmidrule(lr){@span})) ///
    nonumbers ///
    order(lp lrealWage L.lrealHousePrice) 
''')

with open('Output/T3.tex', 'r+') as f:
    content = f.read()
    for key, value in word_list.items():
        content = content.replace(key, value)
    # 调整宽度
    content = R'\resizebox{\textwidth}{!}{' + content + '}'
    f.seek(0)
    f.truncate()
    f.write(content)
    f.close()