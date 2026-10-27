
# Will normalize score to be <1 later

class HybridSearchService:

  def __init__(self, search_service, lexical_search_service):
    self.search_service = search_service
    self.lexical_search_service = lexical_search_service

  def search(self, query, top_k = 3, min_score=0.2):
    semantic_results = self.search_service.search(query, 
                                                  top_k=10,
                                                  min_similarity=0.0)
    lexical_results = self.lexical_search_service.search(query, top_k = 10)
    combined = {}

    for resource, score in semantic_results:
      combined[resource.resource_id] = {
          "resource":resource,
          "semantic_score":score,
          "lexical_score":0.0
      }

    for resource, score in lexical_results:

            if resource.resource_id not in combined:
                combined[resource.resource_id] = {
                    "resource": resource,
                    "semantic_score": 0.0,
                    "lexical_score": score
                }
            else:
                combined[resource.resource_id]["lexical_score"] = score
    
    results = []

    for item in combined.values():
      final_score = ( 0.5 * item["semantic_score"] +
                0.5 * item["lexical_score"])
      results.append((item["resource"], final_score))

    results = [
    (resource, score)
    for resource, score in results
    if score >= min_score
]
    results.sort(key=lambda x:x[1], reverse=True)
    return results[:top_k]

    
      
