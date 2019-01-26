setwd('C:/Users/fgsci/OneDrive/Documents/GitHub/cfb-scouting')

library(data.table)

passing <- fread('Data/NFL/passing.csv')
rush_receiving <- fread('Data/NFL/rush_receiving.csv')
defense <- fread('Data/NFL/defense.csv')

passing$sumGP <- with(passing, ave(GP, `Player ID`, FUN=sum))
rush_receiving$sumGP <- with(rush_receiving, ave(GP, `Player ID`, FUN=sum))
defense$sumGP <- with(defense, ave(GP, `Player ID`, FUN=sum))

passing$sumGS <- with(passing, ave(GS, `Player ID`, FUN=sum))
rush_receiving$sumGS <- with(rush_receiving, ave(GS, `Player ID`, FUN=sum))
defense$sumGS <- with(defense, ave(GS, `Player ID`, FUN=sum))

passing$minYear <- with(passing, ave(Year, `Player ID`, FUN=min))
rush_receiving$minYear <- with(rush_receiving, ave(Year, `Player ID`, FUN=min))
defense$minYear <- with(defense, ave(Year, `Player ID`, FUN=min))

RC.passing <- subset(passing, Year <= (minYear + 3))