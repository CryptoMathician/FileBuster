#!/usr/bin/env python

import argparse
import importlib
import sys
from typing import Union

import requests as req
from urllib.parse import urljoin
import os
from termcolor import colored

"""
Usage example of this tool:
./main.py -w wordlist.txt http://10.10.10.248/documents/ -n jpg -d output 
./main.py --date-generator http://10.10.10.248/documents/ -n pdf -d output
"""


def get_req(url: str, headers: dict, directory: str, fname: str) -> None:
    """
    Do a request and write a founded document to a file with the same name of the document and the specified directory
    :param url:
    :param headers:
    :param directory:
    :param fname:
    :return:
    """
    # print(colored(f"url: {url}", "blue"))
    res = req.get(url, headers=headers)
    if res.status_code == 200:
        print(colored(f"url: {url}", "green"))
        # create output directory if necessary
        if directory != "" and not os.path.exists(directory):
            os.mkdir(directory)
        # save document to file
        with open(os.path.join(directory, fname), "wb") as f2:
            f2.write(res.content)


def wordlist_downloader(url: str, wlist: Union[str, list], headers: dict = {}, extensions: list = [], directory: str = "") -> None:
    """

    :param url:
    :param wlist:
    :param headers:
    :param extensions:
    :param directory:
    :return:
    """
    if type(wlist) == str:
        # Read the wordlist and try every word and extensions permutation.
        # If the file exist download it and save it as a file in the specified directory
        with open(wlist, "r") as f:
            for word in f:
                for extension in extensions:
                    # add extensions to word and build a proper url and request it via get method
                    fname = f"{word}.{extension}"
                    url2 = urljoin(url, fname)
                    get_req(url2, headers, directory, fname)
    elif type(wlist) == list:
        for word in wlist:
            for extension in extensions:
                fname = f"{word}.{extension}"
                url2 = urljoin(url, fname)
                get_req(url2, headers, directory, fname)


def load_plugin(name):
    return importlib.import_module(f"plugins.{name}", ".").run


if __name__ == '__main__':

    # prepare argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--wordlist", help="wordlist for dictionary attack")
    parser.add_argument("url", help="url to scrape")
    parser.add_argument("-n", "--extensions", nargs="+", default=[], help="list of extensions to try")
    parser.add_argument("-d", "--directory", help="directory output")
    parser.add_argument("--generator", help="use generator to generate wordlist")
    parser.add_argument("--data", nargs=argparse.REMAINDER, default=[], help="list of data")

    # parse the arguments
    args = parser.parse_args()

    wordlist = []
    if args.generator and not args.wordlist and args.data:
        run = load_plugin(args.generator)
        wordlist = run(args.data)
        if wordlist is None:
            print(f"Error on loading plugin {args.generator} and run \"run\"", file=sys.stderr)

    # argument logic
    if args.url:
        if args.extensions:
            if args.directory:
                if args.wordlist:
                    wordlist_downloader(args.url, args.wordlist, extensions=args.extensions, directory=args.directory)
                else:
                    wordlist_downloader(args.url, wordlist, extensions=args.extensions, directory=args.directory)
            else:
                wordlist_downloader(args.url, args.wordlist, extensions=args.extensions)
        else:
            wordlist_downloader(args.url, args.wordlist, extensions=["pdf"])
