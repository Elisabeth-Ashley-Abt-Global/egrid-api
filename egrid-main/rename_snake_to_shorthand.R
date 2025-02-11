

# load name matches from snake_case to shorthand vars
setwd('C:/Users/AshleyE/Desktop/egrid/egrid-main')
 
source("scripts/name_matching.R")
library(dplyr)


rds_file <- file.path(".", "data", "outputs", "plant_file.RDS")
# read in plant file and rename with shorthand vars
plant_file <- 
  readRDS(rds_file) %>% 
  rename_with(~ tolower(names(plant_nonmetric))[which(as_tibble(plant_nonmetric)$value == .x)], .cols = as_tibble(plant_nonmetric)$value) 

saveRDS(plant_file, file = file.path(".", "data", "outputs", "plant_file.RDS"))
 