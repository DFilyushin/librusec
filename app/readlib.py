# -*- coding: utf-8 -*-
import os
import subprocess
import settings


def get_archive_file(id_book):
    for archive in os.listdir(settings.LIB_ARCHIVE):
        if archive.endswith('.zip'):
            fb, start, end = archive[:-4].split('-')
            pos = end.find('_')
            if pos > -1:
                end = end[:pos]
            start_num = int(start)
            end_num = int(end)
            if (id_book >= start_num) and (id_book <= end_num):
                return archive


def extract_book(id_book, type_book):
    archive = get_archive_file(id_book)
    arc = os.path.join(settings.LIB_ARCHIVE, archive)
    book = '%d.%s' % (id_book, type_book)
    where_extract = '-o%s' % settings.TMP_DIR

    cmd = ['7z', 'e', arc, book, where_extract]
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    p.wait()
    return os.path.join(settings.TMP_DIR, book)
