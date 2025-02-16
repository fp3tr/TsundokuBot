from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from functools import lru_cache
import logging

# Set up logging
logger = logging.getLogger(__name__)

class BookHelper:
    @staticmethod
    @lru_cache(maxsize=128)
    def make_google_books_request(query: str) -> Dict[Text, Any]:
        """Fetches book data from the Google Books API."""
        try:
            response = requests.get(
                "https://www.googleapis.com/books/v1/volumes",
                params={"q": query, "maxResults": 10},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error("Timeout while accessing Google Books API")
            return {"error": "timeout", "items": []}
        except requests.exceptions.RequestException as e:
            logger.error(f"API Request failed: {str(e)}")
            return {"error": "api_error", "items": []}
        except ValueError as e:
            logger.error(f"Invalid JSON response: {str(e)}")
            return {"error": "invalid_response", "items": []}

class NumberExtractor:
    WORD_TO_NUM = {
        'a': 1, 'an': 1, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
        'couple': 2, 'few': 3, 'several': 4, 'some': 3
    }

    PLURAL_INDICATORS = ['books', 'novels', 'recommendations', 'suggestions']

    @classmethod
    def extract_number(cls, text: str, default: int = 3) -> int:
        """Extracts a number from the given text."""
        text = text.lower().strip()

        for word, num in cls.WORD_TO_NUM.items():
            if word in text.split():
                return num

        import re
        digits = re.findall(r'\b\d+\b', text)
        if digits:
            return int(digits[0])

        if any(plural in text.lower() for plural in cls.PLURAL_INDICATORS):
            return 3

        return default

class ActionRecommendBook(Action):
    def name(self) -> Text:
        return "action_recommend_book"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        genre = tracker.get_slot("genre")
        number_slot = tracker.get_slot("number")
        last_message = tracker.latest_message.get('text', '')

        # Normalize genre names
        genre_mappings = {
            "sci-fi": "science fiction",
            "graphic novel": "comics & graphic novels",
            "non-fiction": "nonfiction"
        }
        genre = genre_mappings.get(genre.lower(), genre) if genre else None

        extracted_number = NumberExtractor.extract_number(f"{number_slot} {last_message}" if number_slot else last_message)

        try:
            number = int(extracted_number)
        except ValueError:
            number = 3  # Default number of recommendations

        valid_genres = {"fantasy", "science fiction", "horror", "romance", "thriller", "mystery", "nonfiction", "action", "manga", "comics & graphic novels"}
        if not genre or genre.lower() not in valid_genres:
            dispatcher.utter_message(text="Sorry, that's not a valid genre. Please choose from: fantasy, sci-fi, horror, romance, thriller, mystery, non-fiction, action, manga, comic, or graphic novel.")
            return [SlotSet("genre", None)]

        books = BookHelper.make_google_books_request(f"subject:{genre}")

        if books.get("error"):
            dispatcher.utter_message(text="I'm having trouble accessing the book database right now. Please try again later.")
            return []

        if not books.get("items"):
            dispatcher.utter_message(text=f"I couldn't find any {genre} books. Would you like to try a different genre?")
            return []

        dispatcher.utter_message(text=f"Here are {number} {genre} book recommendations:")
        for i, book in enumerate(books.get("items", [])[:number]):
            volume_info = book.get("volumeInfo", {})
            title = volume_info.get("title", "Unknown Title")
            authors = ", ".join(volume_info.get("authors", ["Unknown Author"]))
            rating = volume_info.get("averageRating", "N/A")

            message = f"{i+1}. {title} by {authors}"
            if rating != "N/A":
                message += f" (Rating: {rating}/5)"
            dispatcher.utter_message(text=message)

        return []

class ActionGetBookInfo(Action):
    def name(self) -> Text:
        return "action_get_book_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        book_title = tracker.get_slot("book_title") or tracker.latest_message.get("text", "").strip()

        if not book_title:
            dispatcher.utter_message(text="Please specify a book title.")
            return []

        query = f'intitle:"{book_title}"&maxResults=1'
        books = BookHelper.make_google_books_request(query)

        if not books.get("items"):
            dispatcher.utter_message(text=f"Sorry, I couldn't find any information about '{book_title}'.")
            return []

        book_info = books["items"][0]["volumeInfo"]
        title = book_info.get("title", "Unknown Title")
        authors = ", ".join(book_info.get("authors", ["Unknown Author"]))
        published_date = book_info.get("publishedDate", "Unknown Date")

        dispatcher.utter_message(text=f"📖 *{title}*\n✍️ Author: {authors}\n📅 Published: {published_date}")

        return []

class ActionGetBooksByAuthor(Action):
    def name(self) -> Text:
        return "action_get_books_by_author"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        author_name = tracker.get_slot("author_name") or tracker.latest_message.get("text", "").strip()
        number_slot = tracker.get_slot("number")
        last_message = tracker.latest_message.get('text', '')

        extracted_number = NumberExtractor.extract_number(f"{number_slot} {last_message}" if number_slot else last_message)

        try:
            number = int(extracted_number)
        except ValueError:
            number = 5  # Default to 5 books if no valid number is found

        if not author_name or len(author_name.split()) < 2:
            dispatcher.utter_message(text="Please specify the full name of the author.")
            return []

        query = f'inauthor:"{author_name}"&maxResults={number}'
        books = BookHelper.make_google_books_request(query)

        if not books.get("items"):
            dispatcher.utter_message(text=f"Sorry, I couldn't find any books by {author_name}.")
            return []

        dispatcher.utter_message(text=f"Here are {number} books by {author_name}:")
        for i, book in enumerate(books.get("items", [])[:number]):
            volume_info = book.get("volumeInfo", {})
            title = volume_info.get("title", "Unknown Title")
            dispatcher.utter_message(text=f"📖 {i+1}. *{title}*")

        return []
