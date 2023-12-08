from utils.env_loader import env
from elasticsearch import Elasticsearch

class ES_access:
    def __init__(self, name_index, name_doc="_doc", url="http://localhost:9200"):
        self.es = Elasticsearch(url)
        self.name_index = name_index
        self.name_doc = name_doc
    
    def query_cosine(self, unit_vector, tag_name_compare, top_n, collapse):
        if type(tag_name_compare) != list:
            tag_name_compare = [tag_name_compare]
            
        query = {
            "query": 
            {
                "function_score": 
                {
                    "query":
                    {
                        "terms": {"tag": tag_name_compare}
                    },
                
                    "functions": 
                    [
                        {
                            "script_score": 
                            {
                                "script": 
                                {
                                    "source": "cosineSimilarity(params.query_vector, 'features')/2+0.5",
                                    "params": {"query_vector": unit_vector}  # Replace with your query vector
                                }
                            }
                        }
                    ], 
                    "boost_mode": "replace"
                }
            },
            
            "_source": {"excludes": ["features"]},
            "size": top_n,
            "sort": 
            [
                {"_score": "desc"}
            ],
        }
        
        if collapse:
            query['collapse'] = {"field": "labels"}
        return query
        
    def search_in_elasticsearch(self, features, tag_name_compare=["train_split"], top_n=5, collapse=True):
        search_results = self.es.search(index=self.name_index, 
                                        body=self.query_cosine(
                                            features, 
                                            tag_name_compare=tag_name_compare, 
                                            top_n=top_n, 
                                            collapse=collapse))
        return search_results["hits"]["hits"]