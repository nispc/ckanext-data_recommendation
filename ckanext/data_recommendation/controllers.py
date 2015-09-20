import jieba
import jieba.analyse

from ckan.plugins.toolkit import BaseController

class ApiController(BaseController):
    def extract(self, text):
        jieba.set_dictionary('/usr/lib/ckan/default/src/ckanext-data_recommendation/dict.txt.big')
        result = jieba.analyse.extract_tags(text, topK=5)
        result = [i.encode('utf8') for i in result]
        result = '[' + ','.join(result) + ']'
        return result