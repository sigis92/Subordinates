# crawler designed for the facebook group LAUSANNE à louer - bouche à oreille at https://www.facebook.com/groups/330486193693264/
# since it's way too slow to sort through the content manually
import os
import bs4
import re
import requests
from requests.compat import urljoin

"""
@funct: takes an url, stores a copy of the site locally by downloading its html and a copy of all of the resources it links to.
@param: an url
"""
def consume(url):
    print("Lausanne Eater ACTIVATED")
    mkdir(url)
    response = get_response(url)
    urls = regex_links(response)

    url = urls[0]
    print("CHECKING {}".format(url))
    regex_price(response)

    extract_content(response)

    print("It was delicious")

def regex_links(response):
    urls = []
    if response:
        cleaned = response.text
        pattern = re.compile("\/groups\/\d*?\/permalink\/.*?(?=sale_post)", re.IGNORECASE)
        matches = re.findall(pattern, cleaned)
        for match in matches:
            match = "https://www.facebook.com" + match
            urls.append(match)
        urls = list(set(urls))
        print("extracted {} links from the page".format(len(urls)))
    return urls

def regex_price(response):
    price = 0
    if response:
        cleaned = response.text
        print(response.text)
        

def extract_content(response):
    if response:
        soup = bs4.BeautifulSoup(response.content, 'html5lib')
        print("Page title is:\n{}".format(soup.title.string))
        #a = soup.find_all('div', class_= "_3ccb")
        a = soup.find_all('div', attrs = {
            'class': '_lm7'})

# beginning navigation:



"""
@funct: creates a folder to contain all the content consumed and moves the execution process into that folder
@param: an url
"""
def mkdir(url):
    directory = "./" + url.split('/')[-1]
    try:
        os.makedirs(directory)
        print("Directory created")
    except Exception as exc:
        print("Notification: %s" %(exc))

    os.chdir(directory)


""" 
@funct: creates a local copy of the content existing at the specified url
@param: an URL
@retur: a response object
"""
def get_response(url):
    try:
        response = requests.get(url)
        return response
    except Exception as exc:
        print("Notification: %s" %(exc))



"""
@funct: stores a local copy of the content found in the response object
@param: a response object
"""
def clone_content(response):
    if response:
        url = response.url
        if url[-1] == '/':
            url = url[:-1]
        filename = url.split('/')[-1] 
        if 'text/html' in response.headers['content-type']:
            filename = filename + '.html'
        try:
            copy = open(filename, 'wb+')
            for chunk in response.iter_content(1024):
                copy.write(chunk)
            copy.close()
            print("downloaded " + filename)
        except Exception as exc:
            print("Notification: %s" %(exc))



"""
@funct: checks if the object is html/text. If it is, it returns all urls found in it
@param: a response object
@retur: a list of urls
"""
def extract_urls(response):
    urls = []
    if response:
        if 'text/html' in response.headers['content-type']:
            soup = bs4.BeautifulSoup(response.content, 'html5lib')
            links = soup.findAll('a')
            for link in links:
                link = link.get('href')
                link = urljoin(response.url, link) # Makes relative urls absolute
                urls.append(link)
            #In case of duplicates, remove them
            urls = set(urls)
            print("Found {} links".format(len(urls)))
    return urls



consume('https://www.facebook.com/groups/330486193693264')