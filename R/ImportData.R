
# getPowerIndex <- function(swimmer_ID){
#   # check for type
#   swimmer_url <- "https://swimcloud.com/swimmer/" + as.character(swimmer_ID)
#   headers <-list("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36", "https://google.com/")
#   names(headers) <- c("User-Agent", "Referer")
#   url <- requests::get(swimmer_url, headers)
#
#
# }

library(reticulate)
py_config()

source_python('R/SwimScraper.py', envir = globalenv(), convert = TRUE)
