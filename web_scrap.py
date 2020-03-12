import urllib.request
from bs4 import BeautifulSoup
import logging
import os
import sys

def get_path():

    path = input('Please enter the path where you want to download data or enter "No" to exit: ')
	
    if path.upper() == 'NO':
        sys.exit(0)
		
    while path.upper() != 'NO':

        try:
            os.chdir(path)
            print('Data files will be placed in ', path)
            break
        except FileNotFoundError:
            path = input('Enter the valid path or enter "NO" to exit: ')
        except:
            print('Have come across unhandled exception, hence exiting')
            sys.exit(0)

    return path

def get_sector_data():

    sectors = dict()
    company_code_mapping = dict()
    sectorwise_com = dict()

    soup = BeautifulSoup(urllib.request.urlopen(r'http://www.moneycontrol.com/stocks/sectors'))

    parser = soup.find_all( 'ul', class_='sec_comp_nm')[2].find_all('li')

    for i in parser:
        sectors[i.text] = str(i).lstrip('<li><a href=').rstrip('</a></li>').split('>')[0].replace('"', '')

    for key, value in sectors.items():
        print('Generating the data for', key, 'sector')
        soup = BeautifulSoup(urllib.request.urlopen(sectors[key]))
        parser = BeautifulSoup(str(soup.find_all( class_='pricePertable')))
        company_codes = parser.find_all('td', class_='left')
        companies = []
		
        for i in company_codes:
            company_code_mapping[i.text] =  str(i).lstrip('<td class="left"><a href=').split('>')[0].split('/')[-1].replace('"', '')
            companies.append(i.text)
        else:
            sectorwise_com[key] = companies

    return sectorwise_com, company_code_mapping			

def get_stock_data(sectorwise_com, company_code_mapping, path):

    for key, value in sectorwise_com.items():
        if value:
            for each_com in value:
                code = company_code_mapping.get(each_com)
                print('Generating the data for {}'.format(each_com))
                ip_ad = 'https://www.moneycontrol.com/tech_charts/nse/his/' + code.lower() + '.csv'
                try:
                    data_file = urllib.request.urlopen(ip_ad)
                except:
                    print("=============================================" + each_com)

                if not os.path.exists(os.path.join(path, key)):
                    os.makedirs(os.path.join(path, key))
			
                    line = data_file.readline()
	
                    while line:
                        with open(os.path.join(path, key, each_com + '.csv'	), 'ab') as file:
                            file.write(line)
                            line = data_file.readline()

						
if __name__ == '__main__':
        path = get_path()
        sectorwise_com, company_code_mapping = get_sector_data()
        get_stock_data(sectorwise_com, company_code_mapping, path)	
