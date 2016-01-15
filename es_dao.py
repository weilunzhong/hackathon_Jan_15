from elasticsearch import Elasticsearch



def get_actor_freebase_id_by_name(name):
    server_address = '52.17.103.114:9200'
    es_client = Elasticsearch(server_address, timeout=50)
    index_type = 'artist'

    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "nested":
                        {
                            "path": "names",
                            "query":
                            {
                                "bool":
                                {
                                    "should": [
                                        {
                                            "match": {
                                                "names.value.standard": {
                                                    "query": name
                                                }
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        },
        "_source": "externalIDs.freebaseID",
        "size": 1
    }

    results = es_client.search(index=index_type, doc_type=index_type, body=query)
    results = results['hits']['hits']

    for row in results:
        row = row['_source']
        for _, field_value in row['externalIDs'].iteritems():
            if field_value:
                return '/' + field_value.replace('.', '/')


if __name__ == "__main__":
    print get_actor_freebase_id_by_name('brad pitt') 
