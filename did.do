use Clean/PanelData.dta, clear
drop if provCode=="650000"
//drop if provCode=="640000"
//drop if provCode=="620000"
//keep if cityType == "地级市"
//drop if cityCode == "411400"
set scheme tufte
encode cityCode, gen(id)
gen ti = year - 2010
drop if year > 2020
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
reghdfe lrealHousePrice pre_* current post_*, absorb(id ti) vce(cluster provCode)
//reghdfe lrealWage pre_* current post_*, absorb(id ti) vce(cluster provCode)
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
title("Housing Price")
graph save "Output/did/did_hp.gph", replace
graph export "Output/did/did_hp.svg", replace name("Graph")
graph export "Output/did/did_hp.pdf", replace name("Graph")

drop if year > 2018
reghdfe laverageWageOfEmployees pre_* current post_* lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare secondaryIndustryEmploymentShare , absorb(id) vce(cluster provCode)
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
