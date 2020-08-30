# ------- Imports + Setup Environment
rm(list=ls())
library(tidyverse)
library(MASS)
library(Rfast)

path <- "~/DATA/04_SPORTS/00_NBA/2019/Applied ML/WAR/"                  # Local file path
setwd(path)

nba <- read_csv("Stats-and-Salaries.csv")                               # Read in CSV from .py script

# Custom histogram function
fastHistogram <- function(FEAT) {
        nba %>% ggplot(aes(x = FEAT)) +
                geom_histogram(color="white", bins = 50) +
                theme_minimal()
}

# ------- Clean + Transform
nba$Salary <- as.numeric(gsub("[\\$,]", "", nba$Salary))                # Convert salary to int value

nba <- nba %>% 
        mutate("PPM" = PTS / MP, "APM" = AST/MP)                        # Points / Minute and Assists / Minute

nba.reduced <- nba %>% 
        dplyr::select(!c("Rk", "Player", "Tm", "Pos")) %>% 
        na.omit()

sapply(nba.reduced, function(x) skew(x))                                # Calculate column-wise kurtosis

# ------- Build Model
base.model <- lm(log(Salary) ~ ., data = nba.reduced)                   # Build model with all features
summary(base.model)

# Log-transform points and 2-point attempts
base.model <- stats::update(base.model, . ~ . -PTS +log(PTS) -`2PA` +log(`2PA`))

# Select optimal variables via AIC stepwise selection
base.model <- MASS::stepAIC(base.model, 
                            direction = "both",
                            k = 2,
                            trace = F, 
                            steps = 1000)

# ------- Predictions
nba["PREDICTIONS"] <- exp(predict(base.model, nba))                     # Predict salaries with our optimal model

# Plot actual vs. predicted salaries
nba %>%
        ggplot(aes(x = Salary, y = PREDICTIONS)) +
        geom_point(alpha=0.65, size=(nba$MP / 400), color="dodgerblue") +
        geom_smooth(color="white", alpha=0.65) +
        theme_minimal() +
        labs(x = "Actual Salary", 
             y = "Predicted Salary",
             title = "Salary Prediction Model") +
        theme(plot.title = element_text(hjust = 0.5, face="bold"))

# Who is overpaid and who is underpaid, based on the results of this model?
nba <- nba %>%
        mutate("Salary.Differntial" = PREDICTIONS - Salary,
               "Overpaid" = ifelse(Salary.Differntial < 0, "Overpaid", "Underpaid"))

write.table(x = nba, file = "NBA-Salary-Assertions.csv", sep = ",")     # Push table to CSV

