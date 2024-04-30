from ..shapes import *


def test_book_counts():
    assert len(old_testament) == 39
    assert len(new_testament) == 27
    assert len(book_of_mormon) == 15
    assert len(pearl_of_great_price) == 5


def assert_book(book, name, ordinal, abbrev, *names):
    assert book.names[0] == name
    assert book.ordinal == ordinal
    assert book.abbrev == abbrev
    if names:
        other_names = book.names[1:]
        for n in names:
            assert n in other_names

def test_easy_book():
    assert_book(new_testament[0], 'matthew', None, 'Matt')


def test_ordinal_book():
    assert_book(book_of_mormon[10], 'nephi', '3', 'Ne')


def test_book_without_abbrev():
    assert_book(book_of_mormon[2], 'jacob', None, None)


def test_hard_book():
    assert_book(old_testament[21], 'songofsolomon', None, 'Song', 'sos', 'songofsongs', 'canticles')


def test_uniques():

    # This test actually does a lot of work to calculate the correct minimum unique
    # abbreviation for each book. That's because calculating these abbreviations takes
    # longer than I want, so I want to hard-code the values in my array. If I get any
    # of the hard-coded values wrong, I want the test to tell me.

    def count_common(a, b):
        max_common = min(len(a), len(b))
        for i in range(max_common):
            if a[i] != b[i]:
                return i
        return max_common

    def uniques_are_perfect():
        perfect = True
        for book in next_book(library):
            name = book.unique_basis
            common_len = 2 if book.ordinal else 1
            # Look at all other books; see which has the most letters in common
            # with the name of this one.
            for book2 in next_book(library):
                if book2 != book:
                    name2 = book2.unique_basis
                    common_len = max(common_len, count_common(name, name2))
            expected_unique = name[:common_len + 1].replace('-', '')
            if book.unique != expected_unique:
                print('Expected unique for %s to be "%s", not "%s"' % (book.abbrev_title, expected_unique, book.unique))
                perfect = False
        return perfect

    assert uniques_are_perfect()


def assert_found(lookup, title):
    x = find_book(lookup)
    assert x
    assert x.title == title


def test_books_found():
    assert_found('1jn', '1 John')
    assert_found('Joseph Smith History', 'Joseph Smith - History')
    assert_found('d & c', 'Doctrine & Covenants')
    assert_found('d&c', 'Doctrine & Covenants')
    assert_found('art of faith', 'Articles of Faith')
    assert_found('a of f', 'Articles of Faith')
    assert_found('articles of faith', 'Articles of Faith')
    assert_found('jshist', 'Joseph Smith - History')
    assert_found('jshistory', 'Joseph Smith - History')
    assert_found('joseph smith-m', 'Joseph Smith - Matthew')
    assert_found('js-m', 'Joseph Smith - Matthew')
    assert_found('js&mdash;m', 'Joseph Smith - Matthew')
    assert_found('jsm', 'Joseph Smith - Matthew')
    assert_found('eze', 'Ezekiel')
    assert_found('do', 'Doctrine & Covenants')
    assert_found('d&amp;c', 'Doctrine & Covenants')
    assert_found('d&c', 'Doctrine & Covenants')
    assert_found('dc', 'Doctrine & Covenants')
    assert_found('lu', 'Luke')
    assert_found('Matthe', 'Matthew')
    assert_found('sos', 'Song of Solomon')
    assert_found('Canticles', 'Song of Solomon')
    assert_found('ThirdJohn.', '3 John')
    assert_found('2nd Pet.', '2 Peter')
    assert_found('4th nephi', '4 Nephi')
    assert_found('3 ne.', '3 Nephi')
    assert_found('1chr', '1 Chronicles')
    assert_found('1 chron', '1 Chronicles')
    assert_found('genesis', 'Genesis')


def test_books_not_found():
    # Not enough characters for reliable match
    assert find_book('m') is None
    # Too many characters
    assert find_book('matthewx') is None
    # Same as a unique prefix, but diverges after
    assert find_book('gesxyz') is None
    # Partial name that isn't canonical and therefore not truncatable
    assert find_book('Cantic') is None
