import os
import json


class Book:
    """Класс, представляющий книгу в библиотеке."""

    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self) -> str:
        """Возвращает строковое представление книги."""
        return (f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}, "
                f"Year: {self.year}, Status: {self.status}")

    def to_dict(self) -> dict:
        """Конвертирует объект книги в словарь."""
        return {
            "id": self.book_id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict):
        """Создает объект книги из словаря."""
        return Book(
            data["id"],
            data["title"],
            data["author"],
            data["year"],
            data["status"]
        )


class Library:
    """Класс для управления библиотекой книг с сохранением в JSON файл."""

    FILE_PATH = "library.json"

    def __init__(self):
        self.books = []
        self.current_id = 1
        self.load_books()

    def load_books(self) -> None:
        """Загружает книги из JSON файла."""
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    for book_data in data:
                        book = Book.from_dict(book_data)
                        self.books.append(book)
                        self.current_id = max(self.current_id, book.book_id + 1)
                except json.JSONDecodeError:
                    print("Ошибка чтения файла. В библиотеке нет доступных книг.")

    def save_books(self) -> None:
        """Сохраняет книги в JSON файл."""
        with open(self.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, indent=2, ensure_ascii=False)

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет новую книгу в библиотеку."""
        book = Book(self.current_id, title, author, year)
        self.books.append(book)
        self.current_id += 1
        self.save_books()
        print(f"Книга '{title}' добавлена с ID {book.book_id}.")

    def remove_book(self, book_id: int) -> None:
        """Удаляет книгу из библиотеки."""
        book_to_remove = next((book for book in self.books if book.book_id == book_id), None)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            print(f"Книга с ID {book_id} удалена.")
        else:
            print(f"Ошибка: Книга с ID {book_id} не найдена.")

    def search_books(self, key: str, value: str) -> None:
        """Ищет книги по указанному ключу."""
        if key not in ["title", "author", "year", "status"]:
            print("Ошибка: Неверный ключ поиска.")
            return
        results = [book for book in self.books if str(getattr(book, key, "")).lower() == value.lower()]
        if results:
            print("Найденные книги:")
            for book in results:
                print(book)
        else:
            print("Книги не найдены.")

    def display_books(self) -> None:
        """Отображает список всех книг в библиотеке."""
        if self.books:
            print("Список всех книг:")
            for book in self.books:
                print(book)
        else:
            print("Библиотека пуста.")

    def update_status(self, book_id: int, new_status: str) -> None:
        """Обновляет статус книги."""
        book_to_update = next((book for book in self.books if book.book_id == book_id), None)
        if book_to_update:
            book_to_update.status = new_status
            self.save_books()
            print(f"Статус книги '{book_to_update.title}' обновлен на '{new_status}'.")
        else:
            print(f"Ошибка: Книга с ID {book_id} не найдена.")


if __name__ == "__main__":
    library = Library()

    while True:
        print("\n1. Добавить книгу\n2. Удалить книгу\n3. Искать книгу\n4. Показать все книги\n5. Изменить статус книги\n6. Выйти")
        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания книги: "))
                library.add_book(title, author, year)
            elif choice == "2":
                book_id = int(input("Введите ID книги для удаления: "))
                library.remove_book(book_id)
            elif choice == "3":
                key = input("Искать по (title, author, year, status): ").lower()
                value = input("Введите значение для поиска: ")
                library.search_books(key, value)
            elif choice == "4":
                library.display_books()
            elif choice == "5":
                book_id = int(input("Введите ID книги для изменения статуса: "))
                new_status = input("Введите новый статус книги: ")
                library.update_status(book_id, new_status)
            elif choice == "6":
                print("Выход из программы.")
                break
            else:
                print("Ошибка: Неверный выбор.")
        except ValueError:
            print("Ошибка ввода. Убедитесь, что данные корректны.")
