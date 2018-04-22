# -*- coding: utf-8 -*-
# @Date    : Jul 13, 2016
# @Author  : Ram Prakash, Sharath Puranik
# @Version : 1

import QuillLanguage as qlang
import QuillEngXlit as xlit
from get_data import data
import re

class QuillSourceProcessor(object):
    """
    QuillSourceProcessor
    """
    def __init__(self):

        self.scriptEngines = {
                lang: qlang.QuillLanguage(data.language_definition[lang], data.language_knowledge[lang]) for lang in data.languages
        }

        self.xlitEngines = {
                lang: xlit.QuillEngXliterator('EnglishPronouncingTrees', 'IndianPronouncingTrees', data.language_xlit[lang])
                    for lang in data.languages
        }

        self.clashMaps = data.clash_maps

        self.modeTypes = ['predictive', 'xliterate', 'itrans']
        self.currLanguage = 'english'
        self.currMode = 'predictive'
        self.engine = None

    def sediment_non_unique_words(self, lang, arr):
        a1 = []
        a2 = []
        for word in arr:
            if data.unique_words_map[lang].has_key(word):
                a1.append(word)
            else:
                a2.append(word)
        return a1 + a2

    def setLanguage(self, script):
        if self.scriptEngines.has_key(script):
            self.engine = self.scriptEngines[script]
        else:
            self.engine = None

    def xlit(self, inString, lang):
        if lang in self.xlitEngines:
            inString = inString.lower()
            engine = self.xlitEngines[lang]
            return {'xlitWords': engine.xliterate(inString)}
        else:
            return {'xlitWords': [inString]}

    def processString(self, inString, lang):
        def transliterate(word):
            if re.search("[a-zA-Z]+", word):
                return self.processWord(word, lang)["twords"][0]["options"][0]
            return word

        words = map(lambda x: x[0], re.findall("(([a-zA-Z]+)|([^a-zA-Z])+)", inString))
        return "".join(map(transliterate, words))

    def processWord(self, inString, lang):

        if not isinstance(inString, str):
            raise ValueError("<type 'str'> only accepted as inString")

        for i in inString:
            if i in ".~^/" or i in "0123456789":
                raise ValueError("Cannot handle a word with non alphabets")

        inString = inString.lower()
        engine = self.scriptEngines[lang]

        options = engine.strToUnicode(inString)
        options = ["".join(item) for item in options]
        options = self.sediment_non_unique_words(lang, options)

        xlitWords = self.xlitEngines[lang].xliterate(inString)
        if len(xlitWords) > 0 and len(xlitWords[0]) > 0:
            xlitWord = xlitWords[0]
            if inString in data.english_dictionary:
                if inString in self.clashMaps[lang]:
                    if xlitWord not in options:
                        options = options[:1] + [xlitWord] + options[1:]
                else:
                    if xlitWord in options:
                        options.remove(xlitWord)
                    options = [xlitWord] + options
            else:
                if xlitWord not in options:
                    options = options + [xlitWord]
        return options

    def getCorrections(self, lang, currWord, userInput, pos):
        engine = self.scriptEngines[lang]
        return engine.getCorrections(currWord, userInput, pos)

    def getCorrectionsStr(self, lang, currWord, userInput, pos):
        engine = self.scriptEngines[lang]
        return engine.getCorrectionsStr(currWord, userInput, pos)


if __name__ == '__main__':

    proc = QuillSourceProcessor()

    res = proc.processWord("kaha", "punjabi")
    print('res', res)
    print("".join(res['twords'][0]['options']))

    res = proc.processWord("kaha", "hindi")
    print('res', res)
    print("".join(res['twords'][0]['options']))