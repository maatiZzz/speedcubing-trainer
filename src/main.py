from app.main_menu.window import App
from app.logic.database.db_manager import DBManager
from app.logic.scraper.algo_scraper import AlgorithmScraper

if __name__ == '__main__':
    # s = AlgorithmScraper()
    # s.get_response()
    # s.parse_html()
    # s.scrape_alogrithms('f2l')
    # scraped_objs = s.get_scraped_obj()

    # db = DBManager()
    # db.create_table('algorithms')
    # db.insert_data('algorithms', scraped_objs)
    # db.view_data('algorithms')

    app = App()
    app.mainloop()