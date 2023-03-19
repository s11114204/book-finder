import json
from typing import List

from bs4 import BeautifulSoup

import requests
from requests import Response


def apply_strict_mode(func):
    def wrapper(book_name: str, strict_mode: bool):
        func(book_name, strict_mode)

    return wrapper


class BookSearchResult:
    def __init__(self, resource_name, url, name, description="", is_error_occurred=False):
        self.resource_name = resource_name
        self.url = url
        self.name = name
        self.description = description
        self.is_error_occurred = is_error_occurred


class BookResource:
    def __init__(self, resource_name: str, resource_url: str, results_limit: int):
        self._resource_name = resource_name
        self._resource_url = resource_url
        self.results_limit = results_limit

    def search(self, book_name: str, strict_mode: bool = False) -> List[BookSearchResult]:
        search_url = self._get_search_url(book_name)

        response = requests.get(search_url)

        if response.status_code != 200:
            return [BookSearchResult(self._resource_name, search_url, book_name, "Status code is not 200", True)]

        return self._parse_search_response(response, strict_mode)

    def _get_search_url(self, book_name: str) -> str:
        raise NotImplementedError()

    def _parse_search_response(self, response: Response, strict_mode: bool) -> List[BookSearchResult]:
        raise NotImplementedError()


class ManyBooksResource(BookResource):
    def __init__(self, results_limit):
        super().__init__("ManyBooks", "https://manybooks.net", results_limit)

    def _get_search_url(self, book_name: str) -> str:
        return f"{self._resource_url}/search-book?search={book_name}"

    def _parse_search_response(self, response: Response, strict_mode: bool) -> List[BookSearchResult]:
        html = BeautifulSoup(response.text, features="html.parser")
        results = []

        for book_link in html.select('.book .content .field--name-field-cover a', limit=self.results_limit):
            book = BookSearchResult(
                resource_name=self._resource_name,
                url=self._resource_url+book_link.get('href'),
                name=book_link.find('img').get('alt')
            )

            results.append(book)

        return results


class FreeComputerBooksResource(BookResource):
    def __init__(self, results_limit):
        super().__init__("FreeComputerBooks", "https://freecomputerbooks.com", results_limit)

    def _get_search_url(self, book_name: str) -> str:
        return f'https://cse.google.com/cse/element/v1?q={book_name}&rsz=filtered_cse&num=10&hl=en&source=gcsc&gss' \
               f'=.com&cselibv=c23214b953e32f29&cx=partner-pub-5976068913745703:4325807428&safe=active&cse_tok' \
               f'=ALwrddHhTrimgEEonPI0B3fcxsng:1679227582537&exp=csqr,cc&callback=google.search.cse.api1208'

    def _parse_search_response(self, response, strict_mode: bool) -> List[BookSearchResult]:
        plain = response.text[response.text.find('{'):response.text.rfind('}')+1]
        parsed = json.loads(plain)

        results = []

        for result in parsed['results']:
            book = BookSearchResult(
                resource_name=self._resource_name,
                url=result['url'],
                name=result['titleNoFormatting'],
                description=result['contentNoFormatting']
            )

            results.append(book)

            if len(results) == self.results_limit:
                break

        return results


class FreeEBooksResource(BookResource):
    def __init__(self, results_limit):
        super().__init__("FreeEBooks", "https://www.free-ebooks.net", results_limit)

    def _get_search_url(self, book_name: str) -> str:
        return f"{self._resource_url}/search/{book_name.replace(' ', '+')}"

    def _parse_search_response(self, response: Response, strict_mode: bool) -> List[BookSearchResult]:
        html = BeautifulSoup(response.text, features="html.parser")
        results = []

        for result_row in html.select('.mt80 .laText.row', limit=self.results_limit):
            book_link = result_row.select_one('a.title')
            description_paragraph = result_row.select_one('p.book-description')

            book = BookSearchResult(
                resource_name=self._resource_name,
                url=self._resource_url+book_link.get('href'),
                name=book_link.text,
                description=description_paragraph.text
            )

            results.append(book)

        return results
