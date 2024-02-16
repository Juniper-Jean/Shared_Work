length(which(R2[which(R2$R_squared > 0.6),]$model == 'Boltzmann-Arrhenius')) / length(which(R2$model == 'Boltzmann-Arrhenius'))

length(which(Sch_SE[which(Sch_SE$standard_error > 0.6),]$parameter == 'B0')) /
  length(which(Sch_SE$parameter == 'B0'))




which(Sch_SE[which(Sch_SE$standard_error),]$parameter == 'B0')

max(Sch_SE[which(Sch_SE$parameter == 'B0'),]$standard_error)
dim(Sch_SE)[1] / 4

length(which(Sch_SE[which(Sch_SE$standard_error > 100),]$parameter == 'E')) /
  length(which(Sch_SE$parameter == 'E'))
# why 2

match(
  results[which(results$Sch_E_SE > 100),]$ID,
  unlist(no_rise)
  )

length(which(Sch_SE[which(Sch_SE$standard_error > 50),]$parameter == 'Ed')) /
  length(which(Sch_SE$parameter == 'Ed'))

match(
  results[which(results$Ed_SE > 10),]$ID,
  unlist(no_fall)
)



length(which(results$AIC_Schoolfield < results$AIC_cubic)) # 607
Sch_AIC_lessthan_cubic <- results[which(results$AIC_Schoolfield < results$AIC_cubic),]
# ID_Sch_AIC_lessthan_cubic <- results[which(results$AIC_Schoolfield < results$AIC_cubic),]$ID
length(which(Sch_AIC_lessthan_cubic$R_squared_cubic < 0.6)) / 607
length(which(Sch_AIC_lessthan_cubic$R_squared_Sch < 0.6)) / 607
ID_lowR2_Sch_AIC_less <- Sch_AIC_lessthan_cubic[which(Sch_AIC_lessthan_cubic$R_squared_cubic < 0.6),]$ID

length(which(results$AIC_cubic < results$AIC_Schoolfield)) # 1329
cubic_AIC_lessthan_Sch <- results[which(results$AIC_cubic < results$AIC_Schoolfield),]
# ID_cubic_AIC_lessthan_Sch <- results[which(results$AIC_cubic < results$AIC_Schoolfield),]$ID
length(which(cubic_AIC_lessthan_Sch$R_squared_Sch < 0.6)) / 1329
length(which(cubic_AIC_lessthan_Sch$R_squared_cubic < 0.6)) / 1329
ID_lowR2_cubic_AIC_less <- cubic_AIC_lessthan_Sch[which(cubic_AIC_lessthan_Sch$R_squared_Sch < 0.6),]$ID


length(which(results$AIC_Boltzmann < results$AIC_cubic)) # 139
BoltAIC_lessthan_cubic <- results[which(results$AIC_Boltzmann < results$AIC_cubic),]
length(which(BoltAIC_lessthan_cubic$R_squared_Bolt > 0.6)) / 139
# caveat

results_curve_rise_only <- results[which(results$ID %in% curve_rise_only),]
BoltAIC_lessthan_cubic <- which(results_curve_rise_only$AIC_Boltzmann < results_curve_rise_only$AIC_cubic)
length(BoltAIC_lessthan_cubic) # 94
sum(results_curve_rise_only[BoltAIC_lessthan_cubic,]$R_squared_cubic > 0.9) # 81
81 / 94 # note: not universal code - not reproducible worflow/analysis


Tpk_est_implausible <- results[which(results$Tpk > 400),]
length(which(Tpk_est_implausible$ID %in% unlist(curve_rise_only))) / # 259
  length(Tpk_est_implausible$ID)

Tpk_est_implausible <- results[which(results$Tpk > (50 + 273.15)),]
length(which(unlist(curve_rise_only) %in% Tpk_est_implausible$ID)) / # 259
  length(Tpk_est_implausible$ID)

length(results[(results$Tpk > 293.15) & (results$Tpk < 333.15),]$ID) / 1947

# E
min(results$Sch_E, na.rm = T)
length(which(results$Sch_E < 0.1)) /
  sum(!is.na(results$Sch_E))

min(results$Ed, na.rm = T)
length(which(results$Sch_E < 1)) /
  sum(!is.na(results$Sch_E))

min(results$Sch_B0, na.rm = T)
length(which(results$Sch_E < 1)) /
  sum(!is.na(results$Sch_E))


max(results$Sch_E_SE, na.rm = T)
length(which(results$Sch_E_SE < 0.001)) /
  sum(!is.na(results$Sch_E))


Bolt_lowestAIC <- results[results$Best_model == 'Boltzmann',]
length(which(Bolt_lowestAIC$ID %in% curve_rise_only))

d <- subset(thermal_data, thermal_data$FinalID == 'MTD2462')
res_d <- subset(results, results$ID == 'MTD2462')
plot(d$TempK, log(d$Trait_minus_min_plus1))
mod <- Schoolfield(res_d$Sch_B0, res_d$Sch_E, res_d$Ed, res_d$Tpk, d$TempK)
lines(d$TempK, mod)


results_initial_decrease
# results_initial_decrease <- results[which(results$ID %in% unlist(initial_decrease)),]
length(which(results_initial_decrease$R_squared_Sch < 0.6)) /
  sum(!is.na(results_initial_decrease$R_squared_Sch))
