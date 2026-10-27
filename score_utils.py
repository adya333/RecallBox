
def normalize_scores(results):
    if not results:
        return []

    scores = [score for _, score in results]

    min_score = min(scores)
    max_score = max(scores)

    if max_score == min_score:
        return [
            (resource, 1.0)
            for resource, _ in results
        ]

    normalized = []

    for resource, score in results:
        normalized_score = (
            (score - min_score) /
            (max_score - min_score)
        )

        normalized.append(
            (resource, normalized_score)
        )

    return normalized
