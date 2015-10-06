import pysolr

import ckan.plugins.toolkit as toolkit
import pylons.config as config
from ckan.plugins.toolkit import BaseController
import json

class DataLinkedController(BaseController):
    # def graph(self):
    #     solr_url = config.get('solr_url', 'http://127.0.0.1:8983/solr')
    #     solr = pysolr.Solr(solr_url)
    #
    #
    #     package_list = toolkit.get_action('package_list')(context={}, data_dict={})
    #     rows = len(package_list)
    #
    #     organization_list = toolkit.get_action('organization_list')(context={}, data_dict={})
    #
    #     organization_tags = {}
    #
    #     for organization in organization_list:
    #         tags = dict()
    #
    #         results = solr.search(q='*:*', fl='tags', rows=rows, fq='organization: {}'.format(organization))
    #
    #         for result in results:
    #             if result.get('tags'):
    #                 for tag in result['tags']:
    #                     if tags.has_key(tag):
    #                         tags[tag] += 1
    #                     else:
    #                         tags[tag] = 1
    #
    #         tags = sorted(tags.items(), key=lambda t: t[1], reverse=True)
    #         organization_tags[organization] = tags
    #
    #     # return str(organization_tags)
    #     return toolkit.render('graph.html', extra_vars={'organization_tags': json.dumps(organization_tags, ensure_ascii=False, encoding='utf8')})
    #
    def stack_graph(self):
        solr_url = config.get('solr_url', 'http://127.0.0.1:8983/solr')
        solr = pysolr.Solr(solr_url)


        package_list = toolkit.get_action('package_list')(context={}, data_dict={})
        rows = len(package_list)

        organization_list = toolkit.get_action('organization_list')(context={}, data_dict={})

        # organization_tags = {}

        tags = dict()

        results = solr.search(q='*:*', fl='tags, organization', rows=rows)

        for result in results:
            if result.get('tags') and result.get('organization'):
                for tag in result['tags']:
                    if not tags.has_key(tag):
                        tags[tag] = {}
                        tags[tag]['sum'] = 0
                    if not tags[tag].has_key(result['organization']):
                        tags[tag][result['organization']] = 0
                    tags[tag][result['organization']] += 1
                    tags[tag]['sum'] += 1

        tags_ = sorted(tags.items(), key=lambda x: x[1]['sum'], reverse=True)
        tags = sorted(tags.items(), key=lambda x: x[1]['sum'], reverse=True)[:10]
        categories = [_[0] for _ in tags]
        # series = [for


        series = []
        for organization in organization_list:
            data = {
                'name': organization,
                'data': []
            }

            for tag in tags:
                if tag[1].has_key(organization):
                    data['data'].append(tag[1][organization])
                else:
                    data['data'].append(0)
            series.append(data)



        # return json.dumps(list(results), indent=4, ensure_ascii=False)
        # return json.dumps(series, indent=4, ensure_ascii=False)
        return toolkit.render('graph.html', extra_vars={
            'series': json.dumps(series, ensure_ascii=False),
            'categories': json.dumps(categories, ensure_ascii=False),
            'tags': json.dumps(tags_, ensure_ascii=False)
        })
