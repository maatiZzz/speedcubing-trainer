import requests
from bs4 import BeautifulSoup

class AlgorithmScraper:
    """Scrapes F2L algorithms from SpeedCubeDB with timeout."""

    DEFAULT_URL: str = "https://speedcubedb.com/a/3x3/F2L"
    TIMEOUT_SECONDS: float = 10.0

    def __init__(self, website_url: str = DEFAULT_URL) -> None:
        self.website_url: str = website_url
        self.response_text: str = ""
        self.html_parsed: BeautifulSoup | None = None
        self.scraped_algos: list[tuple[str, str, str, str]] = []

    def get_response(self) -> None:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) RubiksCubeScrambler/0.1"
        }
        response = requests.get(
            self.website_url, headers=headers, timeout=self.TIMEOUT_SECONDS
        )
        response.raise_for_status()
        self.response_text = response.text

    def parse_html(self) -> None:
        self.html_parsed = BeautifulSoup(self.response_text, "html.parser")

    def scrape_algorithms(self, category: str = "F2L") -> None:
        if self.html_parsed is None:
            return

        for main_alg_div in self.html_parsed.find_all(
            "div", class_="row singlealgorithm g-0"
        ):
            header_div = main_alg_div.div
            if header_div is None:
                continue

            links = header_div.find_all("a")
            if len(links) < 2:
                continue
            name = links[1].get_text(strip=True)

            if len(header_div.contents) < 2:
                continue
            setup = (
                header_div.contents[-2]
                .get_text(strip=True)
                .replace("setup:", "")
                .strip()
            )

            formatted_divs = main_alg_div.find_all("div", "formatted-alg", limit=1)
            if not formatted_divs:
                continue
            solution = formatted_divs[0].get_text(strip=True)

            self.scraped_algos.append((name, setup, solution, category))

    def get_scraped_obj(self) -> list[tuple[str, str, str, str]]:
        return list(self.scraped_algos)
