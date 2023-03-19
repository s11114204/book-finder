import webbrowser

from book_resources import *
from ui import UserInterface, ConsoleUI

# installed modules:
# BeautifulSoup4
# requests


class Application:
    def __init__(self, ui: UserInterface):
        self.__ui = ui
        self.__resources = [
            ManyBooksResource(5),
            FreeComputerBooksResource(5),
            FreeEBooksResource(5)
        ]

    def start(self):
        self.__ui.show_intro()

        while True:
            book_name = self.__ui.ask_book_name()
            search_results = self.search(book_name)

            self.__ui.show_search_results(search_results)

            while True:
                result_number = self.__ui.ask_search_result_number(len(search_results))

                if result_number == 0:
                    break

                book_to_open = search_results[result_number - 1]
                webbrowser.open(book_to_open.url)

    def search(self, book_name: str) -> List[BookSearchResult]:
        results = []

        for resource in self.__resources:
            results.extend(resource.search(book_name))

        return results


app = Application(ConsoleUI())
app.start()
