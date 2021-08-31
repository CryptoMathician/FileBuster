from datetime import date, timedelta
from typing import Union
from termcolor import colored
import sys
"""
example input:
2020-01-01 2022-12-31 -upload
"""


def run(lst: list) -> Union[list, None]:
    """
    This example plugin generates a wordlist with dates and a concatinated string to it.
    :param lst:
    :return:
    """
    wlist = []

    if len(lst) > 3:
        return None

    dates = []
    ext = ""

    for ii, el in zip(range(len(lst)), lst):
        if ii == 0 or ii == 1:
            el2 = el.strip().split('-')
            if len(el2) > 3:
                return None
            try:
                dates.append(date(int(el2[0]), int(el2[1]), int(el[2])))
            except ValueError as e:
                print(e.with_traceback(), file=sys.stderr)
        else:
            ext = el

    print(colored(f"Try documents with a name like {lst[0] + ext}.<extension>", "yellow"))

    delta = dates[1] - dates[0]

    for ii in range(delta.days + 1):
        day = dates[0] + timedelta(days=ii)
        wlist.append(f"{str(day)}{ext}")

    return wlist