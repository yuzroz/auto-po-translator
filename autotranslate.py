#!/usr/bin/python
import os
import sys

from microsofttranslator import Translator
from translate.storage import po

MS_APP_ID = os.environ['MS_APP_ID']
MS_APP_SECRET = os.environ['MS_APP_SECRET']


def ms_get_translation(sl, tl, x):
    translator = Translator(MS_APP_ID, MS_APP_SECRET)
    return translator.translate(x, tl, sl)


def translate_po(file_path, sl, tl):
    openfile = po.pofile(open(file_path))
    nb_elem = len(openfile.units)
    moves = 1
    cur_elem = 0
    for unit in openfile.units:
        # report progress
        cur_elem += 1
        s = "\r%f %% - (%d msg processed out of %d) " \
            % (100 * float(cur_elem) / float(nb_elem), cur_elem, nb_elem)
        sys.stderr.write(s)
        if not unit.isheader():
            if len(unit.msgid):
                if unit.msgstr == [u'""']:
                    moves += 1
                    unit.msgstr = ['"%s"' % ms_get_translation(sl, tl, x) for x in unit.msgid]
        if not bool(moves % 50):
            print "Saving file..."
            openfile.save()
    openfile.save()


if __name__ == "__main__":

    if len(sys.argv) < 4 or \
            not os.path.exists(sys.argv[1]):
        sys.stderr.write("""
usage example: python autotranslate.py <lang.po> en fr
""")
        sys.exit(1)
    else:
        po_file = os.path.abspath(sys.argv[1])
        from_lang = sys.argv[2]
        to_lang = sys.argv[3]
        print('Translating %s to %s' % (from_lang, to_lang))
        translate_po(po_file, from_lang, to_lang)
        print('Translation done')
