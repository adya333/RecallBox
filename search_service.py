
from sentence_transformers import util


class SearchService:

    def __init__(self, embedding_service, resources, qdrant_service):
      self.embedding_service = embedding_service
      self.resources = resources
      self.qdrant_service=qdrant_service

    def search(self, query, top_k=3, min_similarity=0.25):
      query_embedding = self.embedding_service.generate_embedding(query)
      
      matches = self.qdrant_service.search(query_embedding, 
                                           limit=len(self.resources))
      resource_lookup = {
        resource.resource_id: resource
        for resource in self.resources
      }                               
      results = []
      for resource_id, score in matches:
        resource = resource_lookup.get(resource_id)

        if resource:
          results.append((resource, score))
      return results
          

      
