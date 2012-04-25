#!/usr/bin/env python2.7
import os, sys, argparse, logging
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Convert Google Docs to SISG document.')


parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
        default=sys.stdin)

parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
        default=sys.stdout)

args = parser.parse_args()

html = args.infile.read().decode('utf8')

soup = BeautifulSoup(html)

header = title = subtitle = paragraphs = None

# First <div> of the document is the feader
header = soup.div.get_text()

# Div tags are headers or footers.
for tag in soup.find_all('div'):
    tag.extract()

# There is no footer, but if there was it'd be the last div in the document

title = soup.find("p", "title").get_text()

subtitle = soup.find("p", "subtitle").get_text()

######
# TeX escaping
tex_replacements = [
    (u'{', ur'\{'),
    (u'}', ur'\}'),
    (u'[', ur'{[}'),
    (u']', ur'{]}'),
    (u'\\', ur'\textbackslash{}'),
    (u'$', ur'\$'),
    (u'%', ur'\%'),
    (u'&', ur'\&'),
    (u'#', ur'\#'),
    (u'_', ur'\_'),
    (u'~', ur'\textasciitilde{}'),
    (u'^', ur'\textasciicircum{}'),
]

tex_mapping = {ord(char):rep for char, rep in tex_replacements}

def tex_escape(txt):
    """Convert txt to a LaTeX-safe string"""
    return unicode(txt).translate(tex_mapping)


class TagStrategy(object):
    """Base class; given a soup tag, process all subtags
    """

    # Map handlers e.g. "body" => "DocumentStrategy", "b" => "BoldStrategy"
    handlers = {}

    def __init__(self, tag=None):
        if not TagStrategy.handlers:
            TagStrategy.register_all_strategies()

        self.tag = tag

    @classmethod
    def register_all_strategies(cls):
        print "Registering: %s" % cls.__name__

        try:
            cls.handlers[cls.tag] = cls
        except AttributeError:
            pass

        for sc in cls.__subclasses__():
            sc.register_all_strategies()

    def wrap(self, txt):
        logging.warning("%s does not overload wrap." % self.__class__.__name__)
        return txt

    def translate(self, parent_tag):
        """Given a tag, recurse."""
        rst = ""

        tags = parent_tag() # get list of descendents

        if not tags:
            # We're at a leaf; return the wrapped string.
            return self.wrap(tex_escape(parent_tag.string))

        for tag in parent_tag():
                # skip empties
            if not tag.get_text().strip():
                continue

            strat = TagStrategy.factory(tag)
            rst += strat.translate(tag)

            # rst += "str[%s]\n" % len(tag) # unicode(tag) + "\n"

        return self.wrap(rst)

    @classmethod
    def factory(cls, tag):
        # print "Handlers: %s" % TagStrategy.handlers
        return TagStrategy.handlers[tag.name](tag)


class BodyStrategy(TagStrategy):
    tag = 'body'

    def wrap(self, txt):
        return "\\begin{document}\n%s\n\\end{document}" % txt
    
class PStrategy(TagStrategy):
    tag = 'p'

    def wrap(self, txt):
        return "\par{}%s\n\n" % txt

class SpanStrategy(TagStrategy):
    tag = 'span'

    def wrap(self, txt):
        return txt

class H1Strategy(TagStrategy):
    tag = 'h1'

class H2Strategy(TagStrategy):
    tag = 'h2'

class H3Strategy(TagStrategy):
    tag = 'h3'

class H6Strategy(TagStrategy):
    tag = 'h6'

    def wrap(self, txt):
        return "\n\\textbf{%s}%%\n" % txt

class OlStrategy(TagStrategy):
    tag = 'ol'

    def wrap(self, txt):
        # FIXME: attr start = 1
        return "\\begin{enumerate}%%\n%s\n\\end{enumerate}%%\n" % txt

class LiStrategy(TagStrategy):
    tag = 'li'

    def wrap(self, txt):
        return "%%\n\t\\item{}%s" % txt

class BrStrategy(TagStrategy):
    tag = 'br'

    def wrap(self, txt):
        return "%%\n\par{}%%\n%s" % txt

class TableStrategy(TagStrategy):
    tag = 'table'

class TBodyStrategy(TagStrategy):
    tag = 'tbody'

class TrStrategy(TagStrategy):
    tag = 'tr'

class TdStrategy(TagStrategy):
    tag = 'td'

class AStrategy(TagStrategy):
    tag = 'a'

class HrStrategy(TagStrategy):
    tag = 'hr'

print BodyStrategy().translate(soup.body)

print repr(u"""----------\n
Header: %(header)s
Title: %(title)s
Subtitle: %(subtitle)s"""
 % locals())


