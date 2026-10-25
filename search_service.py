
from sentence_transformers import util


class SearchService:

    def __init__(self, embedding_service, resources):
      self.embedding_service = embedding_service
      self.resources = resources

    def search(self, query, top_k=3, min_similarity=0.25):
      query_embedding = self.embedding_service.generate_embedding(query)

      results = []

      for resource in self.resources:
        if resource.embedding is None:
          continue
        score = util.cos_sim(
            query_embedding,
            resource.embedding
        ).item()

        results.append((resource, score))

      results.sort(key=lambda x:x[1], reverse=True)

      results = [
      (resource, score)
      for resource, score in results
       if score >= min_similarity
    ]

      return results[:top_k]
