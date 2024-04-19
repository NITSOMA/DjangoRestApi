from bs4 import BeautifulSoup
import requests
import random

home_url = 'http://127.0.0.1:8000/api/books/'
headers = {"user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}


def get_id(url):
    """
    Function takes one parameter url: str
    Uses for loop to capture book_id-first appearance group of numbers
    once numeric chars ends loop must brake and don't collect other numerics chars
    """
    num = 0
    book_id = ""
    for i in url:
        if num == 1 and not i.isnumeric():
            break
        if i.isnumeric():
            num = 1
            book_id += i
    return book_id


def collect_data(url):
    """
    Function collects data from target webpage (function gets  parameter url: str)
    Function uses requests and beautifulsoup for get data and parse it
    Returns dict full of desired data
    """
    books = {}
    book_id = get_id(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("h1", {"class": "Text Text__title1"})
    author = soup.find("span", {"class": "ContributorLink__name"})
    rating = soup.find("div", {"class": "RatingStatistics__rating"})
    total_voters = soup.find("div", {"class": "RatingStatistics__meta"})
    books['title'] = title.get_text()
    books['author'] = author.get_text()
    books['rating'] = float(rating.get_text())
    books['total_voters'] = int(total_voters.get_text().split()[0].replace(',', ''))
    books['book_id'] = book_id
    return books


def add_requested_data(url):
    """
    Function is responsible for reach api
    Check existing data and update or post data
    has one param: url: str
    returns new_url: str
    """
    books = collect_data(url)
    book_id = books['book_id']
    response = requests.get(f'{home_url}{book_id}/')
    if response.status_code == 404:
        requests.post(home_url, data=books)
    elif response.status_code == 200:
        requests.put(f'{home_url}{book_id}/', data=books)
    return f'{home_url}{book_id}/'


def scheduled_add_data():
    """
    Function is responsible to collect data from target website
    anytime you call function its generate random number
    which helps us to collect data randomly
    reach api and updates or post data

    """
    url = 'https://www.goodreads.com/book/show/'
    book_url = url + str(random.randint(1, 80000))
    data_to_add = collect_data(book_url)
    book_id = data_to_add['book_id']
    get_url = f'{home_url}{book_id}/'
    response = requests.get(get_url)
    if response.status_code == 404:
        requests.post(home_url, data=data_to_add)
    elif response.status_code == 200:
        requests.put(get_url, data=data_to_add)
