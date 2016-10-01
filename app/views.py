# -*- coding: utf-8 -*-
import os
import time
from app import librusec
from flask import render_template, request, abort, send_file, g
from models import Authors, Books, Genre
from readlib import extract_book

RUSSIAN_LETTERS = u'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЭЮЯ'


def get_author_by_id(id_author):
    author = Authors.query.filter_by(id=id_author).one()
    return author.first_name + ' ' + author.last_name


def get_genres():
    genre = getattr(g, 'genre', None)
    if genre is None:
        g.genre = {}
        rows = Genre.query.all()
        for row in rows:
            g.genre[row.id_genre] = row.ru_genre
    return g.genre


def process_books(books_rows):
    q_genres = get_genres()
    for row in books_rows:
        genre_line = row.genre[:-1]
        genres = genre_line.split(':')
        ru_genres = []
        for genre in genres:
            ru_genres.append(q_genres.get(genre, genre))
        row.genre = ', '.join(ru_genres)
    return books_rows


@librusec.route('/')
def index():
    letters = list(i for i in RUSSIAN_LETTERS)
    return render_template("index.html", letters=letters)


@librusec.route('/authors', methods=['GET'])
def authors():
    """
    Get list of authors
    :return:
    """
    writers = None
    letter = request.args.get('letter', '')
    if letter != '':
        try:
            idx = int(letter)
        except ValueError:
            abort(404)
        symbol = RUSSIAN_LETTERS[idx - 1:idx]
        writers = Authors().query.filter(Authors.last_name.like('%s%%' % symbol)).order_by(Authors.last_name)
    letters = list(i for i in RUSSIAN_LETTERS)
    return render_template("authors.html", letters=letters, authors=writers)


@librusec.route('/authorbook', methods=['GET'])
def book_by_author():
    """
    Get list book by author id
    :return:
    """
    get_id = request.args.get('id', '')
    try:
        id_author = int(get_id)
        author = get_author_by_id(id_author)
    except ValueError:
        abort(404)
    books = Books.query.filter(Books.authors.any(id=id_author))
    books2 = process_books(books)
    return render_template("books.html", books=books2, author=author)


@librusec.route('/search', methods=['POST'])
def search():
    """
    Search book by book name
    :return:
    """
    text = request.form['search_text']
    start_time = time.time()
    books = Books.query.filter(Books.name.like('%s%%' % text.lower()))

    author_book = Books.query.filter(Books.authors.any(Authors.last_name.like('%s%%' % text.lower())))
    elapsed = (time.time() - start_time)
    return render_template("books.html", books=books, author_books=author_book, find_text=text, elapsed=elapsed)


@librusec.route('/download/<int:id_book>', methods=['GET'])
def download(id_book):
    """
    Download book from zip archive
    :param id_book:
    :return:
    """
    book = Books.query.filter_by(id=id_book).one()
    id_file = extract_book(id_book, book.type)
    file_name = os.path.basename(id_file)
    return send_file(filename_or_fp=id_file,
                     mimetype='document/fb2',
                     attachment_filename=file_name,
                     as_attachment=True)


@librusec.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
