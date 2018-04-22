import QuillLanguage as qlang
import fire


class Data(object):

    def __init__(self):
        '''
        Init
        '''
        languages = {
            'bengali': 'Vrinda',
            'gujarati': 'Shruti',
            'hindi': 'Mangal',
            'kannada': 'Tunga',
            'malayalam': 'Kartika',
            'marathi': 'Mangal',
            'nepali': 'Mangal',
            'punjabi': 'Raavi',
            'tamil': 'Latha',
            'telugu': 'Raavi'
        }

        language_new = {
            lang: 'langdef/' + lang + '/' + lang[0].upper() + lang[1:] + '_New' + '.xml' for lang in languages
        }

        language_words = {
            lang: 'langdef/' + lang + '/unique_' + lang.lower() + '_words' + '.txt' for lang in languages
        }

        language_definition = {
            lang: 'langdef/' + lang + '/' + lang[0].upper() + lang[1:] + '_' + lang_type + '.xml' for lang, lang_type in languages.items()
        }

        language_knowledge = {
            lang: 'knowledge/' + lang for lang in languages\
        }

        language_xlit = {
            lang: 'langdef/' + lang + '/' + lang[0].upper() + lang[1:] + '_Xlit.xml'\
                for lang in languages
        }

        unique_words_map = {
            lang: dict([(line.split('\t')[0].decode('utf-8'), 1) for line in open(language_words[lang], 'r').readlines()])
                for lang in languages
        }

        # Load the hindi dictionary
        hindi_update = unique_words_map['hindi']
        for line in open('langdef/hindi/HindiDictionary.txt').readlines():
            hindi_update[line.strip().decode('utf-8')] = 1


        def makeClashMap(fname):
            words = open(fname).read().split()
            return dict([(w, None) for w in words])

        clash_maps = {
            lang: makeClashMap('langdef/{lang}/{lang}Clash.txt'.format(lang=lang)) for lang in languages
        }

        english_dictionary_file_name = 'langdef/english/dictionary.txt'
        english_dictionary = dict([(w, None) for w in open(english_dictionary_file_name).read().split()])

        self.languages = languages
        self.language_new = language_new
        self.language_words = language_words
        self.language_definition = language_definition
        self.language_knowledge = language_knowledge
        self.language_xlit = language_xlit
        self.unique_words_map = unique_words_map
        self.clash_maps = clash_maps
        self.english_dictionary = english_dictionary

data = Data()
