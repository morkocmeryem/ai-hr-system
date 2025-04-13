from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise

def train_and_match(cv_texts, job_descriptions):
    results = []

    vectorizer = TfidfVectorizer()
    all_docs = job_descriptions + cv_texts
    tfidf_matrix = vectorizer.fit_transform(all_docs)

    job_vecs = tfidf_matrix[:len(job_descriptions)]
    cv_vecs = tfidf_matrix[len(job_descriptions):]

    for i, job_vec in enumerate(job_vecs):
        scores = pairwise.cosine_similarity(job_vec, cv_vecs)[0]
        result_for_job = sorted(
            list(enumerate(scores)), key=lambda x: x[1], reverse=True)
        results.append({
            "job_id": i,
            "matches": result_for_job
        })

    return results
