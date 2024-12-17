This is the README for the Wikipedia Webscraper Project

The first important file regarding the Webscraping Project would be the file named Webscraper2.0.py

This file will be using petscan as a way to parse through the data and get the results of the different persons who in this experiment are American. The depth can be configured with to get more comprehensive results regarding the persons, who will match in the query. The type of persons, or any of the other queries can be configured in the getWikipediaTitlesByCategory Function. The next functions below are mainly specialized for people who have birthdates, and an occupation. These functions will use Regular Expressions in order to find the specific values that the preceding function will scrape from the query that we get from the Wikipedia PetScan. Then the birth dates are processed, and proceeded to be outputted into a for loop, which will then be inputted into csv files for further data analysis. 

In order to get a certain number of year worth of data depending on the year, the closer it is to the present the large the subset, the process for running will be a very long time. 

CSVReader.py

This will mainly just read the txt files generated in the subsequent py file into a csv format which will have the year, pagecreation date, and the occupation in 3 seperate rows

Plotting.py, and Boxplot.py

These two will generate different graphs according to the user. The boxplot.py will generate a boxplot according to a set number of quantiles which can change according to the user's preference. The Plotting.py will mainly generate a violin plot, but easily can be change to a scatterplot as well. 

All the csv files will be uploaded. The depth used to generate the data for all of these csv files was depth = 10. The depth is an important part of the query and can possibly significantly change the results of the generated data depending on what number is used for the depth.