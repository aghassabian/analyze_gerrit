from perceval.backends.core.gerrit import Gerrit
import elasticsearch


repo_url = ''
repo_dir = '/tmp/gerrit'
repo_user = ''
es = elasticsearch.Elasticsearch(['http://localhost:9200'])

try:
    es.indices.create('gerrit')
except:
    es.indices.delete('gerrit')
    es.indices.create('gerrit')

repo = Gerrit(url=repo_url, user=repo_user,max_reviews=100)

for commit in repo.fetch():
    enriched = {
        'project': commit['data']['project'],
        'branch': commit['data']['branch'],
        'owner': commit['data']['owner']['name'],
        'url': commit['data']['url'],
        'createdon': commit['data']['createdOn'],
        'last_update': commit['data']['lastUpdated'],
        'is_open': commit['data']['open'],
        'status': commit['data']['status'],
        'user_comment': commit['data']['comments']['reviewer']['name'],
        'patchset_number': commit['data']['patchSets']['number'],
        'patchset_uploader': commit['data']['patchSets']['uploader']['name'],
        'patchset_createdon': commit['data']['patchset']['createdOn'],
        'patchset_insert': commit['data']['patchset']['sizeInsertions'],
        'patchset_delete': commit['data']['patchset']['sizeDeletions']

    }
    print(test_summary)

    es.index(index='gerrit',doc_type='gerrit',body=enriched)

