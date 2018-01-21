class NavTable ():

    def __init__ (self, **kwa):
        self._targets = []

    #  def __repr__ (self):
    #      return "Item (href={href}, data={data}, links={links})".format (
    #          href   = self.href,
    #          data   = self.data,
    #          links  = self.links,
    #      )

    def fetch (self, **kwa):
        no = kwa.get ('no')

        targets = [tgt.get ('href') for tgt in self._targets if tgt.get ('no') == no]

        if len(targets):
            return targets.pop()
        else:
            raise RuntimeWarning ('invalid no')


    def set (self, **kwa):
        no = len (self._targets)

        self._targets.append (dict (
            no   = no,
            href = kwa.get ('href'),
        ))

        return no

class Item ():

    def __init__ (self, **kwa):
        self._href   = kwa.get ('href')
        self._data   = kwa.get ('data')
        self._links  = kwa.get ('links')

    def __repr__ (self):
        return "Item (href={href}, data={data}, links={links})".format (
            href   = self.href,
            data   = self.data,
            links  = self.links,
        )

    @property
    def href (self):
        return self._href

    @href.setter
    def set_href (self, href):
        self._href = href
        return self._href

    @property
    def data (self):
        return self._data

    @data.setter
    def set_data (self, data):
        if type (data) != list:
            raise (TypeError, 'expected type <list>')
        for d in data:
            if type (d) != Data:
                raise (TypeError, 'expected type <Data>')

        self._data = data
        return self._data

    @property
    def links (self):
        return self._links

    @links.setter
    def set_links (self, links):
        if type (links) != list:
            raise (TypeError, 'expected type <list>')
        for l in links:
            if type (l) != Link:
                raise (TypeError, 'expected type <Link>')

        self._links = links
        return self._links

class Data ():

    def __init__ (self, **kwa):
        self._name   = kwa.get ('name')
        self._value  = kwa.get ('value')
        self._prompt = kwa.get ('prompt')

    def __repr__ (self):
        return "Data (name={name}, value={value}, prompt={prompt})".format (
            name   = self.name,
            value  = self.value,
            prompt = self.prompt,
        )

    @property
    def name (self):
        return self._name

    @name.setter
    def set_name (self, name):
        self._name = name
        return self._name

    @property
    def value (self):
        return self._value

    @value.setter
    def set_value (self, value):
        self._value = value
        return self._value

    @property
    def prompt (self):
        return self._prompt

    @prompt.setter
    def set_prompt (self, prompt):
        self._prompt = prompt
        return self._prompt

class Link ():

    def __init__ (self, **kwa):
        self._method  = kwa.get ('method')
        self._rel     = kwa.get ('rel')
        self._href    = kwa.get ('href')
        self._prompt  = kwa.get ('prompt')
        self._render  = kwa.get ('render')

    def __repr__ (self):
        return "Link (method={method}, rel={rel}, href={href}, prompt={prompt}, render={render})".format (
            method  = self.method,
            rel     = self.rel,
            href    = self.href,
            prompt  = self.prompt,
            render  = self.render,
        )

    @property
    def method (self):
        return self._method

    @method.setter
    def set_method (self, method):
        self._method = method
        return self._method

    @property
    def rel (self):
        return self._rel

    @rel.setter
    def set_rel (self, rel):
        self._rel = rel
        return self._rel

    @property
    def href (self):
        return self._href

    @href.setter
    def set_href (self, href):
        self._href = href
        return self._href

    @property
    def prompt (self):
        return self._prompt

    @prompt.setter
    def set_prompt (self, prompt):
        self._prompt = prompt
        return self._prompt

    @property
    def render (self):
        return self._render

    @render.setter
    def set_render (self, render):
        self._render = render
        return self._render
