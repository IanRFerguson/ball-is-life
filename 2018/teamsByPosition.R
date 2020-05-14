library(dplyr)
library(statsr)
library(ggplot2)
library(readxl)

ratings <- '~/DATA/SPORTS SCIENCE/NBA/2019/efficiencyRatings_2018.xlsx'
ratings <- read_excel(ratings)
attach(ratings)

ratings$AST = as.numeric(ratings$AST)
ratings$MP = as.numeric(ratings$MP)
ratings$`eFG%` = as.numeric(ratings$`eFG%`)
ratings <- ratings[!ratings$Tm == 'TOT', ]

ratings %>%
        group_by(ratings$Pos) %>%
        summarise(n = n(), 
                  'Field Goal' = mean(AST, na.rm = TRUE),
                  'Minutes' = mean(MP, na.rm = TRUE))


ggplot(data = ratings, aes(x = Tm, fill = Pos)) + 
        geom_bar() + 
        theme(axis.text.x = element_text(angle = 90, hjust = 1)) +
        labs(x = 'Team', y = 'Count by Position')
