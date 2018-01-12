import requests
import logging
import json
import pprint

# from ab.base import Link, KV
from ab.base import Link, Data, Item

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

        self.log ('content type: <{ct}>'.format (ct = ct))
        self.log ('raw response: <{response}>'.format (response = response))
        self.log ('response text: <{response}>'.format (response = response.text))
        with open ('./raw-response', 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)

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

        # version and href SHOULD be there

        res = dict (
            version = data.get ('version'),
            href = data.get ('href'),
        )

        # items, links, template, queries, error MAY be there

        if data.get ('items'):
            res.update (dict (items = [
                Item (
                    href = item.get ('href'),
                    data = [
                        Data (
                            name   = data.get ('name'),
                            value  = data.get ('value'),
                            prompt = data.get ('prompt'),
                        )
                        for data in item.get ('data')
                    ],
                    #  links = [
                    #      Link (
                    #          method = 'GET',
                    #          rel    = link.get ('rel'),
                    #          href   = link.get ('href'),
                    #          prompt = link.get ('prompt'),
                    #      )
                    #      for link in item.get ('links')
                    #  ],
                )
                for item in data.get ('items')
            ]))


        if data.get ('links'):
            res.update (dict (links = [
                Link (
                    method = 'GET',
                    rel    = link.get ('rel'),
                    href   = link.get ('href'),
                    prompt = link.get ('prompt'),
                )
                for link in data.get ('links')
            ]))

        if data.get ('template'):
            res.update (dict (template = data.get ('template')))

        if data.get ('queries'):
            res.update (dict (template = data.get ('queries')))

        if data.get ('error'):
            res.update (dict (template = data.get ('error')))

        self.log ('Collection_JSON.ab res: %s' % res)
        return res

class TextHTML (object):

    def __init__ (self, **kwa):
        super().__init__()
        self.href = kwa.get ('href')


    def ab (self, **kwa):
        return dict (
            href = self.href,
            thing = kwa.get('data').content,
        )
