import re

import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from django.shortcuts import render
from .models import Search

# created a variable called BASIC_CRAIGSLIST_URL to get the url that we will be scrapping with beautiful soup
BASIC_CRAIGSLIST_URL = 'https://www.buyadog.com.ng/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'


def home(request):
    return render(request, 'blog/base.html')


def new_search(request):
    # created a variable search that will get the search text from the form
    search = request.POST.get('search')
    # we created the search text and store it up in our data base
    Search.objects.create(search=search)
    max_price = request.POST.get('max_price', 1000)
    # concatenating the URL created earlier with the search text that the user enters
    final_url = BASIC_CRAIGSLIST_URL.format(quote_plus(search))

    # Getting the webpage, creating a Response object
    response = requests.get(final_url)
    # Extracting the source code of the page
    data = response.text
    # passing the source code to Beautiful Soup to create a BeautifulSoup object for it
    soup = BeautifulSoup(data, features='html.parser')
    # Extracting all the <a> tags whose class name is 'result-row' into a list.
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        # Get the title of what the user is searching for
        post_title = post.find(class_='result-title').text
        # Get the url of what the user is searching for
        post_url = post.find('a').get('href')

        # check whether the text search have a price and get the price
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text

        # if there is no price existing for the search text create a new one
        else:
            new_response = requests.get(post_url)
            new_data = new_response.text
            new_soup = BeautifulSoup(new_data, features='html.parser')
            post_text = new_soup.find(id='postingbody').text

            r1 = re.findall(r'\s\w+', post_text)
            if r1:
                post_price = r1[0]
            else:
                post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
        }

    return render(request, 'blog/new_search.html', context=stuff_for_frontend)
