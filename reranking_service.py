
from sentence_transformers import CrossEncoder

class RerankingService:
  def __init__(self):
    self.model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

  def reranking(self, query, resources):
    pairs = [[query, resource.raw_text]
             for resource in resources
             ]
    scores = self.model.predict(pairs)

    reranked_results = list(zip(resources, scores))
    reranked_results.sort(
      key=lambda item: item[1],
      reverse=True
      )

    return reranked_results
