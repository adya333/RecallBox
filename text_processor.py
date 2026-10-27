def similarity(text1, text2):
    words1 = set(tokenize(text1))
    words2 = set(tokenize(text2))

    common_words = words1.intersection(words2)

    return common_words


def tokenize(text):
    text = text.lower()
    words = text.split()
    return words


def build_vocabulary(texts):
    vocabulary = set()

    for text in texts:
        words = tokenize(text)
        vocabulary.update(words)

    return sorted(vocabulary)


# Bag of Words (BoW) converts text into numbers because ML algorithms work with
# numerical data. First, we create a common vocabulary containing all unique
# words from our texts. Each word gets a fixed position in that vocabulary.
# For example, if vocabulary = ["authentication", "security", "spring", "user"],
# then every vector follows exactly this order. We then count how many times
# each vocabulary word occurs in a text. So "Spring Security Security" becomes
# [0, 2, 1, 0]. The values are therefore word frequencies, not simply 0s and 1s.
# Using the SAME vocabulary for every text is important because each vector
# position must always represent the same word. This numerical representation
# lets us later mathematically compare texts using methods like cosine similarity.
def vectorize(text, vocabulary):
    words = tokenize(text)
    vector = []

    for word in vocabulary:
        count = words.count(word)
        vector.append(count)

    return vector

# text1 = ["Spring Security provides authentication",
#  "Spring Security handles user authentication fuck fuck"]

# vocabulary = build_vocabulary(text1)
# print(vocabulary)

# print(vectorize(text1[0], vocabulary))
# print(vectorize(text1[1], vocabulary))
