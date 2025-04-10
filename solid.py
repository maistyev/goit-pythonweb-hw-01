from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Book:
    """Клас для представлення книги."""

    def __init__(self, title: str, author: str, year: str) -> None:
        self.title: str = title
        self.author: str = author
        self.year: str = year

    def __str__(self) -> str:
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}"


class BookRepository(ABC):
    """Інтерфейс для роботи з репозиторієм книг."""

    @abstractmethod
    def add(self, book: Book) -> None:
        """Додати книгу до репозиторію."""
        pass

    @abstractmethod
    def remove(self, title: str) -> bool:
        """Видалити книгу з репозиторію за назвою."""
        pass

    @abstractmethod
    def get_all(self) -> List[Book]:
        """Отримати всі книги з репозиторію."""
        pass


class LibraryInterface(ABC):
    """Інтерфейс для роботи з бібліотекою."""

    @abstractmethod
    def add_book(self, title: str, author: str, year: str) -> None:
        """Додати книгу до бібліотеки."""
        pass

    @abstractmethod
    def remove_book(self, title: str) -> bool:
        """Видалити книгу з бібліотеки за назвою."""
        pass

    @abstractmethod
    def get_all_books(self) -> List[Book]:
        """Отримати всі книги з бібліотеки."""
        pass


class InMemoryBookRepository(BookRepository):
    """Реалізація репозиторію книг в пам'яті."""

    def __init__(self) -> None:
        self.books: List[Book] = []

    def add(self, book: Book) -> None:
        """Додати книгу до репозиторію."""
        self.books.append(book)

    def remove(self, title: str) -> bool:
        """Видалити книгу з репозиторію за назвою."""
        for i, book in enumerate(self.books):
            if book.title == title:
                self.books.pop(i)
                return True
        return False

    def get_all(self) -> List[Book]:
        """Отримати всі книги з репозиторію."""
        return self.books


class Library(LibraryInterface):
    """Реалізація бібліотеки."""

    def __init__(self, repository: BookRepository) -> None:
        self.repository: BookRepository = repository

    def add_book(self, title: str, author: str, year: str) -> None:
        """Додати книгу до бібліотеки."""
        book = Book(title, author, year)
        self.repository.add(book)
        logger.info(f"Book added: {book}")

    def remove_book(self, title: str) -> bool:
        """Видалити книгу з бібліотеки за назвою."""
        result = self.repository.remove(title)
        if result:
            logger.info(f"Book removed: {title}")
        else:
            logger.info(f"Book not found: {title}")
        return result

    def get_all_books(self) -> List[Book]:
        """Отримати всі книги з бібліотеки."""
        return self.repository.get_all()


class BookDisplayer:
    """Клас для відображення книг."""

    def display_books(self, books: List[Book]) -> None:
        """Відобразити список книг."""
        if not books:
            logger.info("No books in the library.")
            return

        for book in books:
            logger.info(str(book))


class LibraryManager:
    """Клас для управління бібліотекою."""

    def __init__(self, library: LibraryInterface, displayer: BookDisplayer) -> None:
        self.library: LibraryInterface = library
        self.displayer: BookDisplayer = displayer

    def add_book(self, title: str, author: str, year: str) -> None:
        """Додати книгу до бібліотеки."""
        self.library.add_book(title, author, year)

    def remove_book(self, title: str) -> None:
        """Видалити книгу з бібліотеки за назвою."""
        self.library.remove_book(title)

    def show_books(self) -> None:
        """Показати всі книги в бібліотеці."""
        books = self.library.get_all_books()
        self.displayer.display_books(books)


class ConsoleInputHandler:
    """Клас для обробки введення користувача через консоль."""

    def get_command(self) -> str:
        """Отримати команду від користувача."""
        return input("Enter command (add, remove, show, exit): ").strip().lower()

    def get_book_details(self) -> Dict[str, str]:
        """Отримати деталі книги від користувача."""
        title = input("Enter book title: ").strip()
        author = input("Enter book author: ").strip()
        year = input("Enter book year: ").strip()
        return {"title": title, "author": author, "year": year}

    def get_book_title(self) -> str:
        """Отримати назву книги від користувача."""
        return input("Enter book title to remove: ").strip()


def main() -> None:
    repository = InMemoryBookRepository()
    library = Library(repository)
    displayer = BookDisplayer()
    manager = LibraryManager(library, displayer)
    input_handler = ConsoleInputHandler()

    while True:
        command = input_handler.get_command()

        match command:
            case "add":
                book_details = input_handler.get_book_details()
                manager.add_book(
                    book_details["title"], book_details["author"], book_details["year"]
                )
            case "remove":
                title = input_handler.get_book_title()
                manager.remove_book(title)
            case "show":
                manager.show_books()
            case "exit":
                logger.info("Exiting program...")
                break
            case _:
                logger.info("Invalid command. Please try again.")


if __name__ == "__main__":
    main()