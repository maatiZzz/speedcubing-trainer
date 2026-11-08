from dataclasses import dataclass

"""
    Algorithm specification class:
    
    Attributes:
        name: name of algorithm (f.e. F2L 5)
        setup: sequence allowing to start algorithm animation ("R U R' U2' R U' R' U")
        solution: sequence solving sub-problem, setup inversion ("U' R U R' U2 R U' R'")
        category: algorithm category (f.e. F2L, OLL)
    """

@dataclass(frozen=True)
class Algorithm:
    name: str
    setup: str
    solution: str
    category: str

    def to_tuple(self) -> tuple[str, str, str, str]:
        return (self.name, self.setup, self.solution, self.category)
