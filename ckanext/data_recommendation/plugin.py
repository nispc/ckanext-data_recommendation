import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.plugins.toolkit import asbool
import jieba
import jieba.analyse
from ckan.plugins.toolkit import request, c
import pylons.config as config

class Data_RecommendationPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'data_recommendation')

    @classmethod
    def related_pkgs(cls):
        # Parameter
        extractNum = int(config.get('ckan.data_recommended.extract_num', '5'))
        byTag = asbool(config.get('ckan.data_recommended.by_tag', 'true'))
        byTitle = asbool(config.get('ckan.data_recommended.by_title', 'true'))
        jiebaDictPath = config.get('ckan.data_recommended.jieba_dict_path', '/usr/lib/ckan/default/src/ckanext-data_recommendation/dict.txt.big')

        # fetch pkg info
        pkg_name = request.environ['PATH_INFO'].split('/')[-1]
        pkg_title = toolkit.get_action('package_show')({}, {'id':pkg_name})['title']
        pkg_tags = [pkg_tag['name'] for pkg_tag in toolkit.get_action('package_show')({}, {'id':pkg_name})['tags']]

        # fetch related pkg
        related_tag_titles = {}
        if byTag:
            related_tag_titles.update(set(pkg_tags))

        if byTitle:
            jieba.set_dictionary(jiebaDictPath)
            related_tag_titles.update(
                set(
                    jieba.analyse.extract_tags(pkg_title, topK=extractNum)
                )
            )
        related_pkgs = dict()
        for related_tag_title in related_tag_titles:
            related_pkg_results = toolkit.get_action('package_search')({}, {'q': related_tag_title, 'rows': 3})['results']

            related_pkgs[related_tag_title] = related_pkg_results

        return related_pkgs

    def get_helpers(self):
        return {'related_pkgs': self.related_pkgs}
