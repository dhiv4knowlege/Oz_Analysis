import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import datetime
from dateutil.relativedelta import relativedelta

# Main logic to get find the location of the data on the web page
def get_results(main_page):
    for link in main_page:
        temp = link.find_all(attrs= {'class' : "results-number-set__number--ns1 css-kk5y6-Root eik1jin0"})
        main_numbers.append([x.get_text() for x in temp])
        powerball.append(link.find(attrs= {'class' : "results-number-set__number--ns2 css-1esp5ap-Root eik1jin0"}).get_text())
        draw_number.append(link.find(attrs = {'class' : "css-rqh0kk-DrawNumber e1jwcvj50"}).get_text())
        draw_date.append(link.find(name = 'h4').get_text().split('Draw')[0])

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome("A:\Software\Webdrivers\chromedriver", options=options)

idate = datetime.date.today()
text = idate.strftime('%B-%Y')

main_numbers = []
powerball = []
draw_number = []
draw_date = []

while text != 'February-2013': # As March 2013 is the last archived data for powerball
    
    driver.get('https://www.ozlotteries.com/powerball/results/'+text)
    time.sleep(1)
    source = driver.page_source
    dpage = BeautifulSoup(driver.page_source, 'lxml').find_all(attrs = {'class':"css-y693i7-Root e17om90p0"})
    get_results(dpage)
    
    idate = idate - relativedelta(months = 1)
    text = idate.strftime('%B-%Y')
  
driver.close()

# Saving the data in a dataframe
df_results = pd.DataFrame(list(zip(main_numbers, powerball, draw_number, draw_date)),
                        columns = ['main_numbers', 'powerball', 'draw_number', 'draw_date'])
df_results[['num_1', 'num_2', 'num_3', 'num_4', 'num_5', 'num_6', 'num_7']] = pd.DataFrame(df_results.main_numbers.tolist(),
                                                                                            index = df_results.index)
df_results

# Exporting data to excel file
df_results_1.to_excel('powerball-results.xlsx')