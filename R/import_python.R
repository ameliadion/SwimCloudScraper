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

py_install("pandas")
pandas <- import("pandas")

time <- import("time")

py_install("selenium")
selenium <- import("selenium")
webdriver <- selenium$webdriver

By <- selenium$webdriver$common$by$By

WebDriverWait <- selenium$webdriver$support$ui$WebDriverWait

EC <- selenium$webdriver$support$expected_conditions

Select <- selenium$webdriver$support$ui$Select

Options <- selenium$webdriver$chrome$options$Options

TimeoutException <- selenium$common$exceptions$TimeoutException

NoSuchElementException <- selenium$common$exceptions$NoSuchElementException

StaleElementReferenceException  <- selenium$common$exceptions$StaleElementReferenceException

ActionChains <- selenium$webdriver$common$action_chains$ActionChains

py_install("webdriver_manager")
webdriver_manager <- import("webdriver_manager")
ChromeDriverManager <- webdriver_manager$chrome$ChromeDriverManager


library(tidyverse)
