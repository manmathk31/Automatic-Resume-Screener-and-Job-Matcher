from typing import List, Dict

# Mocking Sentence-BERT logic until 'Manmath' integrates the real ML model
# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str) -> List[float]:
    \"\"\" Generate a dummy embedding vector for similarity computation \"\"\"
    # return model.encode(text).tolist()
    return [0.1, 0.2, 0.3, 0.4]

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    \"\"\" Compute cosine similarity. Mocked for now. \"\"\"
    # import numpy as np
    # return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    return 0.85

def rank_candidates(job_embedding: List[float], candidate_embeddings: Dict[int, List[float]]) -> Dict[int, float]:
    ranks = {}
    for cid, emb in candidate_embeddings.items():
        if emb:
            ranks[cid] = cosine_similarity(job_embedding, emb)
        else:
            ranks[cid] = 0.0
    # Sort descending
    sorted_ranks = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)}
    return sorted_ranks
