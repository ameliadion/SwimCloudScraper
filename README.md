---
title: "README"
output: html_document
author: "Amelia Dion and Jessie Wang"
editor_options: 
  markdown: 
    wrap: 72
---

**Topic**: Scraping and analyzing data from SwimCloud

**Potential Functionality/Task**: - Take specific data from
[swimcloud](swimcloud.com) and upload to R - Data will include
times,recruiting power index, and swim events - Be able to sort through
data easily and clean it - Analyze swimmer data using R - Create tables
and plots in order to see data over time more easily - Be able to
transform and modify dataset so that users can make meaningful
conclusions about data

**Goal**: The user should be able to easily retrieve a swimmer’s data
from [swimcloud](swimcloud.com) to R and analyze their data using this
package. This can be through both creating plots and tables, or
manipulating and cleaning their data.

**Hierarchy: (hypothetical)**

-   R script to scrape data using python
    -   r version of `getPowerIndex(swimmer_ID)`
    -   r version of `getSwimmerEvents(swimmer_ID)`
    -   r version of `getSwimmerTimes(swimmer_ID, event_name, event_ID)`
        -   function to make a graph of improvement over time
-   Test code
-   Everything else
