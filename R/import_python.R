#' Title Here
#'
#' @description Add brief description to function(s)
#' @details Specifics about functionality, inputs, etc.
#' @param input Brief description of input. (Add as many params as needed)
#' @return Brief description of what function returns/prints.
#' @export Added here to export function to user (text not needed here)
#' @import package Import package used to supplement function. (Add as many as needed)
#' @examples
#' Put function call as example.
#'
install.packages("reticulate")
library(reticulate)

py_install("requests")
requests <- import("requests")
csv <- import("csv")


py_install("bs4")
bs4 <- import("bs4")
bs <- bs4$BeautifulSoup

#py_install("beautifulsoup4")
#bs_test <- import("beautifulsoup4")


py_install("pandas")
pandas <- import("pandas")


time <- import("time")

py_install("selenium")
selenium <- import("selenium")
webdriver <- selenium$webdriver

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import StaleElementReferenceException
# from selenium.webdriver.common.action_chains import ActionChains
# from webdriver_manager.chrome import ChromeDriverManager

library(tidyverse)
