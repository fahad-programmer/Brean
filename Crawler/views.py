import random
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import WebPages, Images
from django.views.generic import ListView
import logging


#Logging basic file configuration
logging.basicConfig(filename='app.log', filemode='a', format="%(process)d-%(levelname)s-%(message)s")




class Viper(ListView):

    #Header for the request module to keep us from blocking from the sites

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    current_url = 'https://www.nytimes.com/international/'
    
    waiting_urls = []

    def __init__(self) -> None:
        self.engine()

    def parser(self) -> None:

        """
        Getting the data from the page that is required
            1 -> Title
            2 - > Meta Desciption
            3 - > keywords
        """

        global soup
        page = requests.get(self.current_url, headers=self.headers)
        soup = BeautifulSoup(page.content, "lxml")

        #Now getting the desired thing from the page
        try:
            global title, meta_description, keyword
            title = soup.find("meta", property="og:title")
            meta_description = soup.find("meta", attrs={'name':'description'})
            keyword = soup.find("meta", attrs={'name':'keywords'})

            if title == None:
                title = "No title is given on the page"
            else:
                title = title["content"]

            if meta_description == None:
                meta_description == "No meta description given for the page"
            else:
                meta_description = meta_description["content"]
            
            if keyword == None:
                keyword = "No keywords given on the page"
            else:
                keyword = keyword["content"]
            
        except Exception as e:
            logging.error(f"Error in finding the data on the web page {self.current_url}")

        self.getting_links()

    def add_to_database(self) -> None:
        try:
            main_obj = WebPages(title=title, meta_description=meta_description, keywords=keyword, url=self.current_url)
            main_obj.save()
        except Exception as e:
            logging.error("Error occured while putting the values in the database")
        

    def getting_links(self) -> None:
        try:
            for link in soup.findAll('a'):
                if 'http' in link.get('href'):
                    self.waiting_urls.append(link.get('href'))
                else:
                    self.waiting_urls.append(f"{self.current_url}{link.get('href')}")
        except Exception as e:
            logging.error("some error found while getting the links in webpage crawler")     
        
    def queue_manager(self) -> None:
        #changing the current url
        #chossing different urls to crawl from the list
        self.current_url = self.waiting_urls[random.choice(range(2, len(self.waiting_urls)))]
        #removing the element from the list
        self.waiting_urls.remove(self.current_url)

    def engine(self) -> None:
        #The main engine method that will start the crawler
        while True:
            print(self.current_url)
            self.parser()
            self.add_to_database()
            self.queue_manager()
            

    def __repr__(self) -> str:
        return f"The title is {title} with meta description is {meta_description} \n with the {keyword}"



class ViperImage(ListView):
    #Header for the request module to keep us from blocking from the sites

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    current_url = 'https://python.plainenglish.io/how-to-scrape-images-using-beautifulsoup4-in-python-e7a4ddb904b8'
    
    waiting_urls = []

    def __init__(self) -> None:
        self.engine()

    def parser(self) -> None:
        """Getting the image from the page"""
        global soup
        page = requests.get(self.current_url, headers=self.headers)
        soup = BeautifulSoup(page.content, "lxml")

        #Now getting the desired thing from the page
        try:
            #first getting all the images
            images = soup.find_all('img')
            print(f"there are {len(images)} on the page")
            for image in images:
                url = image.get("src")
                if "http" in url:
                    pass
                else:
                    url = f"{self.current_url}{url}"
                alt_text = image.get("alt")
                self.add_to_database(alt_text=alt_text, url=url)
      
        except Exception as e:
            logging.error(f"error in finding the image on the page")

        self.getting_links()

    @staticmethod
    def add_to_database(alt_text, url) -> None:
        try:
            main_obj = Images(alt_text=alt_text, url=url)
            main_obj.save()
        except Exception as e:
            logging.error("Some Error occcured while putting values in database")

    def getting_links(self) -> None:
        try:
            for link in soup.find_all('a'):
                if 'http' in link.get('href'):
                    self.waiting_urls.append(link.get('href'))
                else:
                    self.waiting_urls.append(f"{self.current_url}{link.get('href')}")
        except Exception as e:
            logging.error("some error found while getting link on the image crawler")

    def queue_manager(self) -> None:
        #changing the current url
        #chossing different urls to crawl from the list
        self.current_url = self.waiting_urls[random.choice(range(2, len(self.waiting_urls)))]
        #removing the element from the list
        self.waiting_urls.remove(self.current_url)

    def engine(self) -> None:
        #The main engine method that will start the crawler
        while True:
            print(self.current_url)
            self.parser()
            self.queue_manager()

    def __repr__(self) -> str:
        return f"The image alt is good"