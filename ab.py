#!/usr/bin/env python3

import re
import os
import pprint
import logging
import urllib

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token

import sys
sys.path = sys.path[1:] + ['']  # WTF

import ab.http
import ab.ui


history = FileHistory (os.path.expanduser ('~/.ab.history'))

def get_bottom_toolbar_tokens (cli):
    last = history.strings[-1] if history else ''
    return [(Token.Toolbar, 'Last address: {adr}'.format (adr = last))]


def main ():
    completer = WordCompleter ('http:// https:// ftp:// ftps://'.split())

    method = 'GET'
    request = ab.http.Request()
    ui = ab.ui.Console()

    while True:
        ui.reset()

        cmd = prompt (
            '> ',
            completer = completer,
            history   = history,
            auto_suggest = AutoSuggestFromHistory(),
            get_bottom_toolbar_tokens = get_bottom_toolbar_tokens,
            style = style_from_dict ({ Token.Toolbar: '#ffffff bg:#333333' }),
        )

        url = ''

        if re.search ('^open (.+)', cmd):
            url = cmd[5:]

        elif re.search ('^\d+$', cmd):
            url = list (filter (lambda n: str(n.no) == cmd, ui.nav_table())).pop().href

            # keep history reusable
            history.strings.pop()
            history.append ('open %s' % url)

        else:
            raise UserWarning ('invalid input')

        ret = dict (
            GET = request.get (url = url),
        ).get (method)

        href, items = ret.get ('href'), ret.get ('items')

        log ('base items: %s' % items)
        print (ui.draw (items))

log = lambda msg, level=logging.INFO: logger.info (msg)

if __name__ == '__main__':
    handler = logging.FileHandler ('./ab.log')
    handler.setFormatter (logging.Formatter (fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger = logging.getLogger ('ab')
    logger.addHandler (handler)
    logger.setLevel (logging.INFO)

    main()
