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
    plugins.implements(plugins.IRoutes, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'data_recommendation')
        toolkit.add_resource('fanstatic', 'tag_cloud')
        toolkit.add_resource('fanstatic', 'stack_chart')
        toolkit.add_resource('fanstatic', 'jqcloud')


    @classmethod
    def related_pkgs(cls):
        # Parameter
        extractNum = int(config.get('ckan.data_recommended.extract_num', '5'))
        byTag = asbool(config.get('ckan.data_recommended.by_tag', 'true'))
        byTitle = asbool(config.get('ckan.data_recommended.by_title', 'true'))
        renderMod = 'front_end'

        # fetch pkg info
        pkg_name = request.environ['PATH_INFO'].split('/')[-1]
        pkg_title = toolkit.get_action('package_show')({}, {'id':pkg_name})['title']
        pkg_tags = [pkg_tag['name'] for pkg_tag in toolkit.get_action('package_show')({}, {'id':pkg_name})['tags']]

         # related_tag_titles
        related_tag_titles = set()
        if byTag:
            related_tag_titles.update(set(pkg_tags))

        if byTitle:
            tmp = jieba.analyse.extract_tags(pkg_title, topK=extractNum)
            related_tag_titles.update(
                set(
                    tmp
                )
            )

        related_pkgs = {}
        if renderMod == 'back_end':
            related_pkgs['mod'] = renderMod
            related_pkgs['results'] = dict()
            for related_tag_title in related_tag_titles:
                related_pkg_results = toolkit.get_action('package_search')({}, {'q': related_tag_title, 'rows': 3})['results']

                related_pkgs['results'][related_tag_title] = related_pkg_results

            return related_pkgs
        elif renderMod == 'front_end':
            related_pkgs['results'] = related_tag_titles
            related_pkgs['mod'] = renderMod
            return related_pkgs

    def get_helpers(self):
        return {'related_pkgs': self.related_pkgs}

    # IRoutes
    def before_map(self, map):
        controller = 'ckanext.data_recommendation.controllers:DataLinkedController'

        map.connect('data-linked-graph', '/linked-data',
            controller=controller, action='stack_graph')

        return map