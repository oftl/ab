from ab.base import NavTable, Link, KV

class Console (object):

    def __init__ (self):
        self._indent = 0
        self._nt = []
        self._no = 0


    def reset (self):
        self.__init__()


    def indent_more (self):
        self._indent += 2
        return self._indent


    def indent_less (self):
        self._indent -= 2
        return self._indent


    def indent (self):
        return self._indent


    def add_nav_entry (self, **kwa):
        if kwa:
            no = kwa.get ('no')
            href = kwa.get ('href')

            if no and href:
                self._nt.append (NavTable (kwa.get ('no'), kwa.get ('href')))

        return self._nt.append


    def nav_table (self):
        if not len (self._nt):
            raise UserWarning ('empty nav table')

        return self._nt


    def next_target_no (self):
        self._target_no += 1


    def no_for_href (self, **kwa):
        href = kwa.get ('href')
        self._no += 1

        self.add_nav_entry (no = self._no, href = href)
        return self._no


    def draw (self, thing):
        out = '\n'

        if type (thing) is dict:
            self.indent_more()

            for k, v in thing.items():
                out += '\n'
                out += '{ind}{key} ... {value}'.format (ind = ' ' * self.indent(), key = k, value = self.draw (v))

            self.indent_less()

        # elif type (thing) in [list, tuple]:
        elif type (thing) is list:
            self.indent_more()

            for t in thing:
                out += self.draw (t)

            self.indent_less()

        elif isinstance (thing, KV):
            out += '{ind}{key} ... {value}'.format (ind = ' ' * self.indent(), key = thing.key, value = thing.value)

        elif isinstance (thing, Link):
            out += '{ind}[{no}] {text} ({method} {href})'.format (
                ind = ' ' * self.indent(),
                no = self.no_for_href (href = thing.href),
                text = thing.text,
                method = thing.method,
                href = thing.href,
            )

        else:
            out += '<%s>' % thing

        return out
