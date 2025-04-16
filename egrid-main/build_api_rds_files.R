
#' build_api_rds_files
#'
#' Build RDS files ready for use within API and using shorthand column names 
#'
#' @param year data year as a string
#' @param datatype data type as a string, either "rds" or "excel"
#' @return new version of production model outputs with lowercase shorthand names 

build_api_rds_files <- function(year, filetype) {
  
  require(dplyr)
  require(readr)
  require(readxl)
  
  # load name matches from snake_case to shorthand vars
  source("scripts/name_matching.R")
  
  if(filetype == "rds") {
    # unit convert to shorthand names
    if(file.exists(file.path(".", "egrid_outputs", year, "unit_file.RDS"))) { 
      unit_file <- 
        read_rds(file.path(".", "egrid_outputs", year, "unit_file.RDS")) %>% 
        rename_with(~ tolower(names(unit_nonmetric))[which(as_tibble(unit_nonmetric)$value == .x)], .cols = as_tibble(unit_nonmetric)$value) 

      write_rds(unit_file, (file.path(".", "egrid_outputs", year, "unit_file.RDS")))
    } else { 
      print(glue::glue("unit_file.RDS does not exist in {file.path('.', 'egrid_outputs', year)}"))
      }  

    # generator convert shorthand names
    if(file.exists(file.path(".", "egrid_outputs", year, "generator_file.RDS"))) { 
      generator_file <- 
        read_rds((file.path(".", "egrid_outputs", year, "generator_file.RDS"))) %>% 
        rename_with(~ tolower(names(gen_nonmetric))[which(as_tibble(gen_nonmetric)$value == .x)], .cols = as_tibble(gen_nonmetric)$value) 

      write_rds(unit_file, (file.path(".", "egrid_outputs", year, "generator_file.RDS")))
    } else { 
      print(glue::glue("generator_file.RDS does not exist in {file.path('.', 'egrid_outputs', year)}"))
      }

    # plant file convert shorthand names
    if(file.exists(file.path(".", "egrid_outputs", year, "plant_file.RDS"))) { 
      plant_file <- 
        read_rds(file.path(".", "egrid_outputs", year, "plant_file.RDS")) %>% 
        rename_with(~ tolower(names(plant_nonmetric))[which(as_tibble(plant_nonmetric)$value == .x)], .cols = as_tibble(plant_nonmetric)$value) 
  
      write_rds(unit_file, (file.path(".", "egrid_outputs", year, "plant_file.RDS")))
    } else { 
      print(glue::glue("plant_file.RDS does not exist in {file.path('.', 'egrid_outputs', year)}"))
    }  

    # state file convert shorthand names
    if(file.exists(file.path(".", "egrid_outputs", year, "state_aggregation.RDS"))) { 
      state_file <- 
        read_rds(file.path(".", "egrid_outputs", year, "state_aggregation.RDS")) %>% 
        rename_with(~ tolower(names(state_nonmetric))[which(as_tibble(state_nonmetric)$value == .x)], .cols = as_tibble(state_nonmetric)$value) 
      
      write_rds(state_file, (file.path(".", "egrid_outputs", year, "state_aggregation.RDS")))
    } else { 
      print(glue::glue("state_aggregation.RDS does not exist in {file.path('.', 'egrid_outputs', year)}"))
    }  
    
    # BA file convert shorthand names
    if(file.exists(file.path(".", "egrid_outputs", year, "ba_aggregation.RDS"))) { 
      ba_file <- 
        read_rds(file.path(".", "egrid_outputs", year, "ba_aggregation.RDS")) %>% 
        rename_with(~ tolower(names(ba_nonmetric))[which(as_tibble(ba_nonmetric)$value == .x)], .cols = as_tibble(ba_nonmetric)$value) 
      
      write_rds(ba_file, (file.path(".", "egrid_outputs", year, "ba_aggregation.RDS")))
    } else { 
      print(glue::glue("ba_aggregation.RDS does not exist in {file.path('.', 'egrid_outputs', year)}"))
    }  

    # NERC file convert shorthand names
    if(file.exists(file.path(".", "egrid_outputs", year, "nerc_aggregation.RDS"))) { 
      nerc_file <- 
        read_rds(file.path(".", "egrid_outputs", year, "nerc_aggregation.RDS")) %>% 
        rename_with(~ tolower(names(nerc_nonmetric))[which(as_tibble(nerc_nonmetric)$value == .x)], .cols = as_tibble(nerc_nonmetric)$value) 
      
      write_rds(nerc_file, (file.path(".", "egrid_outputs", year, "nerc_aggregation.RDS")))
    } else { 
      print(glue::glue("nerc_aggregation.RDS does not exist in {file.path('.', 'egrid_outputs', year)}"))
    }  

    # subregion file convert shorthand names
    if(file.exists(file.path(".", "egrid_outputs", year, "subregion_aggregation.RDS"))) { 
      subregion_file <- 
        read_rds(file.path(".", "egrid_outputs", year, "subregion_aggregation.RDS")) %>% 
        rename_with(~ tolower(names(subregion_nonmetric))[which(as_tibble(subregion_nonmetric)$value == .x)], .cols = as_tibble(subregion_nonmetric)$value) 
      
      write_rds(subregion_file, (file.path(".", "egrid_outputs", year, "subregion_aggregation.RDS")))
    } else { 
      print(glue::glue("subregion_aggregation.RDS does not exist in {file.path('.', 'egrid_outputs', year)}"))
    }  

    # US file convert shorthand names
    if(file.exists(file.path(".", "egrid_outputs", year, "us_aggregation.RDS"))) { 
      us_file <- 
        read_rds(file.path(".", "egrid_outputs", year, "us_aggregation.RDS")) %>% 
        rename_with(~ tolower(names(us_nonmetric))[which(as_tibble(us_nonmetric)$value == .x)], .cols = as_tibble(us_nonmetric)$value) 
      
      write_rds(us_file, (file.path(".", "egrid_outputs", year, "us_aggregation.RDS")))
    } else { 
      print(glue::glue("us_aggregation.RDS does not exist in {file.path('.', 'egrid_outputs', year)}"))
    }  
    
    } else if (filetype == "excel") { # create RDS files from excel data
    
    year_abb <- as.numeric(year) %% 1000
    
    # unit convert to shorthand names
    if(file.exists(file.path(".", glue::glue("egrid{year}_data.xlsx")))) { 
      unit_file <-
        read_excel(file.path(".", glue::glue("egrid{year}_data.xlsx")),
                  sheet = glue::glue("UNT{year_abb}"),
                  skip = 1) %>%
        janitor::clean_names() %>%
        rename("sequnt" = glue::glue("sequnt{year_abb}"), 
               any_of(c("capdflag" = "camdflag"))) 
        
      write_rds(unit_file, file.path(".", "egrid_outputs", year, "unit_file.RDS"))
  
      # generator convert shorthand names
      generator_file <-
        read_excel(file.path(".", glue::glue("egrid{year}_data.xlsx")),
                  sheet = glue::glue("GEN{year_abb}"),
                  skip = 1) %>%
        janitor::clean_names() %>%
        rename("seqgen" = glue::glue("seqgen{year_abb}")) 
  
      write_rds(generator_file, file.path(".", "egrid_outputs", year, "generator_file.RDS"))
  
      # plant file convert shorthand names
      plant_file <- 
        read_excel(file.path(".", glue::glue("egrid{year}_data.xlsx")), 
                  sheet = glue::glue("PLNT{year_abb}"), 
                  skip = 1) %>%
        janitor::clean_names() %>%
        rename("seqplt" = glue::glue("seqplt{year_abb}"), 
               any_of(c("capdflag" = "camdflag"))) 
  
      write_rds(plant_file, file.path(".", "egrid_outputs", year, "plant_file.RDS"))
  
      # state file convert shorthand names
      state_file <- 
        read_excel(file.path(".", glue::glue("egrid{year}_data.xlsx")), 
                  sheet = glue::glue("ST{year_abb}"), 
                  skip = 1) %>%
        janitor::clean_names() 
  
      write_rds(state_file, file.path(".", "egrid_outputs", year, "state_aggregation.RDS"))
  
      # BA file convert shorthand names
      ba_file <- 
        read_excel(file.path(".", glue::glue("egrid{year}_data.xlsx")), 
                  sheet = glue::glue("BA{year_abb}"), 
                  skip = 1) %>%
        janitor::clean_names() 
  
      write_rds(ba_file, file.path(".", "egrid_outputs", year, "ba_aggregation.RDS"))
  
      # NERC file convert shorthand names
      nerc_file <- 
        read_excel(file.path(".", glue::glue("egrid{year}_data.xlsx")), 
                  sheet = glue::glue("NRL{year_abb}"), 
                  skip = 1) %>%
        janitor::clean_names() 
  
      write_rds(nerc_file, file.path(".", "egrid_outputs", year, "nerc_aggregation.RDS"))
  
      # subregion file convert shorthand names
      subregion_file <- 
        read_excel(file.path(".", glue::glue("egrid{year}_data.xlsx")), 
                  sheet = glue::glue("SRL{year_abb}"), 
                  skip = 1) %>%
        janitor::clean_names() 
  
      write_rds(subregion_file, file.path(".", "egrid_outputs", year, "subregion_aggregation.RDS"))
  
      # US file convert shorthand names
      us_file <- 
        read_excel(file.path(".", glue::glue("egrid{year}_data.xlsx")), 
                  sheet = glue::glue("US{year_abb}"),
                  skip = 1) %>%
        janitor::clean_names() 
  
      write_rds(us_file, file.path(".", "egrid_outputs", year, "us_aggregation.RDS"))
    } else {
      print(glue::glue("egrid{year}_data.xlsx does not exist in {file.path('.', 'egrid_outputs', year)}"))
    }
  }
}