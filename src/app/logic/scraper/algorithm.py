class Algorithm:
    def __init__(self, name = '', setup = '', solution = '', category=''):
        self.name = name
        self.setup = setup
        self.solution = solution
        self.category = category

    # QUERY PREPARE
    def prepare_insert(self):
        return f"('{self.name}', '{self.setup}', '{self.solution}', '{self.category}')"

    # SETTERS
    def set_name(self, name):
        self.name = name
    
    def set_setup(self, setup):
        self.setup = setup
    
    def set_solution(self, solution):
        self.solution = solution

    def set_category(self, category):
        self.category = category

    # GETTERS
    def get_name(self):
        return self.name
    
    def get_setup(self):
        return self.setup
    
    def get_solution(self):
        return self.solution
    
    def get_category(self):
        return self.category