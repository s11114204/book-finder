from typing import List

from book_resources import BookSearchResult


class Texts:
    def __init__(self):
        self.app_name = "book-searcher 3000"
        self.exit = "Exiting book-searcher 3000"

        self.ask_book_name = "Enter book name you want to search: "
        self.found_results_text = "Found results:"
        self.ask_search_result_number = "You can enter result number to open it in browser, or enter \'stop\' or 0 to search again: "
        self.ask_search_result_number_again = "You entered wrong number. Enter it again: "


texts = Texts()


class UserInterface:
    def __init__(self):
        self._texts = texts

    def show_intro(self):
        raise NotImplementedError()

    def ask_book_name(self):
        raise NotImplementedError()

    def show_search_results(self, results: List):
        raise NotImplementedError()

    def ask_search_result_number(self, search_results_length: int):
        raise NotImplementedError()


def handle_commands(func):
    def wrapper(*args, **kwargs):
        user_input = func(*args, **kwargs)

        if user_input == 'exit':
            print(texts.exit)
            exit()

        return user_input

    return wrapper


class ConsoleUI(UserInterface):
    def show_intro(self):
        wrapper_text = "[==============================]"

        print(f"{wrapper_text}\n[===== {self._texts.app_name} =====]\n{wrapper_text}")

    @handle_commands
    def ask_book_name(self):
        print()
        return input(self._texts.ask_book_name)

    def show_search_results(self, results: List[BookSearchResult]):
        print()
        print(self._texts.found_results_text)

        order_number = 1
        for book in results:
            if book.is_error_occurred:
                print(f"{order_number}) Unsuccessful search - {book.resource_name} ({book.url}) - {book.description}")
            else:
                print(f"{order_number}) {book.name} - {book.resource_name} ({book.url})")

            order_number += 1

        print()

    @handle_commands
    def __ask_search_result_number_core(self, is_first_time: bool) -> str:
        text = self._texts.ask_search_result_number if is_first_time else self._texts.ask_search_result_number_again
        user_input = input(text)

        if user_input == 'stop':
            return '0'

        return user_input

    def ask_search_result_number(self, search_results_length: int) -> int:
        is_first_time = True
        result_number = 0

        while True:
            try:
                result_number = int(self.__ask_search_result_number_core(is_first_time))

                if search_results_length >= result_number >= 0:
                    break
            except ValueError:
                pass
            finally:
                is_first_time = False

        return result_number
