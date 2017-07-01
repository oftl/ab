import requests
import logging
import json
import pprint
import collections

from ab.base import Link, KV

class Request (object):

    def __init__ (self):
        self.logger = logging.getLogger ('ab')
        self.log = lambda msg, level=logging.INFO: self.logger.info (msg)


    def get (self, **kwa):
        url = kwa.get ('url')

        self.log ('GET from <{url}>'.format (url = url))
        response = requests.get (url)

        return self.handle_response (response = response)

    def handle_response (self, **kwa):
        response = kwa.get ('response')
        ct = response.headers.get ('Content-Type')

        self.log ('raw response: {response}'.format (response = response))
        self.log ('content type: <{ct}>'.format (ct = ct))

        # XXX ct can include profile link XXX
        if ct == 'application/vnd.collection+json':
            strategy = Collection_JSON()
        #  elif ct == 'application/json':
        #      strategy = Collection_JSON()
        elif ct == 'text/html':
            strategy = TextHTML (href = url)
        else:
            raise UserWarning ('unknown content type: <{ct}>'.format(ct=ct))

        return strategy.ab (data = response)

class TheOrigin (object):

    def __init__ (self):
        self.logger = logging.getLogger ('ab')
        self.log = lambda msg, level=logging.INFO: self.logger.info (msg)

class Collection_JSON (TheOrigin):

    def __init__ (self):
        super().__init__()


    def ab (self, **kwa):
        data = json.loads (kwa.get('data').content).get ('collection')

        # self.log ('version: {}'.format (data.get ('version')))
        # self.log ('href: {}'.format (data.get ('href')))
        # self.log ('items: \n{}'.format (pprint.pformat (data.get ('items'), indent=2)))
        # self.log ('template: {}'.format (data.get ('template')))

        return dict (
            href = data.get ('href'),
            thing = [
                dict (
                    thing = [
                        KV (d.get ('name'), d.get ('value'))
                        for d in i.get ('data')
                    ],
                    links = [
                        Link ('DELETE', 'delete', i.get ('href')),
                        Link ('GET',    'view',   i.get ('href')),
                    ]
                )
                for i in data.get ('items')
            ],
            links = [
                Link ('DELETE', 'delete all', data.get ('href')),
                Link ('POST',   'new item',   data.get ('href')),
            ],
            template = data.get ('template'),
        )

        return self.ab (data = self.reply)

class TextHTML (object):

    def __init__ (self, **kwa):
        super().__init__()
        self.href = kwa.get ('href')


    def ab (self, **kwa):
        return dict (
            href = self.href,
            thing = kwa.get('data').content,
        )
