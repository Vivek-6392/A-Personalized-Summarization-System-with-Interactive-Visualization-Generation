# import chromadb
# from sentence_transformers import SentenceTransformer

# class VectorDB:
#     def __init__(self, persist_path=None, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        
#         # Load SentenceTransformer model
#         self.model = SentenceTransformer(model_name)
        
#         # Connect to Chroma
#         if persist_path:
#             self.client = chromadb.PersistentClient(path=persist_path)
#         else:
#             self.client = chromadb.Client()

#         # Delete existing collection to avoid dimension mismatch
#         try:
#             self.client.delete_collection("doc_chunks")
#         except:
#             pass

#         # Create new collection
#         self.coll = self.client.get_or_create_collection(
#             name="doc_chunks",
#             metadata={"hnsw:space": "cosine"}
#         )

#     def _embed(self, texts):
#         """Generate embeddings using SentenceTransformer."""
#         return self.model.encode(texts).tolist()

#     def add_chunks(self, chunks_dict):
#         """Add text chunks to vector DB."""
#         texts = list(chunks_dict.values())
#         ids = [str(i) for i in range(len(texts))]
#         metadatas = [{"section": sec} for sec in chunks_dict.keys()]
        
#         embeddings = self._embed(texts)

#         self.coll.add(
#             documents=texts,
#             metadatas=metadatas,
#             ids=ids,
#             embeddings=embeddings
#         )

#     def search(self, query, top_k=5):
#         """Semantic search"""
#         embedding = self._embed([query])
        
#         results = self.coll.query(query_embeddings=embedding, n_results=top_k)
#         return results["documents"], results.get("metadatas")

import chromadb
from sentence_transformers import SentenceTransformer
import torch

class VectorDB:
    def __init__(self, persist_path=None, model_name="sentence-transformers/all-MiniLM-L6-v2"):

        # ---- Fix: Safe device detection ----
        if torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"

        print(f"[VectorDB] Loading embedding model on: {device}")

        try:
            self.model = SentenceTransformer(model_name, device=device)
        except NotImplementedError:
            # Fallback for meta tensor issue
            print("[Warning] Meta tensor issue detected. Loading on CPU.")
            self.model = SentenceTransformer(model_name, device="cpu")

        # ---- Chroma Client ----
        if persist_path:
            self.client = chromadb.PersistentClient(path=persist_path)
        else:
            self.client = chromadb.Client()

        # ---- Reset or Load Collection ----
        try:
            self.client.delete_collection("doc_chunks")
        except Exception:
            pass

        self.coll = self.client.get_or_create_collection(
            name="doc_chunks",
            metadata={"hnsw:space": "cosine"}
        )

    def _embed(self, texts):
        """Generate embeddings using SentenceTransformer (Torch no_grad for speed)."""
        with torch.no_grad():
            return self.model.encode(texts).tolist()

    def add_chunks(self, chunks_dict):
        """Add text chunks to vector DB."""
        texts = list(chunks_dict.values())
        ids = [str(i) for i in range(len(texts))]
        metadatas = [{"section": sec} for sec in chunks_dict.keys()]

        embeddings = self._embed(texts)

        self.coll.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )

    def search(self, query, top_k=5):
        """Semantic search."""
        embedding = self._embed([query])

        results = self.coll.query(
            query_embeddings=embedding,
            n_results=top_k
        )
        return results.get("documents"), results.get("metadatas")
