import logging

from ab.base import NavTable
from ab.base import Link, Data, Item

class Console (object):

    def __init__ (self):
        self._indent = 0
        self._nt = NavTable()
        self._no = 0
        self.logger = logging.getLogger ('ab')
        self.log = lambda msg, level=logging.INFO: self.logger.info (msg)


    def reset (self):
        # self.__init__()
        pass


    def indent_more (self):
        self._indent += 2
        return self._indent


    def indent_less (self):
        self._indent -= 2
        return self._indent


    def indent (self):
        return self._indent


    #  def add_nav_entry (self, **kwa):
    #      href = kwa.get ('href')
    #
    #      if href:
    #          no = self._nt.set (href = href)
    #          return no
    #
    #
    #  def nav_table (self):
    #      if not len (self._nt):
    #          raise UserWarning ('empty nav table')
    #
    #      return self._nt
    #
    #
    #  def next_target_no (self):
    #      self._target_no += 1


    def draw (self, thing):
        out = '\n'

        # if type (thing) in [list, tuple]:
        if type (thing) is list:
            self.indent_more()

            for t in thing:
                out += self.draw (t)

            self.indent_less()

        elif isinstance (thing, Item):
            out += '{indent}[{index}] {prompt} ({href})'.format (
                indent = ' ' * self.indent(),
                index  = self._nt.set (href = thing.href),
                prompt = 'Permaurl',
                href   = 'GET ' + thing.href,
            )

            out += self.draw (thing.data)
            out += self.draw (thing.links)

        elif isinstance (thing, Data):
            out += '{indent}{prompt}: {value}'.format (
                indent = ' ' * self.indent(),
                prompt = thing.prompt,
                value  = thing.value,
            )

        elif isinstance (thing, Link):
            out += '{indent}[{index}] {prompt} ({method} {href})'.format (
                indent = ' ' * self.indent(),
                index  = self._nt.set (href = thing.href),
                prompt = thing.prompt,
                method = thing.method,
                href   = thing.href,
            )

        else:
            out += '<%s>' % thing

        return out
