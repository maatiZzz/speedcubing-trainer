import sqlite3
from app.logic.scraper.algo_scraper import AlgorithmScraper

class DBManager:
    def __init__(self):
        self.con = sqlite3.connect('rubik.db')
        self.cur = self.con.cursor()
    
    def create_table(self, table_name):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name}(name, setup, solution, category)")

    def insert_data(self, table_name, obj_arr):
        self.cur.executemany(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?)", obj_arr)
        
    def commit_changes(self):
        self.con.commit()

    def check_if_empty(self, table_name):
        res = self.cur.execute(f"SELECT * FROM {table_name}")
        return len(res.fetchall()) == 0
    
    def get_all_alg_data(self, table_name):
        res = self.cur.execute(f"SELECT * FROM {table_name}")
        return res.fetchall()

    def view_data(self, table_name):
        res = self.cur.execute(f"SELECT * FROM {name}")
        return res.fetchone()[0]