library(dplyr)
library(babynames)
library(streamgraph)

babynames %>%
  filter(grepl("^Kr", name)) %>%
  group_by(year, name) %>%
  tally(wt=n) %>%
  streamgraph("name", "n", "year")
