import sqlite3
from app.logic.scraper.algo_scraper import AlgorithmScraper

class DBManager:
    def __init__(self):
        self.con = sqlite3.connect('rubik.db')
        self.cur = self.con.cursor()
    
    def create_table(self, name):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {name}(name, setup, solution, category)")

    def insert_data(self, name, obj_arr):
        self.cur.executemany(f"INSERT INTO {name} VALUES (?, ?, ?, ?)", obj_arr)

    def check_if_empty(self, name):
        res = self.cur.execute(f"SELECT * FROM {name}")
        return len(res.fetchall()) == 0

    def view_data(self, name):
        res = self.cur.execute(f"SELECT setup FROM {name}")
        return res.fetchone()[0]