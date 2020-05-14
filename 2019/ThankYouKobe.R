library(tidyverse)
library(htmltab)

kobe <- htmltab(doc = 'https://www.basketball-reference.com/players/b/bryanko01.html',
                which = "//caption[starts-with(text(), 'Per Game')]/ancestor::table")

kobe[, 6:length(colnames(kobe))] <- lapply(kobe[, 6:length(colnames(kobe))], function(x) as.numeric(x))

# Points Per Season
kobe %>% 
        ggplot(aes(x = Season, y = PTS, color = "purple")) +
        geom_col(fill = "purple") + 
        theme(axis.text.x = element_text(angle = 45, hjust = 1),
              legend.position = "non")

# Points Per Minute
kobe <- kobe %>% 
        mutate(PPM = PTS / MP)

ppm <- kobe %>% 
        ggplot(aes(x = Season, y = PPM, color = "purple")) +
        geom_col(fill = "purple") +
        ggtitle("Thank You Kobe") +  
        theme(axis.text.x = element_text(angle = 45, hjust = 1),
              legend.position = "non",
              plot.title = element_text(hjust = 0.5))

ggsave(filename = "Kobe_PPM.jpg", plot = ppm)
