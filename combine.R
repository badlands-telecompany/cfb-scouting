setwd('C:/Users/fgsci/OneDrive/Documents/GitHub/cfb-scouting')

library(data.table)
extrafont::loadfonts(device="win") # Call this before importing ggplot2 library
library(ggplot2)

df <- fread('Data/combine_nflcombineresults.csv')
df <- subset(df, year >= 2000)  # Remove old combine data

df$POSgroup <- df$POS
df$POSgroup <- with(df, ifelse(POS %in% c("RB", "FB"), "RB", POSgroup))
df$POSgroup <- with(df, ifelse(POS %in% c("OT", "OG", "C", "G"), "OL", POSgroup))
df$POSgroup <- with(df, ifelse(POS %in% c("DT", "DE", "NT"), "DL", POSgroup))
df$POSgroup <- with(df, ifelse(POS %in% c("ILB", "OLB"), "LB", POSgroup))
df$POSgroup <- with(df, ifelse(POS %in% c("CB", "SS", "FS"), "DB", POSgroup))
df$POSgroup <- with(df, ifelse(POS %in% c("K", "LS", "P"), "SPEC", POSgroup))

themes <- theme(text=element_text(family="Garamond", size=12),
                plot.title=element_text(size=20, 
                                        face="bold",
                                        hjust=0.5,
                                        lineheight=1.2),  # title
                plot.subtitle=element_text(size=15,
                                           face="bold",
                                           hjust=0.5),  # subtitle
                axis.title.x=element_text(family="Garamond",
                                          face="bold",
                                          size=15),  # X axis title
                axis.title.y=element_text(size=15,
                                          family="Garamond",
                                          face="bold"),  # Y axis title
                axis.text.x=element_text(size=10, 
                                         angle = 30,
                                         vjust=.5),  # X axis text
                axis.text.y=element_text(size=10),  # Y axis text
                legend.title=element_text(face="bold"))

#################################################################################

df.40.mean <- aggregate(forty ~ year, data=df, FUN=mean)

mean.40 <- ggplot(data=df.40.mean, aes(x=year, y=forty)) +
             geom_line() +
             geom_point() + 
             labs(title="Mean 40-Yard Speeds Over Time",
                  subtitle="@MeshPointScout",
                  y="Mean 40-Yard Time (s)", x="Year",
                  caption="Data source: NFLcombineresults.com") +
             scale_x_continuous(breaks=seq(2000, 2018, 2)) +
             scale_y_continuous(breaks=seq(4.74, 4.86, 0.01))

mean.40 + themes

#################################################################################

df.40.mean.groups <- aggregate(forty ~ year + POSgroup, data=df, FUN=mean)
df.40.mean.groups <- subset(df.40.mean.groups, POSgroup != "SPEC")

mean.40.groups <- ggplot(data=df.40.mean.groups, aes(x=year, y=forty, col=POSgroup)) +
                   geom_line() +
                   geom_point() + 
                   labs(title="Mean 40-Yard Speeds by Position Group Over Time",
                        subtitle="@MeshPointScout",
                        y="Mean 40-Yard Time (s)", x="Year",
                        caption="Data source: NFLcombineresults.com",
                        col="Position") +
                   scale_x_continuous(breaks=seq(2000, 2018, 2)) +
                   scale_y_continuous(breaks=seq(4.3, 5.4, 0.1)) +
                   scale_color_discrete(breaks=c("OL", "DL", "QB", "TE", "LB", "RB", "DB", "WR"))

mean.40.groups + themes

#######################################################################################

# Test significance of year
test.trend <- lm(forty ~ year, data=df)
summary(test.trend)  # Significant with p-value of almost 0
# Check normality assumption

# Athleticism regression
test <- lm(forty ~ height * weight + year, data=df)
summary(test)
resids <- test$residuals
