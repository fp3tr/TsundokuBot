import pytest
from unittest.mock import Mock, patch
from actions.book_actions import BookHelper, ActionRecommendBook, ActionGetBookInfo, ActionGetBooksByAuthor
from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def mock_tracker():
    return Mock(spec=Tracker)

@pytest.fixture
def mock_dispatcher():
    return Mock(spec=CollectingDispatcher)

@pytest.fixture
def mock_domain():
    return {}

# ✅ Test API Call to Google Books
class TestBookHelper:
    @patch('requests.get')
    def test_make_google_books_request_success(self, mock_get):
        """Test API request successfully returns book data."""
        mock_get.return_value.json.return_value = {"items": [{"volumeInfo": {"title": "Test Book"}}]}
        mock_get.return_value.raise_for_status.return_value = None

        result = BookHelper.make_google_books_request("test query")
        assert "items" in result
        assert result["items"][0]["volumeInfo"]["title"] == "Test Book"

    @patch('requests.get')
    def test_make_google_books_request_failure(self, mock_get):
        """Test API request failure handling."""
    
    # Clear cache to ensure API call happens
        BookHelper.make_google_books_request.cache_clear()
    
        mock_get.side_effect = Exception("API Error")  # Simulating API failure
    
        result = BookHelper.make_google_books_request("test query")
        assert result == {}, f"Expected an empty dict, but got: {result}"


# ✅ Test Book Recommendation Action
class TestActionRecommendBook:
    def test_recommend_book_success(self, mock_tracker, mock_dispatcher, mock_domain):
        """Test successful book recommendations."""
        mock_tracker.get_slot.side_effect = lambda x: {"genre": "fantasy", "number": "2"}[x]
        
        action = ActionRecommendBook()
        with patch.object(BookHelper, 'make_google_books_request') as mock_request:
            mock_request.return_value = {
                "items": [
                    {"volumeInfo": {"title": "Book 1", "authors": ["Author 1"]}},
                    {"volumeInfo": {"title": "Book 2", "authors": ["Author 2"]}}
                ]
            }
            
            events = action.run(mock_dispatcher, mock_tracker, mock_domain)
            assert len(events) == 0
            assert mock_dispatcher.utter_message.called

    def test_recommend_book_no_results(self, mock_tracker, mock_dispatcher, mock_domain):
        """Test case when no book recommendations are found."""
        mock_tracker.get_slot.side_effect = lambda x: {"genre": "unknown", "number": "1"}[x]
        
        action = ActionRecommendBook()
        with patch.object(BookHelper, 'make_google_books_request') as mock_request:
            mock_request.return_value = {}
            
            events = action.run(mock_dispatcher, mock_tracker, mock_domain)
            assert len(events) == 0
            assert mock_dispatcher.utter_message.called

# ✅ Test Book Info Action
class TestActionGetBookInfo:
    def test_get_book_info_success(self, mock_tracker, mock_dispatcher, mock_domain):
        """Test getting book details successfully."""
        mock_tracker.get_slot.return_value = "1984"

        action = ActionGetBookInfo()
        with patch.object(BookHelper, 'make_google_books_request') as mock_request:
            mock_request.return_value = {
                "items": [{"volumeInfo": {"title": "1984", "authors": ["George Orwell"], "publishedDate": "1949"}}]
            }

            events = action.run(mock_dispatcher, mock_tracker, mock_domain)
            assert len(events) == 0
            assert mock_dispatcher.utter_message.called

# ✅ Test Books by Author Action
class TestActionGetBooksByAuthor:
    def test_get_books_by_author_success(self, mock_tracker, mock_dispatcher, mock_domain):
        """Test fetching books by an author successfully."""
        mock_tracker.get_slot.return_value = "Haruki Murakami"

        action = ActionGetBooksByAuthor()
        with patch.object(BookHelper, 'make_google_books_request') as mock_request:
            mock_request.return_value = {
                "items": [
                    {"volumeInfo": {"title": "Kafka on the Shore"}},
                    {"volumeInfo": {"title": "Norwegian Wood"}}
                ]
            }

            events = action.run(mock_dispatcher, mock_tracker, mock_domain)
            assert len(events) == 0
            assert mock_dispatcher.utter_message.called
