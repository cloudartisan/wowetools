#!/usr/bin/env python


import sys
import os
from glob import glob
from optparse import OptionParser


MONTHS = [
    "jan", "january",
    "feb", "february",
    "mar", "march",
    "apr", "april",
    "may",
    "jun", "june",
    "jul", "july",
    "aug", "august",
    "sep", "sept", "september",
    "oct", "october",
    "nov", "november",
    "dec", "december"
]

BOOK_TYPES = [ "pdf", "epub", "mobi" ]


class Book(object):
    def __init__(book_path):
        self.book_path = book_path
        self.book_dir = os.path.dirname(self.book_path)
        self.book_name, self.book_ext = os.path.splitext(os.path.basename(self.book_path))
        self.publisher = ""
        # Fix publisher names and separate from book title with a hyphen
        book_name_bits = self.book_name.split(".")
        if book_name_bits[0] == "Oreilly":
            self.publisher = "O'Reilly"
        elif book_name_bits[0:2] in (["Addison", "Wesley"], ["Pragmatic",
            "Programmer"], ["Prentice", "Hall"], ["McGraw", "Hill"],
            ["No", "Starch"]):
            self.publisher = " ".join(book_name_bits[0:2])
        elif book_name_bits[0] in ("Apress", "Artima", "Packtpub",
            "Pragmatic", "Wiley", "Wrox"):
            self.publisher = book_name_bits[0]


def get_books(path):
    books = []
    for book_type in BOOK_TYPES:
        books.extend(glob("%s/*.%s" % (path, book_type)))
    return books


def main():
    usage = "Usage: %prog [options] <path> [[path] [path] ...]"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--delete-originals", dest="delete_originals",
                      default=False, help="Delete the original files")
    (opts, args) = parser.parse_args()
    # First, make sure all the supplied paths are directories
    for path in args:
        if not os.path.isdir(path):
            parser.error("%s is not a directory" % path)
            sys.exit(1)
    for path in args:
        for book_path in get_books(path):
            book = Book(book_path)
            book_dir = os.path.dirname(book_path)
            book_name, book_ext = os.path.splitext(os.path.basename(book_path))
            book_name_bits = book_name.split(".")

            # Ends with a year?
            try:
                int(book_name_bits[-1])
                # Remove it
                book_name_bits = book_name_bits[:-1]
            except:
                pass

            # Ends with a month?
            if book_name_bits[-1].lower() in MONTHS: 
                # Remove it
                book_name_bits = book_name_bits[:-1]

            # "Xth/Xnd/Xrd Edition" -> "(Xth/Xnd/Xrd Edition)"
            if book_name_bits[-1].lower() == 'edition':
                book_name_bits[-2] = "(" + book_name_bits[-2]
                book_name_bits[-1] = book_name_bits[-1] + ")"

            # Fix publisher names and separate from book title with a hyphen
            if book_name_bits[0] == "Oreilly":
                book_name_bits[0] = "O'Reilly -"
            elif book_name_bits[0:2] in (["Addison", "Wesley"], ["Pragmatic",
                "Programmer"], ["Prentice", "Hall"], ["McGraw", "Hill"],
                ["No", "Starch"]):
                book_name_bits[1] = book_name_bits[1] + " -"
            elif book_name_bits[0] in ("Apress", "Artima", "Packtpub",
                "Pragmatic", "Wiley", "Wrox"):
                book_name_bits[0] = book_name_bits[0] + " -"

            new_book_filename = " ".join(book_name_bits) + book_ext
            new_book_filename = os.path.join(book_dir, new_book_filename)
            print "%s -> %s" % (book_path, new_book_filename)
            os.rename(book_path, new_book_filename)
            if opts.delete_originals:
                os.remove(book_path)


if __name__ == "__main__":
    main()
