library(plumber)

#* @get /hello
function() {
  list(message = "Hello, from R!")
}

#* @get /plant
function() {
  rds_file <- file.path(".", "data", "outputs", "plant_file.RDS")
  tryCatch({
    plant_data <- readRDS(rds_file)
    list(success = TRUE, data = plant_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}


#* @get /balancingauthority
function() {
  rds_file <- file.path(".", "data", "outputs", "ba_aggregation.RDS")
  tryCatch({
    ba_data <- readRDS(rds_file)
    list(success = TRUE, data = ba_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}

#* @get /generator
function() {
  rds_file <- file.path(".", "data", "outputs", "generator_file.RDS")
  tryCatch({
    ba_data <- readRDS(rds_file)
    list(success = TRUE, data = ba_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}

#* @get /nerc
function() {
  rds_file <- file.path(".", "data", "outputs", "nerc_aggregation.RDS")
  tryCatch({
    ba_data <- readRDS(rds_file)
    list(success = TRUE, data = ba_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}

#* @get /state
function() {
  rds_file <- file.path(".", "data", "outputs", "state_aggregation.RDS")
  tryCatch({
    ba_data <- readRDS(rds_file)
    list(success = TRUE, data = ba_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}

#* @get /subregion
function() {
  rds_file <- file.path(".", "data", "outputs", "subregion_file.RDS")
  tryCatch({
    ba_data <- readRDS(rds_file)
    list(success = TRUE, data = ba_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}


#* @post /process
#* @param input_data:string
function(input_data) {
  processed <- toupper(input_data) # Example: Make input uppercase
  list(processed_data = processed)
}
