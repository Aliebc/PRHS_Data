import stata_setup
stata_setup.config("/Applications/Stata", "mp")
from pystata import stata

word_list = {
    'did': 'Policy',
    'lrealHousePrice': 'Housing Price',
    'lrealWage': 'Wage',
    'Standard errors in parentheses': 'Standard errors in parentheses. Clustered at the provincial level.',
}


stata.run(R'''
use Clean/PanelData.dta, clear
drop if provCode=="650000"
drop if year > 2017
drop if year < 2003
gen Post = cond(year > 2009, 1, 0)
set scheme tufte
encode cityCode, gen(id)
gen ti = year - 2010
gen treat = isRestrict
gen did = isRestrict * Post
est clear
reghdfe lrealHousePrice did lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare popDensity, absorb(id year) vce(cluster provCode)
estadd local Control "YES"
est store r0
reghdfe lrealWage did lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare secondaryIndustryEmploymentShare popDensity, absorb(id) vce(cluster provCode)
estadd local Control "YES"
est store r1
reghdfe lrealHousePrice did, absorb(id year) vce(cluster provCode)
estadd local Control "NO"
est store r3
reghdfe lrealWage did, absorb(id) vce(cluster provCode)
estadd local Control "NO"
est store r4
esttab r3 r4 r0 r1 using Output/T1.tex, replace b(%9.3f) star(* 0.1 ** 0.05 *** 0.01) r2 se scalars(Control) booktabs drop(_cons lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare popDensity secondaryIndustryEmploymentShare)  
''')


with open('Output/T1.tex', 'r+') as f:
    content = f.read()
    for key, value in word_list.items():
        content = content.replace(key, value)
    f.seek(0)
    f.truncate()
    f.write(content)
    f.close()