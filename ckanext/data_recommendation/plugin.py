import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import jieba
import jieba.analyse
from ckan.plugins.toolkit import request, c
import os

class Data_RecommendationPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'data_recommendation')

    '''@classmethod
    def pkg_title(cls):
        pkg_name = request.environ['PATH_INFO'].split('/')[-1]
        pkg_title = toolkit.get_action('package_show')({}, {'id':pkg_name})['title']
        jieba.set_dictionary('dict.txt.big')
        pkg_title = jieba.analyse.extract_tags(pkg_title, topK=5)
        return pkg_title'''

    @classmethod
    def related_pkgs(cls):
        extract_tags_num = 5

        pkg_name = request.environ['PATH_INFO'].split('/')[-1]
        pkg_title = toolkit.get_action('package_show')({}, {'id':pkg_name})['title']

        jieba.set_dictionary('dict.txt.big')
        related_tag_titles = jieba.analyse.extract_tags(pkg_title, topK=extract_tags_num)

        related_pkgs = {}
        for related_tag_title in related_tag_titles:
            related_pkg_results = toolkit.get_action('package_search')({}, {'q': related_tag_title})['results']

            related_pkgs[related_tag_title] = related_pkg_results

        return related_pkgs



    def get_helpers(self):
        return {'related_pkgs': self.related_pkgs}