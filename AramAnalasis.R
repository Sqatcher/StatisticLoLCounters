setwd("D:/PythonThings/RiotThings/StatisticLoLCounters")
library(tidyverse)
AramData <- read.csv("AramData.csv", sep=";")
head(AramData)
AramData <- subset(AramData, select = -c(teamposition))
head(AramData)

aramWinRatio <- AramData %>%
  group_by(championname) %>%
  summarise(wonGames = sum(win == 't'), lostGames = sum(win == 'f'),
            gamesPlayed = wonGames+lostGames, winRatio = wonGames / gamesPlayed * 100)

aramWinRatio %>%
  arrange(desc(winRatio))

library(plotly)

plotRatio <- plot_ly(aramWinRatio, x = ~gamesPlayed, y = ~winRatio, text = ~championname, 
                     type='scatter', mode = 'markers', name='champions')

plotRatio <- plotRatio %>%
  layout(title = "Win ratio per champion - ARAM Games",
         xaxis = list(showgrid = FALSE),
         yaxis = list(showgrid = FALSE))

plotRatio %>%
  add_trace(y = 50, mode='lines', name="50% ratio")

aramWinRatio %>%
  filter(championname == 'Yasuo')

eps = 0.3
aramWinRatio %>%
  filter(winRatio > (50-eps) & winRatio < (50+eps))

championName = 'Lux'

championGames <- AramData %>%
  filter(championname == championName)

championGames$gameversion <- championGames$gameversion
championGamesByVersion <- championGames %>%
  group_by(gameversion) %>%
  summarize(gamesWon = sum(win=='t'), gamesLost=sum(win=='f'))
championGamesByVersion
# odciecie
championGamesByVersion <- championGamesByVersion %>%
  arrange(desc(gameversion))
rowsNumber <- nrow(championGamesByVersion)
library(dplyr)
championGamesByVersion <- slice(championGamesByVersion, seq(1, by = 1, length.out = 5))
rownames(championGamesByVersion) <- championGamesByVersion$gameversion
championGamesByVersion <- as.data.frame(t(championGamesByVersion))
championGamesByVersion <- championGamesByVersion[-c(1), ]


barplot(as.matrix(championGamesByVersion),
        col = c("blue", "red"),
        main=paste("Games by patch for", championName))
