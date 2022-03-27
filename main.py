'''
Author: Connor Keenum

Date: 26 March 2022

Sources: 
    1. How to Web Scrape in Python - https://realpython.com/beautiful-soup-web-scraper-python/

Description: 
    Entry point for the Python web scraper.

Input/Output:
    input = https://www.keyhero.com/topplayers/?page={page}
    output = csv file containing a random sample of the input data

Other Notes: 
    It may be possible that I cannot do the analysis in excel, so I may have to make another module that performs the analysis.
'''

import requests # library used to scrape data
from bs4 import BeautifulSoup # library used to parse the HTML
import random # library used to generate random numbers for the data sampling
import csv # library used to handle CSV files
from os import path
import re # Regex parsing, to help clean up the scraped data

# X TODO: determine how many samples you need to make to get the 99% confidence interval and +- 2 WPM ~~ 4022 samples
# X TODO: import random module, and use it to randomly sample the data from the website (at a random route between 1 and 6311 (Not visited!), for however many samples you need)
# X TODO: covert the sampled data into a CSV, save the CSV in the same directory as this file
# TODO: get the keyhero sample data (4022 samples) from about 2900 pages+ (Might take a long time!). You will need to debug all the functions leading up to this as well. 

'''
Statistics Notes:

+ When std of pop is not known, you must use the t distribution, degrees of freedom, and the std of the sample to estimate the mean of the population from the sample. (Ch. 7.2)
+ Formula for a specific confidence interval when the pop STD is NOT known: X hat - t_(a/2)(s / sqrt(n)) < mu < X hat + t_(a/2)(s / sqrt(n)) 
+ Formula for determining minimum sample size needed for interval estimate of a population: E = t_(a/2)(s / sqrt(n)) ; n = (s^2 * t_(a/2)^2) / (E^2)

+ Formula for how many samples are needed for a 99% confidence interval, with margin of error = 2, and an unknown sample STD ---> n = s^2 * 1.658944

+ We just need to calculate the STD of the random sample so that we can know how many samples we will need

+ I don't know what the standard deviation of the Population is, however, I know that a good initial estimate would be that the population standard deviation is less than 20 WPM
+ Assuming this initial guess, I will now sample the population with n = 20^2 * 1.658944 samples ==> n = 664 samples 
+ using the range rule of estimating the standard deviation, we get an estimate of STD ~ (200 - 3.07) / 4 ~~ 49.23 ; n = 49.23^2 * 1.658944 ==> n ~ 4022 samples
'''

# This statistics function gives the mean of the sample 
def mean(data):
    return sum(data)/len(data)

# This statistics function gives the median of the data
def median(data):
    sortedData = sorted(data)
    if len(data)%2 != 0:
        return sortedData[int(len(data)/2)]  
    else: 
        return mean([sortedData[int(len(data)/2)],sortedData[int(len(data)/2+1)]])

'''
# Test Median
print(median([3,2,1]))
print(median([4,3,2,1]))
'''

# This statistics function gives the range of the sample
def statRange(data):
    return max(data) - min(data)

# This statistics function gives the variance of the sample
def variance(data):
    variance = 0
    meanData = mean(data)
    for i in data:
        variance += (i - meanData)**2
    return variance / (len(data) - 1)

# This statistics function returns the standard deviation of a list of numbers
def standard_deviation(data):
    return variance(data)**.5

'''
# Test standard_deviation
print(standard_deviation([1,2,3,4,2,3,4,10,5,7,8,11]))
'''

# This will generate a map containing pages with random indices for each page, up to data_points number of total indices
def randomSampleGenerator(data_points, number_of_pages,page_len):  # data_points:int , number_of_pages:int, page_len:int
    rand_indices = {}  # {int:page:[]}
    num_pages = list(range(1, number_of_pages))
    num_indices_page = list(range(1, page_len+1))
    full_pages = {} # {int:page: boolean}
    # {key: value for (key, value) in list(zip(range(1, page_len + 1), [False for x in range(0, page_len)]))}

    for rand in range(data_points):
        page = random.choice(num_pages)  # choose a random page
        rand_page_index = random.choice(num_indices_page)  # choose a random page index [1,50]

        page_keys = list(rand_indices.keys())  # Gets all the keys of the map of pages with random indices

        if page in page_keys:  # if chosen page is in the map
            map_val = rand_indices[page]  # memoize the map value at key = page

            if len(map_val) >= page_len:  # if the page is full
                full_pages[page] = True # set that page to be True in full_pages memo
                for candidate_page in page_keys:  # loop through the keys of the map
                    new_map_val = rand_indices[candidate_page]  # memoize map value at key = candidate_page

                    if len(new_map_val) < page_len:  # if the next page isn't full
                        new_rand_page_index = random.choice(num_indices_page)  # choose a new random index
                        if new_rand_page_index in new_map_val:  # if the new random index is in the map for candidate_page
                            while new_rand_page_index in new_map_val:
                                new_rand_page_index = random.choice(num_indices_page)  # generate a new random number until you can find one that isn't in the map
                            new_map_val.append(new_rand_page_index)  # Then add the random index to the end of the page in the map
                            break
                        else:  # if the new random index is not in the map for candidate_page
                            new_map_val.append(new_rand_page_index)  # Then add the random index to the end of the page in the map
                            break
                    elif len(new_map_val) >= page_len: # if the next page is full
                        full_pages[candidate_page] = True  # set that page to be True in full_pages memo
                # if you got here, it means all the pages in the map are full
                t = sum(list(map(len,list(rand_indices.values())))) # Placed here for the debugger
                if all(list(full_pages.values())): # check and make sure all pages are full and the checksum is correct before proceeding
                    # you want to check and see if you can generate a new page in the map and put in a value
                    if len(page_keys) < number_of_pages-1: # you can make a new key value pair iff the len of the map is less than the number of pages
                        # generate new key value pair, by using the while loop algorithm
                        new_rand_page = random.choice(num_pages)
                        if new_rand_page in page_keys:
                            while new_rand_page in page_keys:
                                new_rand_page = random.choice(num_pages)
                            rand_indices[new_rand_page] = [rand_page_index]
                    # if you can't do that, then that means that you have more samples than data, so you can safely return rand_indices
                    elif t == (page_len*(number_of_pages-1)):
                        return rand_indices


            else:  # if the page is not full
                # generate a new random number until you can find one that isn't in the map
                new_map_val = rand_indices[page]
                new_rand_page_index = random.choice(num_indices_page)
                if new_rand_page_index in new_map_val:
                    while new_rand_page_index in new_map_val:
                        new_rand_page_index = random.choice(num_indices_page)  # generate a new random number until you can find one that isn't in the map, break the loop
                    new_map_val.append(new_rand_page_index)
                else:
                    new_map_val.append(new_rand_page_index)

        else:  # if chosen page is not in the map
            rand_indices[page] = [rand_page_index]  # Will create rand_indices = {..., page:[rand_page_index], ...}

    return rand_indices

'''
# Test random sample generator
a = randomSampleGenerator(4022, 5925, 50)
print(a)
print(len(a))
'''

# data row format: [Number:{data number}, String:{userName}, Number:{wordsPerMinute}, Number:{numberOfGames}, String:{Layout}]
# This function gets data from a page in our corpus and returns a list of the data
# See also: https://realpython.com/beautiful-soup-web-scraper-python/
def getPageData(pageNum):
    li = [] # cleaned data for every row in every page. Each element is a string. If you want to use the data, you must put it in the format expected.
    Query = "?page="+str(pageNum)+"&games=0"
    URL = "https://www.keyhero.com/topplayers/"+Query # base URL to be scraped + the actual route

    page = requests.get(URL) # GET request to the URL. Returns the HTML of the page requested.
    soup = BeautifulSoup(page.content, "html.parser")

    for item in soup.select("tr"):
        # Before we add the collected data to li, we must first clean it
        # 1. split the string on "/n". Example: --> ['', '1', '_-uivb.tysekgol', '200.00 WPM', '', '          ', '          1 games', '          ', '        ', ' ', '']
        v = item.get_text().split("\n")
        # 2. loop through the split string, remove the empty strings, strip the string, and remove uneeded information added too. Example: -->  ['1', '_-uivb.tysekgol', '200.00', '1']
        t = []
        for td in range(len(v)):
            if len(v[td].strip()) != 0:
                t.append(v[td].strip())

        # See also: https://pythex.org/
        t[0] = int(re.sub("[^0-9.]","",t[0])) # Turn player Id into int and filter A-Z out
        t[2] = float(re.sub("[^0-9.]","",t[2])) # Turn WPM into float and filter A-Z out
        if len(re.sub("[^0-9.]","",t[3])) == 0:
            pass # if number of games is invalid, don't count this row
        else:
            t[3] = int(re.sub("[^0-9.]","",t[3])) # Turn games number into int and filter A-Z out
            # 3. put the cleaned string into li, this is your page data
            li.append(t)
        
    return li

'''
# Test getPageData
print(getPageData(2))
'''

# This will efficiently randomly sample our corpus, getting all the data for a page before moving on to the next page
# Returns a list of the randomly sampled data
def randomSample(map): # input --> map: {page1:[indices to sample], pagen: [indices to sample]}
    rand_vals = [] # [[1,'user',100.00,1,'QWERTY',...],[...]]
    rand_indices = map # {1:[1,4,5],4:[1,5],...}
    # We must loop over the rand_indices, and pull the relevant data from each page
    for page in rand_indices.keys():
        print("Page: ",page)
        # Get the page data
        data = getPageData(page)
        # Get the information we need from the page
        rand_vals.append([data[x] for x in rand_indices[page]])

    return rand_vals

'''
# Test randomSample

print("a:")
print(a) # 4022, 5925, 50
print("")
print(randomSample(a))
print("")
'''

# Driver for this application, it will return the filled out CSV file with all the scraped data if there wasn't one already in this directory
def main():
    # CSV file name
    filename = "keyhero_sample_data.csv"

    # Check if csv file is created
    if path.exists("keyhero_sample_data.csv"): # If a csv exists, then read the data from it and perform analysis on it
        # initializing the titles and rows list
        fields = []
        rows = []

        # reading csv file
        # see also: https://www.geeksforgeeks.org/working-csv-files-python/
        with open(filename, 'r') as csvfile:
            # creating a csv reader object
            csvreader = csv.reader(csvfile)
            
            # extracting field names through first row
            fields = next(csvreader)
        
            # extracting each data row one by one
            for row in csvreader:
                rows.append(row)

        # Calculate Min, Max, Median, Mean, Variance, and the Standard Deviation for the data
        
        d = []
        for row in range(len(rows)):
            d.append(float(rows[row][2]))

        print("Size of sample:            ",len(d))
        print("Min of wpm:                ",min(d))
        print("Max of wpm:                ",max(d))
        print("Median of wpm:             ",median(d))
        print("Mean of wpm:               ",mean(d))
        print("Variance of wpm:           ",variance(d))
        print("Standard Deviation of wpm: ",standard_deviation(d))
        
         
    else: # If a csv does not exist, then gather the data from the Corpus and output it to CSV in this directory
        # field names
        fields = ['Player Id', 'Username', 'WPM', 'Games Played', 'Layout'] 

        # data rows of csv file, given by scraping the Keyhero corpus. See also: https://www.keyhero.com/topplayers/
        a = randomSampleGenerator(10, 3, 50)
        rows = randomSample(a) # We will test this for only 1 page for now
        print(rows)

        # writing to CSV file
        with open(filename, 'w', newline='\n', encoding='utf-8') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
            
            # writing the fields
            csvwriter.writerow(fields)
            
            # writing the data rows
            csvwriter.writerows(rows)

if __name__ == '__main__':
    main()