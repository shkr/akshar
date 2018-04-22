import fire
from QuillLanguage import QuillLanguage
from get_data import data

class App(object):

  def transform(self, language, word):
    lang_object = QuillLanguage(data.language_definition[language], data.language_knowledge[language])
    result = lang_object.strToUnicode(word)
    for item in result:
        print(''.join(item))
    return True

if __name__=='__main__':
  fire.Fire(App)
