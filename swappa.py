import requests
from lxml import html
import os
from random import randint
from time import sleep
import pickle

try:
    with open("p.dump", "rb") as f:
        pixel_list = pickle.load(f)
except:
    pixel_list = []
try:
    with open("p2.dump", "rb") as f:
        pixel2_list = pickle.load(f)
except:
    pixel2_list = []

# The notifier function
def sendnotify(title, subtitle, message, link):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    u = '-open {!r}'.format(link)


    print('%s %s %s' %(title, subtitle, message))
    os.system('terminal-notifier {}'.format(' '.join([m, t, s, u])))

def notify(listing_dict, product):
    sendnotify(title = '%s in ' % product+ listing_dict['condition']  + ' condition - $' + str(listing_dict['price']),
               subtitle = listing_dict['storage'],
               message  = listing_dict['color'],
               link = listing_dict['link'])    

def retrieve_page():
    # Change this URL to fetch other phones
    url = 'https://swappa.com/mobile/buy/google-pixel-2/unlocked'
    page = requests.get(url)
    tree = html.fromstring(page.text)
    listings = tree.xpath('//div[@class="listing_previews"]/div')
    return listings

def retrieve_page_pixel():
    # Change this URL to fetch other phones
    url = 'https://swappa.com/mobile/buy/google-pixel/unlocked'
    page = requests.get(url)
    tree = html.fromstring(page.text)
    listings = tree.xpath('//div[@class="listing_previews"]/div')
    return listings

def listing_post_pixel(listings):
    global pixel_list
    new_pixel2s_fetched = []
    for listing in listings:
        listing_text = listing.text_content().replace('\t','').split('\n')
        listing_data = [x for x in listing_text if x.strip()]
        if len(listing_data) < 5:
            continue
        if len(listing_data) == 13:
            categories = ['seller', 'reputation', 'location', 'price', 'condition', 'unlocked', 'edition', 'color', 'storage', 'memory', 'business_seller', 'description', 'price_again', 'link']
        elif len(listing_data) == 12:
            categories = ['seller', 'reputation', 'location', 'price', 'condition', 'unlocked', 'edition', 'color', 'storage', 'memory', 'description', 'price_again', 'link']
        else:
            print(str(listing_data))
        listing_data[1] = listing_data[1].split(' ')[0]
        listing_data[3] = int(listing_data[3].strip('$'))
        listing_data[5] = listing_data[5].strip().strip('•').strip()
        listing_data[6] = listing_data[6].strip().strip('•').strip()
        listing_data[7] = listing_data[7].strip().strip('•').strip()
        listing_data[8] = listing_data[8].strip().strip('•').strip()
        listing_data[9] = listing_data[9].strip().strip('•').strip()
        listing_data += ['http://swappa.com'+listing.xpath('a')[0].get('href')]
        listing_dict = {}
        listing_dict = dict(zip(categories, listing_data))
        if not any(d[-1] == listing_dict['link'] for d in pixel_list):
            notify(listing_dict, 'Pixel')
        new_pixel2s_fetched.append(listing_data)
    pixel_list = new_pixel2s_fetched
    filename = "p.dump"
    with open(filename, "wb") as f:
        pickle.dump(pixel_list, f)

def listing_post(listings):
    global pixel_list
    global pixel2_list
    new_pixel2s_fetched = []
    categories = ['seller', 'reputation', 'location', 'price', 'condition', 'unlocked', 'edition', 'color', 'storage', 'description', 'price_again', 'link']
    for listing in listings:
        listing_text = listing.text_content().replace('\t','').split('\n')
        listing_data = [x for x in listing_text if x.strip()]
        if len(listing_data) < 5:
            continue
        listing_data[1] = listing_data[1].split(' ')[0]
        listing_data[3] = int(listing_data[3].strip('$'))
        listing_data[5] = listing_data[5].strip().strip('•').strip()
        listing_data[6] = listing_data[6].strip().strip('•').strip()
        listing_data[7] = listing_data[7].strip().strip('•').strip()
        listing_data[8] = listing_data[8].strip().strip('•').strip()
        listing_data[9] = listing_data[9].strip().strip('•').strip()
        listing_data += ['http://swappa.com'+listing.xpath('a')[0].get('href')]
        listing_dict = {}
        listing_dict = dict(zip(categories, listing_data))
        if not any(d[-1] == listing_dict['link'] for d in pixel2_list):
            notify(listing_dict, 'Pixel 2')
        new_pixel2s_fetched.append(listing_data)
    pixel2_list = new_pixel2s_fetched
    filename = "p2.dump"
    with open(filename, "wb") as f:
        pickle.dump(pixel2_list, f)

if __name__ == '__main__':
    while True:
        listings = retrieve_page()
        listing_post(listings)
        listings = retrieve_page_pixel()
        listing_post_pixel(listings)
        sleep(randint(100,200))
