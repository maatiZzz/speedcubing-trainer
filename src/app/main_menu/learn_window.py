import customtkinter as ctk
from app.logic.database.db_manager import DBManager
from app.logic.scraper.algo_scraper import AlgorithmScraper

class LearnWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.title = "Learn"

        self.grid_columnconfigure((0), weight = 1)
        self.grid_rowconfigure((0, 1), weight = 1)

        # DATABASE
        self.__init_db()

        # LIST FRAME
        self.__init_label_frame()
        self.__init_list_frame()

    def __init_db(self):
        self.db_manager = DBManager()
        # init table
        self.db_manager.create_table('algorithms')
        if self.db_manager.check_if_empty('algorithms'):
            # scrape objs only if algorithms table is empty
            self.__init_scraper()
            scraped_obj_arr = self.scraper.get_scraped_obj()
            self.db_manager.insert_data('algorithms', scraped_obj_arr)

    def __init_scraper(self):
        self.scraper = AlgorithmScraper()

        self.scraper.get_response()
        self.scraper.parse_html()
        self.scraper.scrape_alogrithms('f2l')

    def __init_label_frame(self):
        self.label_frame = ctk.CTkFrame(self)
        self.label_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        self.label_frame.grid_columnconfigure((0), weight=1)

        self.text = ctk.CTkLabel(self.label_frame, text="Pick algorithm to learn: ",  font=('Arial', 22))
        self.text.grid(row = 0, column=0, padx = 20, pady = 20, sticky = "ew")

    def __init_list_frame(self):
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")
        self.list_frame.grid_columnconfigure((0,1), weight=1)

        self.__init_alg_list()

    # def __init_alg_list(self):


