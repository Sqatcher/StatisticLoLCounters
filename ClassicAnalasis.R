setwd("D:/PythonThings/RiotThings/StatisticLoLCounters")
library(plyr)
library(tidyverse)
library(plotly)
gameData <- read.csv("ClassicGamesData.csv", sep=";")

plotData <- gameData %>%
  group_by(championname) %>%
  summarise(wonGames = sum(win=='t'), lostGames = sum(win=='f'), 
            gamesPlayed = wonGames + lostGames, winRatio = wonGames/gamesPlayed * 100)

plotGraph1 <- plot_ly(plotData, x=~gamesPlayed, y=~winRatio, text=~championname,
                      type='scatter', mode='markers', name='champions')

plotGraph1 <- plotGraph1 %>%
  layout(title = "Win ratio per champion - CLASSIC Games",
         xaxis = list(showgrid = FALSE),
         yaxis = list(showgrid = FALSE))

plotGraph1 %>%
  add_trace(y = 50, mode='lines', name="50% ratio")


# lane counters
myEnemy = 'Nasus'
myRole = 'UTILITY'        #TOP JUNGLE MIDDLE BOTTOM UTILITY
showMe = 'Hecarim'

enemyChampionMatches <- gameData %>%
  filter(teamposition == myRole) %>%
  group_by(matchid) %>%
  filter(championname == myEnemy) %>%
  summarise(matchid)
  
matches <- data.frame(match_df(gameData, enemyChampionMatches, on = "matchid"))

counterData <- matches %>%
  filter(teamposition == myRole) %>%
  filter(championname != myEnemy) %>%
  group_by(championname) %>%
  summarise(gamesWon = sum(win=='t'),
            gamesLost = sum(win=='f'),
            gamesPlayed = gamesWon+gamesLost,
            winRatio = gamesWon/gamesPlayed * 100)

counterPlot <- plot_ly(counterData,
                       x = ~gamesPlayed, y = ~winRatio,
                       type='scatter', mode='markers',
                       text=~championname,
                       name='champions')
counterPlot <- counterPlot %>%
  layout(title=paste("Champion counters for", myEnemy, "playing", myRole),
         xaxis = list(showgrid = FALSE),
         yaxis = list(showgrid = FALSE))

counterPlot %>%
  add_trace(y = 50, mode='lines', name="50% ratio")

counterData %>%
  filter(championname == showMe)