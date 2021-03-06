setwd('C:/Users/fgsci/OneDrive/Documents/GitHub/cfb-scouting')

library(data.table)

##### Clean NFL Data #########################################

# Read in data
passing <- fread('Data/NFL/passing.csv')
rush.rec <- fread('Data/NFL/rush_receiving.csv')
defense <- fread('Data/NFL/defense.csv')

# Filter out unnecessary data
passing <- passing[, c(1:7, 22)]
rush.rec <- rush.rec[, c(1:7, 19)]
defense <- defense[, c(1:7, 15)]

# Find total games played for all players
passing$sumGP <- with(passing, ave(GP, PlayerID, FUN=sum))
rush.rec$sumGP <- with(rush.rec, ave(GP, PlayerID, FUN=sum))
defense$sumGP <- with(defense, ave(GP, PlayerID, FUN=sum))

# Find total games started for all players
passing$sumGS <- with(passing, ave(GS, PlayerID, FUN=sum))
rush.rec$sumGS <- with(rush.rec, ave(GS, PlayerID, FUN=sum))
defense$sumGS <- with(defense, ave(GS, PlayerID, FUN=sum))

##### Combine Data ###########################################

combine <- fread('Data/combine.csv') # Read in data
combine <- combine[, c(1:13, 16:17)]

# Initially split combine data by desired positions
P.combine <- subset(combine, POS=="QB")
R.combine <- subset(combine, POS %in% c("RB", "WR", "TE"))
D.combine <- subset(combine, POS %in% c("CB", "DB", "DE", "DT",
                                        "EDGE", "FS", "ILB", "S",
                                        "OLB", "LB", "SS", "NT"))

# Right merge NFL data into combine data
PC <- merge(P.combine, passing, by="PlayerID", all.x=TRUE)
RC <- merge(R.combine, rush.rec, by="PlayerID", all.x=TRUE)
DC <- merge(D.combine, defense, by="PlayerID", all.x=TRUE)

# Fill in 0 for desired values for players with no NFL stats
PC$Year.y[is.na(PC$Year.y)] <- 0
RC$Year.y[is.na(RC$Year.y)] <- 0
DC$Year.y[is.na(DC$Year.y)] <- 0

PC$GP[is.na(PC$GP)] <- 0
RC$GP[is.na(RC$GP)] <- 0
DC$GP[is.na(DC$GP)] <- 0

PC$GS[is.na(PC$GS)] <- 0
RC$GS[is.na(RC$GS)] <- 0
DC$GS[is.na(DC$GS)] <- 0

PC$sumGP[is.na(PC$sumGP)] <- 0
RC$sumGP[is.na(RC$sumGP)] <- 0
DC$sumGP[is.na(DC$sumGP)] <- 0

PC$sumGS[is.na(PC$sumGS)] <- 0
RC$sumGS[is.na(RC$sumGS)] <- 0
DC$sumGS[is.na(DC$sumGS)] <- 0

# Only calculate GP and GS for the first four years of career
PC <- subset(PC, Year.y <= (Year.x + 3))
RC <- subset(RC, Year.y <= (Year.x + 3))
DC <- subset(DC, Year.y <= (Year.x + 3))

PC$sumGP4 <- with(PC, ave(GP, PlayerID, FUN=sum))
RC$sumGP4 <- with(RC, ave(GP, PlayerID, FUN=sum))
DC$sumGP4 <- with(DC, ave(GP, PlayerID, FUN=sum))

PC$sumGS4 <- with(PC, ave(GS, PlayerID, FUN=sum))
RC$sumGS4 <- with(RC, ave(GS, PlayerID, FUN=sum))
DC$sumGS4 <- with(DC, ave(GS, PlayerID, FUN=sum))

# Remove unnecessary observations
PC <- PC[!duplicated(PC[, "PlayerYearID.x"]), ]
RC <- RC[!duplicated(RC[, "PlayerYearID.x"]), ]
DC <- DC[!duplicated(DC[, "PlayerYearID.x"]), ]

##### Clean CFB Passing Data #########################################

passing.cfb <- fread('Data/CFB/passing.csv')

# Find max values for various passing stats
passing.cfb$maxCMP <- with(passing.cfb, ave(CMP, CollegeID, FUN=max))
passing.cfb$maxATT <- with(passing.cfb, ave(ATT, CollegeID, FUN=max))
passing.cfb$maxCMPPCT <- with(passing.cfb, ave(`CMP PCT`, CollegeID, FUN=max))
passing.cfb$maxYARDS <- with(passing.cfb, ave(YARDS, CollegeID, FUN=max))
passing.cfb$maxYPA <- with(passing.cfb, ave(YPA, CollegeID, FUN=max))
passing.cfb$maxADJYPA <- with(passing.cfb, ave(`ADJ YPA`, CollegeID, FUN=max))
passing.cfb$maxTD <- with(passing.cfb, ave(TD, CollegeID, FUN=max))
passing.cfb$maxINT <- with(passing.cfb, ave(INT, CollegeID, FUN=max))
passing.cfb$maxRTG <- with(passing.cfb, ave(`PASS RTG`, CollegeID, FUN=max))
passing.cfb$maxTDPCT <- with(passing.cfb, ave(`TD PCT`, CollegeID, FUN=max))
passing.cfb$maxINTPCT <- with(passing.cfb, ave(`INT PCT`, CollegeID, FUN=max))

# Define functions we will need for calculating means
calculate.ADJ.YPA <- function(YARDS, TD, INT, ATT) {
  (YARDS + 20 * TD - 45 * INT) / ATT
}

calculate.RTG <- function(YARDS, TD, CMP, INT, ATT) {
  ((8.4 * YARDS) + (330 * TD) + (100 * CMP) - (200 * INT)) / ATT
}

# Find sums for various passing stats
passing.cfb$sumCMP <- with(passing.cfb, ave(CMP, CollegeID, FUN=sum))
passing.cfb$sumATT <- with(passing.cfb, ave(ATT, CollegeID, FUN=sum))
passing.cfb$sumYARDS <- with(passing.cfb, ave(YARDS, CollegeID, FUN=sum))
passing.cfb$sumTD <- with(passing.cfb, ave(TD, CollegeID, FUN=sum))
passing.cfb$sumINT <- with(passing.cfb, ave(INT, CollegeID, FUN=sum))

# Find career values for various passing stats
passing.cfb$careerCMPPCT <- with(passing.cfb, round(sumCMP / sumATT * 100), 1)
passing.cfb$careerYPA <- with(passing.cfb, round(sumYARDS / sumATT, 1))
passing.cfb$careerADJYPA <- with(passing.cfb, round(calculate.ADJ.YPA(sumYARDS, sumTD, sumINT, sumATT), 1))
passing.cfb$careerRTG <- with(passing.cfb, round(calculate.RTG(sumYARDS, sumTD, sumCMP, sumINT, sumATT), 1))
passing.cfb$careerTDPCT <- with(passing.cfb, round(sumTD / sumATT, 2))
passing.cfb$careerINTPCT <- with(passing.cfb, round(sumINT / sumATT, 2))

# Sort and filter out unnecessary rows, keeping only most recent season
passing.cfb <- passing.cfb[order(passing.cfb$CollegeID, -Year ), ] #sort by ID and Year descending
passing.cfb <- passing.cfb[!duplicated(passing.cfb$CollegeID), ]  # take the first row within each ID

##### Clean CFB Rush/Rec Data #########################################

rush.rec.cfb <- fread('Data/CFB/rush_receiving_shares.csv')

# Find max values for various rushing/rec stats
rush.rec.cfb$maxRUSHATT <- with(rush.rec.cfb, ave(`RUSH ATT`, CollegeID, FUN=max))
rush.rec.cfb$maxRUSHYDS <- with(rush.rec.cfb, ave(`RUSH YDS`, CollegeID, FUN=max))
rush.rec.cfb$maxRUSHYPA <- with(rush.rec.cfb, ave(`RUSH YPA`, CollegeID, FUN=max))
rush.rec.cfb$maxRUSHTD <- with(rush.rec.cfb, ave(`RUSH TD`, CollegeID, FUN=max))
rush.rec.cfb$maxREC <- with(rush.rec.cfb, ave(REC, CollegeID, FUN=max))
rush.rec.cfb$maxRECYDS <- with(rush.rec.cfb, ave(`REC YDS`, CollegeID, FUN=max))
rush.rec.cfb$maxRECYPC <- with(rush.rec.cfb, ave(`REC YPC`, CollegeID, FUN=max))
rush.rec.cfb$maxRECTD <- with(rush.rec.cfb, ave(`REC TD`, CollegeID, FUN=max))
rush.rec.cfb$maxRUSHATTSHARE <- with(rush.rec.cfb, ave(`RUSH ATT SHARE`, CollegeID, FUN=max))
rush.rec.cfb$maxRUSHYDSSHARE<- with(rush.rec.cfb, ave(`RUSH YDS SHARE`, CollegeID, FUN=max))
rush.rec.cfb$maxRUSHTDSHARE <- with(rush.rec.cfb, ave(`RUSH TD SHARE`, CollegeID, FUN=max))
rush.rec.cfb$maxRECSHARE <- with(rush.rec.cfb, ave(`REC SHARE`, CollegeID, FUN=max))
rush.rec.cfb$maxRECYDSSHARE <- with(rush.rec.cfb, ave(`REC YDS SHARE`, CollegeID, FUN=max))
rush.rec.cfb$maxRECTDSHARE <- with(rush.rec.cfb, ave(`REC TD SHARE`, CollegeID, FUN=max))

# Find sums for various rush/rec stats
rush.rec.cfb$sumRUSHATT <- with(rush.rec.cfb, ave(`RUSH ATT`, CollegeID, FUN=sum))
rush.rec.cfb$sumRUSHYDS <- with(rush.rec.cfb, ave(`RUSH YDS`, CollegeID, FUN=sum))
rush.rec.cfb$sumRUSHTD <- with(rush.rec.cfb, ave(`RUSH TD`, CollegeID, FUN=sum))
rush.rec.cfb$sumREC <- with(rush.rec.cfb, ave(REC, CollegeID, FUN=sum))
rush.rec.cfb$sumRECYDS <- with(rush.rec.cfb, ave(`REC YDS`, CollegeID, FUN=sum))
rush.rec.cfb$sumRECTD <- with(rush.rec.cfb, ave(`REC TD`, CollegeID, FUN=sum))

# Find career values for various rush/rec stats
rush.rec.cfb$maxRUSHYPA <- with(rush.rec.cfb, round(sumRUSHYDS / sumRUSHATT, 1))
rush.rec.cfb$maxRECYPC <- with(rush.rec.cfb, round(sumRECYDS / sumREC, 1))

# Sort and filter out unnecessary rows, keeping only most recent season
rush.rec.cfb <- rush.rec.cfb[order(rush.rec.cfb$CollegeID, -Year ), ] #sort by ID and Year descending
rush.rec.cfb <- rush.rec.cfb[!duplicated(rush.rec.cfb$CollegeID), ]  # take the first row within each ID

# Add dummy variables for triple option offenses
rush.rec.cfb$optionoff <- with(rush.rec.cfb,
                              (Team %in% c("Navy", "Air Force")) |
                              (Team == "Nebraska" & Year <= 2003) |
                              (Team == "Syracuse" & Year <= 2001) |
                              (Team == "New Mexico" & Year <= 2006) |
                              (Team == "Rice" & Year <= 2005) |
                              (Team == "Georgia Southern" & (Year <= 2005 | Year >= 2010)) |
                              (Team == "Georgia Tech" & Year %in% c(2008:2018)) |
                              (Team == "Army" & Year >= 2008) |
                              (Team == "New Mexico" & Year >= 2012) |
                              (Team == "Tulane" & Year >= 2016))

# SOURCE: https://en.wikipedia.org/wiki/Option_offense#Teams_that_have_or_currently_run_an_option_offense

##### Clean CFB Defense Data ##########################################

defense.cfb <- fread('Data/CFB/defense_shares.csv')

# Find max values for various rushing/rec stats
defense.cfb$maxTCKL <- with(defense.cfb, ave(`SOLO TCKL`, CollegeID, FUN=max))
defense.cfb$maxTFL <- with(defense.cfb, ave(TFL, CollegeID, FUN=max))
defense.cfb$maxSACK <- with(defense.cfb, ave(SACK, CollegeID, FUN=max))
defense.cfb$maxINT <- with(defense.cfb, ave(INT, CollegeID, FUN=max))
defense.cfb$maxPBU <- with(defense.cfb, ave(PBU, CollegeID, FUN=max))
defense.cfb$maxFF <- with(defense.cfb, ave(FF, CollegeID, FUN=max))
defense.cfb$maxTCKLSHARE <- with(defense.cfb, ave(`SOLO TCKL SHARE`, CollegeID, FUN=max))
defense.cfb$maxTFLSHARE <- with(defense.cfb, ave(`TFL SHARE`, CollegeID, FUN=max))
defense.cfb$maxSACKSHARE <- with(defense.cfb, ave(`SACK SHARE`, CollegeID, FUN=max))
defense.cfb$maxINTSHARE <- with(defense.cfb, ave(`INT SHARE`, CollegeID, FUN=max))
defense.cfb$maxPBUSHARE <- with(defense.cfb, ave(`PBU SHARE`, CollegeID, FUN=max))
defense.cfb$maxFFSHARE <- with(defense.cfb, ave(`FF SHARE`, CollegeID, FUN=max))

# Find sums for various rush/rec stats
defense.cfb$sumSOLOTCKL <- with(defense.cfb, ave(`SOLO TCKL`, CollegeID, FUN=sum))
defense.cfb$sumTFL <- with(defense.cfb, ave(TFL, CollegeID, FUN=sum))
defense.cfb$sumSACK <- with(defense.cfb, ave(SACK, CollegeID, FUN=sum))
defense.cfb$sumINT <- with(defense.cfb, ave(INT, CollegeID, FUN=sum))
defense.cfb$sumPBU <- with(defense.cfb, ave(PBU, CollegeID, FUN=sum))
defense.cfb$sumFF <- with(defense.cfb, ave(FF, CollegeID, FUN=sum))

# Sort and filter out unnecessary rows, keeping only most recent season
defense.cfb <- defense.cfb[order(defense.cfb$CollegeID, -Year ), ] #sort by ID and Year descending
defense.cfb <- defense.cfb[!duplicated(defense.cfb$CollegeID), ]  # take the first row within each ID

##### Merge All Data ##########################################

PC.m <- merge(PC, passing.cfb, by="CollegeID", all.x=TRUE)
RC.m <- merge(RC, rush.rec.cfb, by="CollegeID", all.x=TRUE)
DC.m <- merge(DC, defense.cfb, by="CollegeID", all.x=TRUE)



