# Python-Web-Scraper
A custom built Web Scraper I am using to gather data for statistical analysis of average typing speeds.

## Table of Contents

- [Python-Web-Scraper](#python-web-scraper)
  * [Overview](#overview)
  * [How to use this project](#how-to-use-this-project)
    + [Downloading the Code from GitHub](#downloading-the-code-from-github)
    + [Downloading Python Interpreter](#downloading-python-interpreter)
    + [Pip packages used in this project](#pip-packages-used-in-this-project)
    + [Running the program in your terminal](#running-the-program-in-your-terminal)


## Overview

This project is being used for my introduction to Statistics class at UCO. In this project, I gathered 4022 random samples of typing speeds from Keyhero.com.
The samples indicate a population average typing speed of 47.07 WPM +- 0.9176 WPM (+-1.95%) [46.15 WPM - 47.985 WPM] with a 99% confidence interval. 

![Keyhero WPM Distribution Image](https://raw.githubusercontent.com/Nellak2017/Python-Web-Scraper/main/Keyhero%20WPM%20Distribution%20Image.PNG)

## How to use this project

To use this project, you must download this github repository, a Python interpreter, and the pip packages used in the project. 
Afterwards, you must then run the program using Python. It will scrape the data from the internet if you don't have the csv, and then display the results in your terminal and display a plot of the results on the next run.

### Downloading the Code from GitHub
1. If you have not already, download the github client from GitHub.
2. Create an empty directory, and open a terminal window in that directory.
3. Perform the following commands in the terminal window: 
```bash
git init
git clone https://github.com/Nellak2017/Python-Web-Scraper.git
```

### Downloading Python Interpreter
1. Navigate to python.org and download the proper Python 3 interpreter for your operating system.
2. Follow online tutorials for setting up the Python Path variables.
3. Verify your python 3 installation by performing the following terminal commands:
```bash
python --version
```
If you see Python followed by a version, then you are ready to move on to the next step.

### Pip packages used in this project

Listed below are all the pip packages this project depends on. For each, you must download them by using the terminal in the same directory as your project code. 

+ requests
+ BeautifulSoup4
+ csv
+ itertools
+ matplotlib

To download them, you must have a terminal open in the project directory, then perform the following command for each module you want to download:
```bash
pip install (module name here)
```
Example:
```bash
pip install matplotlib
```

### Running the program in your terminal

Navigate to your project directory and open a terminal inside.

Perform the following command in the terminal to run the program:

```bash
python -u "c:\... directory path ... \main.py" 
```

On the first run, if you don't have the csv in the correct directory, then it will try to scrape the data off the internet. 
If you have the CSV in the correct location, then it will display the statistical summary in your terminal and will display a plot of the data as well.
