use Clean/PanelData.dta, clear
drop if provCode=="650000"
encode cityCode, gen(cityCodeI)
xtset cityCodeI year

gen Post = cond(year > 2009, 1, 0)
keep if year < 2017
keep if year > 2002
gen pp = isRestrict * Post
gen dp = nDistance * Post
reghdfe lrealHousePrice nDistance lrealWage dp lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare if isRestrict == 0, absorb(year) vce(cluster provCode)

reghdfe lrealHousePrice l.lrealHousePrice lrealWage nDistance lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare popDensity , absorb(year) vce(cluster provCode)


gen lp = L.lrealWage * Post 
reghdfe lrealHousePrice L.lrealHousePrice lrealWage lp lGDP_PerCapita tertiaryIndustryEmploymentShare popDensity if isRestrict == 1, absorb(year cityCode) vce(cluster provCode)

