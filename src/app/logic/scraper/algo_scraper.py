from bs4 import BeautifulSoup
import requests
from app.logic.scraper.algorithm import Algorithm

class AlgorithmScraper:
    def __init__(self):
        self.website_url = 'https://speedcubedb.com/a/3x3/F2L'
        self.scraped_f2l_algos = []                             # list of tuples

    def get_response(self):
        self.response = requests.get(self.website_url)
        
    def parse_html(self):
        self.html_parsed = BeautifulSoup(self.response.text, 'html.parser')

    def scrape_alogrithms(self, category):
        for main_alg_div in self.html_parsed.find_all("div", class_="row singlealgorithm g-0"):
            a = Algorithm()

            # in header div: name and setup
            header_div = main_alg_div.div
            # get name
            name = header_div.find_all("a")[1].get_text(strip=True)
            a.set_name(name)
            # get setup
            setup = header_div.contents[-2].get_text(strip=True).replace("setup:", "")
            a.set_setup(setup)

            # get solution
            solution = main_alg_div.find_all("div", "formatted-alg", limit=1)[0].get_text(strip=True)
            a.set_solution(solution)

            a.set_category(category)

            self.scraped_f2l_algos.append((a.get_name(), a.get_setup(), a.get_solution(), a.get_category()))

    def get_scraped_obj(self):
        return self.scraped_f2l_algos
