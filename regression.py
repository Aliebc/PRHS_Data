import pandas as pd
from plotnine import *

import stata_setup
stata_setup.config("/Applications/Stata", "mp")

from pystata import stata

stata.run(r'''
use Clean/PanelData.dta, clear
drop if provCode=="650000"
encode cityCode, gen(cityCodeI)
xtset cityCodeI year
''')

stata.run(r'''
gen Post = cond(year > 2009, 1, 0)
//keep if year < 2014
//keep if year > 2007
gen pp = isRestrict * Post
gen dp = nDistance * Post

reghdfe lrealHousePrice l.lrealHousePrice lrealWage nDistance lGDP_PerCapita llandAreaResidential tertiaryIndustryEmploymentShare, absorb(year) vce(cluster provCode)
''')