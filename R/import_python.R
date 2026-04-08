#' Import Python
#'
#' @description Installing and adding elements to environment to be used in code. User will not interact with this file.
#' @details Importing Python packages, elements, and classes to R.
#' @param
#' @return
#' @export
#' @import reticulate, tidyverse, requests, bs4, pandas, selenium, webdriver_manager
#' @examples

install.packages("reticulate")
library(reticulate)
library(tidyverse)

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
