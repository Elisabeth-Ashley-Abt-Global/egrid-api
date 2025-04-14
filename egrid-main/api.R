library(plumber)

#* @get /hello
function() {
  list(message = "Hello, from R!")
}

#* @get /<year>/plant
function(year) {
  rds_file <- file.path(
    ".", "data", "outputs", year, "plant_file.RDS"
  )
  tryCatch({
    plant_data <- readRDS(rds_file)
    list(success = TRUE, data = plant_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}


#* @get /<year>/balancingauthority
function(year) {
  rds_file <- file.path(".", "data", "outputs", year, "ba_aggregation.RDS")
  tryCatch({
    ba_data <- readRDS(rds_file)
    list(success = TRUE, data = ba_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}

#* @get /<year>/generator
function(year) {
  rds_file <- file.path(".", "data", "outputs", year, "generator_file.RDS")
  tryCatch({
    ba_data <- readRDS(rds_file)
    list(success = TRUE, data = ba_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}

#* @get /<year>/nerc
function(year) {
  rds_file <- file.path(".", "data", "outputs", year, "nerc_aggregation.RDS")
  tryCatch({
    ba_data <- readRDS(rds_file)
    list(success = TRUE, data = ba_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}

#* @get /<year>/state
function(year) {
  rds_file <- file.path(
    ".", "data", "outputs", year, "state_aggregation.RDS"
  )
  tryCatch({
    ba_data <- readRDS(rds_file)
    list(success = TRUE, data = ba_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}

#* @get /<year>/subregion
function(year) {
  rds_file <- file.path(".", "data", "outputs", year, "subregion_file.RDS")
  tryCatch({
    ba_data <- readRDS(rds_file)
    list(success = TRUE, data = ba_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}


#* @get /<year>/unit
function(year) {
  rds_file <- file.path(".", "data", "outputs", year, "unit_file.RDS")
  tryCatch({
    ba_data <- readRDS(rds_file)
    list(success = TRUE, data = ba_data)
  }, error = function(e) {
    list(success = FALSE, error = e$message)
  })
}

#* @get /<year>/us
function(year) {
  rds_file <- file.path(".", "data", "outputs", year, "us_aggregation.RDS")
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
