use Clean/PanelData.dta, clear
drop if provCode=="650000"
set scheme tufte
encode cityCode, gen(id)
gen ti = year - 2010
gen treat = isRestrict
xtset id ti
forvalues i = 5(-1)1{
	gen pre_`i' = (ti == -`i' & treat == 1)
}
forvalues j = 1(1)6{
	gen  post_`j' = (ti == `j' & treat == 1)
}
gen current = (ti == 0 & treat == 1)
drop pre_1
drop if year > 2017
drop if year < 2003
reghdfe lrealHousePrice pre_* current post_* lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare popDensity, absorb(id year) vce(cluster provCode)
//reghdfe lrealWage pre_* current post_*, absorb(id ti) vce(cluster provCode)
coefplot, baselevels ///
keep(pre_* current post_*) ///
levels(96) ///
vertical ///转置图形
yline(0,lcolor(edkblue*0.8)) ///加入y=0这条虚线 
xline(5, lwidth(vthin) lpattern(dash) lcolor(teal)) ///
ylabel(,labsize(*0.75)) xlabel(,labsize(*0.75)) ///
ytitle("Policy effect", size(small)) ///加入Y轴标题,大小small
xtitle("Policy timing", size(small)) ///加入X轴标题，大小small 
addplot(line @b @at) ///增加点之间的连线
ciopts(lpattern(dash) recast(rcap) msize(medium)) ///CI为虚线上下封口
msymbol(circle_hollow) ///plot空心格式
title("Housing Price")
graph save "Output/did/did_hp.gph", replace
graph export "Output/did/did_hp.svg", replace name("Graph")
graph export "Output/did/did_hp.pdf", replace name("Graph")

drop if year > 2018
reghdfe lrealWage pre_* current post_* lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare secondaryIndustryEmploymentShare popDensity, absorb(id) vce(cluster provCode)
coefplot, baselevels ///
keep(pre_* current post_*) ///
levels(95) ///
vertical ///转置图形
yline(0,lcolor(edkblue*0.8)) ///加入y=0这条虚线 
xline(5, lwidth(vthin) lpattern(dash) lcolor(teal)) ///
ylabel(,labsize(*0.75)) xlabel(,labsize(*0.75)) ///
ytitle("Policy effect", size(small)) ///加入Y轴标题,大小small
xtitle("Policy timing", size(small)) ///加入X轴标题，大小small 
addplot(line @b @at) ///增加点之间的连线
ciopts(lpattern(dash) recast(rcap) msize(medium)) ///CI为虚线上下封口
msymbol(circle_hollow) ///plot空心格式
title("Wage")
graph save "Output/did/did_wage.gph", replace
graph export "Output/did/did_wage.svg", replace name("Graph")
graph export "Output/did/did_wage.pdf", replace name("Graph")

//保存回归表格
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
esttab r3 r4 r0 r1 using Output/T1.tex, replace b(%7.3f) star(* 0.1 ** 0.05 *** 0.01) r2 se booktabs drop(_cons lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare popDensity secondaryIndustryEmploymentShare)  

//安慰剂检验
//gen Post = cond(year > 2009, 1, 0)
//gen did = isRestrict * Post
permute did beta=_b[did], reps(500) rseed(123) saving("Output/perm_hp.dta", replace): reghdfe lrealHousePrice did lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare popDensity, absorb(id year) vce(cluster provCode)

use "Output/perm_hp.dta", clear
set scheme tufte
dpplot beta, xline(-0.054, lc(black*0.5) lp(dash)) ///
             xline(0, lc(black*0.5) lp(solid)) ///
			 xlabel(-0.06(0.01)0.02, format(%4.3f) labsize(small)) ///
             xtitle("Estimator", size(*0.8)) ///
             ytitle("Density", size(*0.8)) ///
             ylabel(, nogrid format(%4.1f) labsize(small)) ///
             note("N=500") caption("Permute-HousingPrice")  ///
             graphregion(fcolor(white))
graph save "output/perm_hp.gph", replace
graph export "Output/did/perm_hp.pdf", replace name("Graph")
