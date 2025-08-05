import pytest
from main import BooksCollector
class TestBooksCollector:
    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2
# Проверка: нельзя добавить книгу с некорректной длиной названия
@pytest.mark.parametrize('name', ['', 'a'*41])
def test_add_new_book_invalid_length(collector, name):
    
    collector.add_new_book(name)
    assert name not in collector.get_books_genre()
# Проверка: нельзя добавить дублирующую книгу

def test_add_new_book_duplicate(collector):
    collector.add_new_book('Война и Мир')
    collector.add_new_book('Война и Мир')
    assert list(collector.get_books_genre().keys()).count('Война и Мир') == 1

# Проверка: успешное добавление жанра к книге

def test_set_book_genre_success(collector):
    collector.add_new_book('Шерлок Холмс')
    collector.set_book_genre('Шерлок Холмс', 'Детективы')
    assert collector.get_book_genre('Шерлок Холмс') == 'Детективы'

# Проверка: нельзя установить жанр несуществующей книге
def test_set_book_genre_invalid_book(collector):
    collector.set_book_genre('Несуществующая книга', 'Комедии')
    assert 'Несуществующая книга' not in collector.get_books_genre()

# Проверка: получение жанра для неизвестной книги возвращает None
def test_get_book_genre_returns_none_for_unknown(collector):
    assert collector.get_book_genre('Неизвестная') is None


# Проверка: получение списка книг по определённому жанру
def test_get_books_with_specific_genre(collector):
    collector.add_new_book('Том и Джерри')
    collector.set_book_genre('Том и Джерри', 'Мультфильмы')
    collector.add_new_book('Дюна')
    collector.set_book_genre('Дюна', 'Фантастика')
    assert collector.get_books_with_specific_genre('Мультфильмы') == ['Том и Джерри']

# Проверка: книги с возрастным рейтингом не попадают в список детских книг
def test_get_books_for_children_excludes_age_rating_genre(collector):
    collector.add_new_book('Детская книга')
    collector.set_book_genre('Детская книга', 'Мультфильмы')
    collector.add_new_book('Взрослая книга')
    collector.set_book_genre('Взрослая книга', 'Детективы')
    assert 'Взрослая книга' not in collector.get_books_for_children()
    assert 'Детская книга' in collector.get_books_for_children()

# Проверка: добавление и удаление книги из избранного

def test_add_and_delete_book_in_favorites(collector):
    collector.add_new_book('Книга')
    collector.add_book_in_favorites('Книга')
    assert 'Книга' in collector.get_list_of_favorites_books()
    collector.delete_book_from_favorites('Книга')
    assert 'Книга' not in collector.get_list_of_favorites_books()

# Проверка: нельзя добавить в избранное книгу, которой нет в списке книг
def test_add_book_in_favorites_only_if_in_books_genre(collector):
    collector.add_book_in_favorites('Неизвестная')
    assert 'Неизвестная' not in collector.get_list_of_favorites_books()

# Проверка: нельзя добавить одну и ту же книгу в избранное дважды
def test_cannot_add_book_twice_in_favorites(collector):
    collector.add_new_book('Книга-2')
    collector.add_book_in_favorites('Книга-2')
    collector.add_book_in_favorites('Книга-2')
    assert collector.get_list_of_favorites_books().count('Книга-2') == 1    