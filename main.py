import webbrowser

from book_resources import *
from ui import UserInterface, ConsoleUI

# installed modules:
# BeautifulSoup4
# requests


class Application:
    def __init__(self, ui: UserInterface):
        search_results_limit = 5

        self.__ui = ui
        self.__resources: List[BookResource] = [
            ManyBooksResource(search_results_limit),
            # FreeComputerBooksResource(search_results_limit),
            FreeEBooksResource(search_results_limit)
        ]
        self.strict_mode = False

        self.__ui.hooks['on_strict_mode_enabled'] = self.enable_strict_mode
        self.__ui.hooks['on_strict_mode_disabled'] = self.disable_strict_mode

    def enable_strict_mode(self):
        self.strict_mode = True

    def disable_strict_mode(self):
        self.strict_mode = False

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
            search_results = resource.search(book_name, self.strict_mode)
            results.extend(search_results)

        return results


app = Application(ConsoleUI())
app.start()
