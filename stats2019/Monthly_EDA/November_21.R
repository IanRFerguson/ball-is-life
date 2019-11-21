library(tidyverse)
library(readxl)
library(MASS)

setwd("~/DATA/SPORTS SCIENCE/NBA/2019/statCompiler/")

data <- read_excel("NBA_Stats_2019.xlsx")
attach(data)

# Evaluate average points between conferences
data %>% 
        group_by(conference) %>% 
        summarise(teams = n(),
                  mean.points = mean(points),
                  mean.win = mean(winpct_tot))

# West - More points (111) and higher average win % (0.52)


## Predicting Win %
# R^2 = 0.918 ... Adjusted R^2 = 0.704
win.model <- lm(winpct_tot ~ . -team -conference, data = data)

# Backwards Selection
# Updated R^2 = 0.911 ... Adjusted R^2 = 0.828
win.step <- stepAIC(win.model)

grand.points <- mean(points)

# "pointDiff" = Team's average points relative to league average
data <- data %>% 
        mutate(pointDiff = points - grand.points)

data.plot <- ggplot(data, aes(x = reorder(team, +points), y = pointDiff, fill = conference)) +
                geom_col() +
                coord_flip() +
                labs(x = "Team", y = "Distance From Avg. Points",
                     title = "Average Points: 110.347") +
                scale_fill_brewer(palette = "Set1")

ggsave("1121_PPG.png", plot = data.plot)

# Western Conference teams more likely to score above league average (9 / 15 teams)
data %>% 
        group_by(conference) %>% 
        summarise(teams = n(),
                  above.avg = sum(pointDiff > 0),
                  below.avg = sum(pointDiff < 0),
                  def.eff = mean(def_eff))

data.plot2 <- ggplot(data, aes(x = conference, y = off_eff, fill = conference)) +
                geom_boxplot() +
                scale_fill_brewer(palette = "Set1") +
                labs(x = "Conference", y = "Offensive Efficiency")

ggsave("1121_OffEff.png", plot = data.plot2)

## Offensive Efficiency
# Dallas = Most efficient (1.1)
# Memphis = Least efficient (1.01)
data %>% 
        filter(conference == "West") %>%
        group_by(team) %>% 
        summarise(off.eff = off_eff) %>% 
        arrange(off.eff)


# Washington = Most efficient (1.09)
# Atlanta = Least efficient (0.994) ... also the worst in the league
data %>% 
        filter(conference == "East") %>%
        group_by(team) %>% 
        summarise(off.eff = off_eff) %>% 
        arrange(off.eff)

data.plot3 <- ggplot(data, aes(x = reorder(team, +off_eff), y = off_eff, fill = conference)) +
                geom_col() +
                scale_fill_brewer(palette = "Set1") +
                theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
                labs(x = "Teams", y = "Offensive Efficiency")

ggsave("1121_OffEff_byTeam.png", plot = data.plot3)
