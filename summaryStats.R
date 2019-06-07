setwd("~")
library(readxl)
library(gdata)

# The spreadsheet below is generated using 2018_NBA.py script
basketballData <- read_excel('~/NBA_Stats.xlsx')
layup <- basketballData[5:27]
skyhook <- colnames(layup)
buildFrame <- data.frame(Stat <- NULL,
                         Min <- numeric(),
                         Mean <- numeric(),
                         Max <- numeric())

k <- 1
j <- 1
for (m in layup) {
        buildFrame[k,1] <- skyhook[k]
        buildFrame[k,2] <- round((min(m)), 2)
        buildFrame[k,3] <- round((mean(m)), 2)
        buildFrame[k,4] <- round((max(m)), 2)
        k <- k + 1
}

write.fwf(x = buildFrame, file = "Summary Stats.txt", quote = FALSE,
          rownames = FALSE, colnames = FALSE)
