from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(cv_text, job_text):
    documents = [cv_text, job_text]
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(similarity * 100, 2)
