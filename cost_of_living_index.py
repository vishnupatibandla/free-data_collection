import urllib2
from bs4 import BeautifulSoup
import csv
import re
import time

with open('living_index.csv', 'wb') as csvfile:
    headers = ['zipcode', 'city_state', 'cost']
    writer = csv.writer(csvfile)

    with open('zipcode_list') as zipcode:
        for zip in zipcode:

            site = "http://www.city-data.com/zips/" + str(zip).strip('\n') + ".html"
            # print "Writing data for Area Code {}".format(zip)
            hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            request = urllib2.Request(site, headers=hdr)

            try:
                page = urllib2.urlopen(request)
            except urllib2.HTTPError, e:
                #print e.fp.read()
                continue

            soup = BeautifulSoup(page, 'html.parser')
            living_index_city = soup.find_all('h1', attrs={"class": "city"}).__str__()
            living_index_city_data = re.match("(.*)(Zip Code \()(.*)(\) Detailed Profile).*", living_index_city)
            living_index = soup.find_all('div', attrs={"class": "row"}).__str__()
            small_data = living_index[400:1200]
            data = re.match("(.*)(cost of living index in zip code )[0-9]{5}(:<\/b> )(.*?)( <b>).*", small_data)
            if data.group() is None:
                continue
            else:
                print ("Cost of living index for zipcode: " + str(zip).strip('\n') + ": " + data.group(4))
                writer.writerow((zip.strip('\n'), living_index_city_data.group(3), data.group(4)))
            time.sleep(2)
            csvfile.flush()
