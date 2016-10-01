# -*- coding: utf-8 -*-
import os
import datetime
import time
import MySQLdb as mdb

LIB_INDEXES = 'D:\\TEMP\\librusec'
MYSQL_HOST = '127.0.0.1'
MYSQL_BASE = 'books100'
MYSQL_LOGIN = 'root'
MYSQL_PASSW = 'qwerty'

SQL_CHECK_BASE = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '%s'"
SQL_CREATE_BASE = "CREATE DATABASE `%s` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;"
SQL_USE_BASE = 'USE `%s`;'


class BookDatabase(object):
    """
    Database class for store books
    """
    SQL_NEW_BOOK = u"INSERT INTO books VALUES ({0}, '{1}', {2}, '{3}', '{4}', '{5}')"
    SQL_CHECK_AUTHOR = u"select id from authors where last_name='{0}' and first_name = '{1}' and middle_name='{2}'"
    SQL_NEW_AUTHOR = u"INSERT INTO authors (last_name, first_name, middle_name) VALUES ('{0}', '{1}', '{2}')"
    SQL_NEW_LINK = u"INSERT INTO link_ab VALUES ({0}, {1})"

    def __init__(self):
        self._conn = mdb.connect(MYSQL_HOST, MYSQL_LOGIN, MYSQL_PASSW, MYSQL_BASE, charset='utf8')
        self._cur = self._conn.cursor()

    def get_last_row_id(self):
        return self._cur.lastrowid

    def exec_sql(self, sql):
        return self._cur.execute(sql)

    def get_row_count(self):
        return self._cur.rowcount

    def get_value(self, index):
        data = self._cur.fetchone()
        return data[index]

    def store_author(self, last_name, first_name, middle_name):
        """
        Store new author with check existing record
        :param last_name: last name author
        :param first_name: first name author
        :param middle_name: middle name author
        :return: Id new record
        """
        sql = self.SQL_CHECK_AUTHOR.format(last_name, first_name, middle_name)
        self.exec_sql(sql)
        if self.get_row_count() == 0:
            sql = self.SQL_NEW_AUTHOR.format(last_name, first_name, middle_name)
            self.exec_sql(sql)
            id_author = self.get_last_row_id()
        else:
            id_author = self.get_value(0)
        return id_author

    def store_book(self, id_book, name, book_size, book_type, lang, genre):
        """
        Store new book
        :param id_book: Id book
        :param name: Name of book
        :param book_size: Size book in bytes
        :param book_type: Type book
        :param lang: Language book
        :param genre: Genres
        :return: Id new record
        """
        book_name = name.replace("'", '`')
        sql = self.SQL_NEW_BOOK.format(id_book, book_name, book_size, book_type, lang, genre)
        self.exec_sql(sql)
        return id_book

    def store_author_in_book(self, id_book, id_author):
        """
        Store links for book+author
        :param id_book: Id book
        :param id_author: Id author
        :return: nothing
        """
        sql = self.SQL_NEW_LINK.format(id_book, id_author)
        self.exec_sql(sql)


def create_schema(filename):
    """
    Create database schema from sql-file
    :param filename: Input schema sql-file for MySql
    :return:
    """
    start = time.time()

    f = open(filename, 'r')
    sql = " ".join(f.readlines())
    print "Start executing: " + filename + " at " + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" + sql
    conn = mdb.connect(MYSQL_HOST, MYSQL_LOGIN, MYSQL_PASSW)
    cur = conn.cursor()
    sql_check = SQL_CHECK_BASE % MYSQL_BASE
    cur.execute(sql_check)
    if cur.rowcount == 0:
        cur.execute(SQL_CREATE_BASE % MYSQL_BASE)
        cur.execute(SQL_USE_BASE % MYSQL_BASE)
        cur.execute(sql)
    else:
        print "Database exist. Stop!"

    end = time.time()
    print "Time elapsed to run the query:"
    print str((end - start)*1000) + ' ms'


def process_file(inp_file, book_db):
    with open(inp_file) as f:
        row_counter = 0
        for line in f:
            row_counter += 1
            line = line.decode('utf-8').strip()
            book_item = line.split(chr(4))
            bid = book_item[7]
            bname = book_item[2]
            bsize = book_item[6]
            btype = book_item[9]
            blang = book_item[11]
            bgenre = book_item[1]
            try:
                id_book = book_db.store_book(int(bid), bname, int(bsize), btype, blang, bgenre)
            except IndexError:
                print 'Index error in %s file (%d line)' % (inp_file, row_counter)
            except Exception as e:
                print 'Error message: %s (%s)' % (e.args, e.message)

            author_line = line.split(chr(4))[0]
            author_line = author_line.replace("'", '`')
            authors = author_line.split(':')
            for author in authors:
                item = author.split(',')
                if len(item) > 1:
                    try:
                        id_author = book_db.store_author(item[0], item[1], item[2])
                    except Exception as e:
                        print 'Error message author: %s (%s). Error in %s file (%d line)' % (e.args, e.message, inp_file, row_counter)
                    try:
                        book_db.store_author_in_book(id_book, id_author)
                    except Exception as e:
                        print 'Error message link: %s (%s). Error in %s file (%d line)' % (e.args, e.message, inp_file, row_counter)


def process_index_files(path_to_index):
    """
    Processing all files in path LIB_INDEXES
    :param path_to_index: path to LIB_ARCHIVE
    :return:
    """
    book_db = BookDatabase()

    index = 0
    indexes = filter(lambda x: x.endswith('.inp'), os.listdir(path_to_index))
    cnt_files = len(indexes)
    os.chdir(path_to_index)
    for index_file in indexes:
        index += 1

        print 'Process file %s. File %d from %d' % (index_file, index, cnt_files)

        start_time = time.time()
        process_file(index_file, book_db)
        elapsed = (time.time() - start_time)

        print "Ok. Processing in {:10.4f} s.".format(elapsed)


def main():
    create_schema('schema.sql')
    process_index_files(LIB_INDEXES)

if __name__ == "__main__":
    main()
