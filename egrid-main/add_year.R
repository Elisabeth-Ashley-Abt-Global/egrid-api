rds_file <- file.path(".", "data", "outputs", "plant_file.RDS")
 
plant_data <- readRDS(rds_file)

# Ensure the data is a data frame
plant_data <- as.data.frame(plant_data)

# Add a 'year' column with the value 2023
plant_data$year <- 2023
 
saveRDS(plant_data, rds_file)

# Check the changes
new_plant_data <- readRDS(rds_file)
head(new_plant_data)
