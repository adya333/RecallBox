
from rank_bm25 import BM25Okapi
from text_processor import tokenize


class LexicalSearchService:

    def __init__(self, resources):
        self.resources = resources

        tokenized_corpus = []

        for resource in resources:
            tokens = tokenize(resource.raw_text)
            tokenized_corpus.append(tokens)

        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query, top_k=3):
        query_tokens = tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        results = list(zip(self.resources, scores))

        results.sort(key=lambda x: x[1], reverse=True)

        return results[:top_k]
