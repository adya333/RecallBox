
from sentence_transformers import util


class SearchService:

    def __init__(self, embedding_service, resources):
      self.embedding_service = embedding_service
      self.resources = resources

    def search(self, query):
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

      return results
