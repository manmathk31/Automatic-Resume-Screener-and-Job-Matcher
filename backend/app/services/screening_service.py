import numpy as np
from typing import List, Dict
from ml_pipeline.embeddings.embedding_generator import generate_embedding
from ml_pipeline.ranking.similarity_engine import compute_similarity

def generate_embedding_real(text: str) -> List[float]:
    """ Uses ml_pipeline to generate an embedding for a job or text """
    embedding = generate_embedding(text)
    if embedding is not None:
        return embedding.tolist()
    return []

def rank_candidates_real(job_embedding_list: List[float], candidate_embeddings_dict: Dict[int, List[float]]) -> Dict[int, float]:
    """ Computes semantic similarity for each candidate relative to the job """
    ranks = {}
    job_emb_arr = np.array(job_embedding_list)
    for cid, emb_list in candidate_embeddings_dict.items():
        if emb_list and len(emb_list) == 384:
            cand_emb_arr = np.array(emb_list)
            score = compute_similarity(cand_emb_arr, job_emb_arr)
            # Clip between 0.0 and 1.0 just in case
            score = max(0.0, min(1.0, float(score)))
            ranks[cid] = score
        else:
            ranks[cid] = 0.0
            
    # Sort descending based on semantic score
    sorted_ranks = {k: v for k, v in sorted(ranks.items(), key=lambda item: item[1], reverse=True)}
    return sorted_ranks
