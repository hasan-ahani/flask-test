# question 1
def unique_sort(data):
    unique_items = []
    for item in data:
      if item not in unique_items:
          unique_items.append(item)
    unique_items.sort()
    return unique_items

# question 2
def analyze_scores(scores):
    if not scores:
        return {"total_count": 0, "average_score": 0, "highest_score": 0}

    total_count = len(scores)
    average_score = sum(scores) / total_count
    highest_score = max(scores)

    return {
        "total_count": total_count,
        "average_score": average_score,
        "highest_score": highest_score
    }

# question 3
def count_words(sentence):
    words = sentence.split()
    word_counts = {}

    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    return word_counts

