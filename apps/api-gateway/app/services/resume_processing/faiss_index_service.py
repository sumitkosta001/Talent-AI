"""Phase 4 — Day 32: FAISS Vector Indexing and Similarity Search Service.

Provides a robust, persistent FAISS vector indexing and similarity search layer
supporting separate indices for Resumes and Jobs, L2-normalized inner-product
cosine similarity, deterministic ID mapping, vector validation, duplicate updates,
and persistence.
"""

import json
import logging
import os
import time
import hashlib
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union
import numpy as np

try:
    import faiss  # type: ignore
except ImportError:
    faiss: Any = None


from app.config.settings import settings
from app.services.resume_processing.models import (
    StructuredResume,
    JobRequirements,
    FAISSIndexResult,
    FAISSSearchItem,
    FAISSSearchResult,
)
from app.services.resume_processing.embedding_service import (
    build_resume_embedding_text,
    build_job_embedding_text,
    generate_embedding,
    normalize_similarity_score,
    get_similarity_tier,
)

logger = logging.getLogger(__name__)

# Process-wide singleton locks and instances
_resume_index_instance: Optional["FAISSVectorIndex"] = None
_job_index_instance: Optional["FAISSVectorIndex"] = None
_index_lock = threading.Lock()


def string_to_int64_id(entity_id: Union[str, Any]) -> int:
    """Converts string/int/UUID entity_id into a positive 63-bit int64 FAISS ID."""
    if entity_id is None:
        raise ValueError("entity_id cannot be None.")
    str_id = str(entity_id).strip()
    if not str_id:
        raise ValueError("entity_id cannot be empty.")
    digest = hashlib.sha256(str_id.encode("utf-8")).digest()
    int_id = int.from_bytes(digest[:8], byteorder="big", signed=False) & 0x7FFFFFFFFFFFFFFF
    return int_id


# Helper wrappers for FAISS C-extension methods (suppresses static type checker missing-attribute warnings)

def _faiss_read_index(file_path: str) -> Any:
    return faiss.read_index(file_path)  # type: ignore


def _faiss_write_index(index: Any, file_path: str) -> None:
    faiss.write_index(index, file_path)  # type: ignore


def _faiss_create_flat_ip(dimension: int) -> Any:
    return faiss.IndexFlatIP(dimension)  # type: ignore


def _faiss_create_id_map2(base_index: Any) -> Any:
    return faiss.IndexIDMap2(base_index)  # type: ignore


def _faiss_normalize_L2(vec_copy: np.ndarray) -> None:
    faiss.normalize_L2(vec_copy)  # type: ignore


def _faiss_remove_ids(index: Any, remove_arr: np.ndarray) -> int:
    return index.remove_ids(remove_arr)  # type: ignore


def _faiss_add_with_ids(index: Any, vec_2d: np.ndarray, ids_arr: np.ndarray) -> None:
    index.add_with_ids(vec_2d, ids_arr)  # type: ignore


def _faiss_search(index: Any, norm_query: np.ndarray, actual_k: int) -> Tuple[np.ndarray, np.ndarray]:
    return index.search(norm_query, actual_k)  # type: ignore


def _faiss_get_ntotal(index: Any) -> int:
    if index is None:
        return 0
    return getattr(index, "ntotal", 0)  # type: ignore


class FAISSVectorIndex:
    """Generic FAISS Vector Index Wrapper using IndexIDMap2 + IndexFlatIP.

    Uses L2-normalized float32 vectors so inner product equals exact cosine similarity.
    Provides persistence, vector validation, ID mapping, updates, and similarity search.
    """

    def __init__(
        self,
        index_name: str,
        index_dir: Optional[Union[str, Path]] = None,
        dimension: Optional[int] = None,
        index_type: str = "FLAT_IP",
    ):
        if faiss is None:
            raise RuntimeError(
                "faiss-cpu package is not installed. Please install faiss-cpu."
            )

        self.index_name = index_name
        raw_dir = index_dir or getattr(settings.faiss, "index_dir", "data/faiss")
        self.index_dir = Path(raw_dir).resolve()
        self.dimension = dimension or getattr(settings.faiss, "embedding_dimension", 384)
        if self.dimension <= 0:
            raise ValueError(f"FAISS embedding dimension must be > 0, got {self.dimension}")

        self.index_type = index_type or getattr(settings.faiss, "index_type", "FLAT_IP")

        self.index_file_path = self.index_dir / self.index_name
        self.metadata_file_path = self.index_dir / f"{self.index_name}.metadata.json"

        self._lock = threading.Lock()
        self.index: Any = None
        self.id_to_entity_map: Dict[str, str] = {}  # str(int_id) -> string entity_id
        self.entity_metadata_map: Dict[str, Dict[str, Any]] = {}  # entity_id -> dict

        self.load_or_create()

    def load_or_create(self) -> None:
        """Loads index and metadata from disk if present, else initializes clean empty index."""
        with self._lock:
            self.index_dir.mkdir(parents=True, exist_ok=True)

            if self.index_file_path.exists():
                try:
                    logger.info("Loading FAISS index from disk: %s", self.index_file_path)
                    loaded_index = _faiss_read_index(str(self.index_file_path))
                    self.index = loaded_index
                    self._load_metadata()
                    logger.info(
                        "Successfully loaded FAISS index '%s' with %d vectors",
                        self.index_name,
                        _faiss_get_ntotal(self.index),
                    )
                    return
                except Exception as e:
                    logger.error(
                        "Failed to load FAISS index from '%s': %s. Initializing fresh index.",
                        self.index_file_path,
                        str(e),
                    )

            self.create_empty_index()

    def create_empty_index(self) -> None:
        """Initializes a new empty IndexIDMap2(IndexFlatIP(dimension))."""
        base_index = _faiss_create_flat_ip(self.dimension)
        self.index = _faiss_create_id_map2(base_index)
        self.id_to_entity_map = {}
        self.entity_metadata_map = {}
        self.save()
        logger.info("Created empty FAISS index '%s' (dim=%d)", self.index_name, self.dimension)

    def save(self) -> None:
        """Persists FAISS index binary and metadata JSON to disk."""
        if self.index is None:
            return

        self.index_dir.mkdir(parents=True, exist_ok=True)
        try:
            _faiss_write_index(self.index, str(self.index_file_path))
            self._save_metadata()
            logger.debug("Persisted FAISS index '%s' (%d vectors)", self.index_name, _faiss_get_ntotal(self.index))
        except Exception as e:
            logger.error("Failed to persist FAISS index '%s': %s", self.index_name, str(e))
            raise RuntimeError(f"FAISS index persistence failure for '{self.index_name}': {str(e)}") from e

    def _save_metadata(self) -> None:
        payload = {
            "dimension": self.dimension,
            "index_type": self.index_type,
            "id_to_entity_map": self.id_to_entity_map,
            "entity_metadata_map": self.entity_metadata_map,
            "updated_at": time.time(),
        }
        with open(self.metadata_file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def _load_metadata(self) -> None:
        if not self.metadata_file_path.exists():
            self.id_to_entity_map = {}
            self.entity_metadata_map = {}
            return

        try:
            with open(self.metadata_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.id_to_entity_map = data.get("id_to_entity_map", {})
                self.entity_metadata_map = data.get("entity_metadata_map", {})
        except Exception as e:
            logger.warning("Could not parse FAISS metadata file '%s': %s", self.metadata_file_path, str(e))
            self.id_to_entity_map = {}
            self.entity_metadata_map = {}

    def validate_vector(self, vector: np.ndarray) -> np.ndarray:
        """Validates vector array dimension, numeric type, and finite values."""
        if vector is None:
            raise ValueError("Input vector embedding cannot be None.")

        if not isinstance(vector, np.ndarray):
            try:
                vector = np.array(vector, dtype=np.float32)
            except Exception as e:
                raise ValueError(f"Input vector is not a valid numeric array: {str(e)}")

        if not np.issubdtype(vector.dtype, np.number):
            raise ValueError("Input vector must contain numeric elements.")

        if vector.ndim > 1:
            vector = vector.flatten()

        if vector.size != self.dimension:
            raise ValueError(
                f"Vector dimension mismatch for FAISS index '{self.index_name}': "
                f"Expected dimension {self.dimension}, received vector of size {vector.size}."
            )

        if not np.all(np.isfinite(vector)):
            raise ValueError(
                f"Input vector for FAISS index '{self.index_name}' contains NaN or Inf values."
            )

        return vector.astype(np.float32)

    def normalize_vector(self, vector: np.ndarray) -> np.ndarray:
        """Validates and L2-normalizes vector array."""
        vec = self.validate_vector(vector)
        vec_copy = vec.copy().reshape(1, -1)
        _faiss_normalize_L2(vec_copy)
        return vec_copy.flatten().astype(np.float32)

    def add(
        self,
        vector: np.ndarray,
        entity_id: Union[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Adds or updates an L2-normalized vector for entity_id."""
        str_entity_id = str(entity_id).strip()
        if not str_entity_id:
            raise ValueError("entity_id cannot be empty.")

        norm_vec = self.normalize_vector(vector)
        int_id = string_to_int64_id(str_entity_id)

        with self._lock:
            if self.index is None:
                self.create_empty_index()

            # Handle duplicate update by removing existing vector if present
            if str(int_id) in self.id_to_entity_map or str_entity_id in self.entity_metadata_map:
                try:
                    remove_arr = np.array([int_id], dtype=np.int64)
                    _faiss_remove_ids(self.index, remove_arr)
                    logger.debug("Removed pre-existing vector for entity '%s' (int_id=%d)", str_entity_id, int_id)
                except Exception as rem_err:
                    logger.warning("Minor warning during pre-existing vector removal: %s", str(rem_err))

            # Add normalized vector to FAISS index with ID
            vec_2d = norm_vec.reshape(1, -1)
            ids_arr = np.array([int_id], dtype=np.int64)
            _faiss_add_with_ids(self.index, vec_2d, ids_arr)

            # Record metadata mappings
            self.id_to_entity_map[str(int_id)] = str_entity_id
            self.entity_metadata_map[str_entity_id] = metadata or {}

            self.save()
            ntotal = _faiss_get_ntotal(self.index)
            logger.info(
                "Indexed vector for '%s' into '%s' (total vectors: %d)",
                str_entity_id,
                self.index_name,
                ntotal,
            )
            return ntotal

    def remove(self, entity_id: Union[str, Any]) -> bool:
        """Removes vector for entity_id from index."""
        if entity_id is None:
            return False
        str_entity_id = str(entity_id).strip()
        if not str_entity_id:
            return False

        int_id = string_to_int64_id(str_entity_id)

        with self._lock:
            if self.index is None:
                return False

            str_int_id = str(int_id)
            found = str_int_id in self.id_to_entity_map or str_entity_id in self.entity_metadata_map

            if found:
                try:
                    remove_arr = np.array([int_id], dtype=np.int64)
                    _faiss_remove_ids(self.index, remove_arr)
                except Exception as e:
                    logger.error("FAISS removal error for entity '%s': %s", str_entity_id, str(e))

                self.id_to_entity_map.pop(str_int_id, None)
                self.entity_metadata_map.pop(str_entity_id, None)
                self.save()
                logger.info("Removed vector for entity '%s' from '%s'", str_entity_id, self.index_name)
                return True

            return False

    def search(
        self,
        query_vector: np.ndarray,
        top_k: int = 10,
        query_type: str = "vector_search",
    ) -> FAISSSearchResult:
        """Performs top-k inner product (cosine similarity) search on FAISS index."""
        start_time = time.time()

        if top_k is None or not isinstance(top_k, int) or top_k <= 0:
            raise ValueError(f"top_k must be a positive integer > 0, received {top_k}.")
        if top_k > 10000:
            raise ValueError(f"top_k cannot exceed 10,000, received {top_k}.")

        # Always validate and normalize query vector FIRST before checking empty state
        norm_query = self.normalize_vector(query_vector).reshape(1, -1)

        total_vecs = _faiss_get_ntotal(self.index)
        # Handle search on empty index gracefully
        if self.index is None or total_vecs == 0:
            return FAISSSearchResult(
                query_type=query_type,
                total_results=0,
                top_k=top_k,
                results=[],
                execution_time_ms=round((time.time() - start_time) * 1000, 2),
                metadata={"status": "empty_index", "vector_count": 0},
            )

        actual_k = min(top_k, total_vecs)
        distances, ids = _faiss_search(self.index, norm_query, actual_k)

        items: List[FAISSSearchItem] = []
        raw_sims = distances[0]
        match_ids = ids[0]

        for raw_sim, idx_id in zip(raw_sims, match_ids):
            if idx_id == -1:
                continue

            str_int_id = str(idx_id)
            entity_id = self.id_to_entity_map.get(str_int_id, f"unknown_id_{idx_id}")
            entity_meta = self.entity_metadata_map.get(entity_id, {})

            cosine_sim = float(np.clip(raw_sim, -1.0, 1.0))
            score = normalize_similarity_score(cosine_sim)
            tier = get_similarity_tier(score)

            items.append(
                FAISSSearchItem(
                    entity_id=entity_id,
                    raw_similarity=round(cosine_sim, 4),
                    similarity_score=score,
                    similarity_tier=tier,
                    metadata=entity_meta,
                )
            )

        exec_ms = round((time.time() - start_time) * 1000, 2)
        return FAISSSearchResult(
            query_type=query_type,
            total_results=len(items),
            top_k=top_k,
            results=items,
            execution_time_ms=exec_ms,
            metadata={
                "index_name": self.index_name,
                "dimension": self.dimension,
                "total_vectors_in_index": total_vecs,
            },
        )

    def count(self) -> int:
        """Returns total vector count in index."""
        return _faiss_get_ntotal(self.index)

    def is_loaded(self) -> bool:
        """Returns True if index is loaded and valid."""
        return self.index is not None

    def get_entity_ids(self) -> List[str]:
        """Returns list of all indexed entity IDs."""
        return list(self.entity_metadata_map.keys())

    def rebuild(self) -> None:
        """Clears and re-initializes empty index."""
        with self._lock:
            self.create_empty_index()


# Process-wide Singleton Accessors

def get_resume_faiss_index() -> FAISSVectorIndex:
    """Gets process-wide singleton FAISSVectorIndex for Resumes."""
    global _resume_index_instance
    if _resume_index_instance is None:
        with _index_lock:
            if _resume_index_instance is None:
                _resume_index_instance = FAISSVectorIndex(
                    index_name=getattr(settings.faiss, "resume_index_name", "resumes.index"),
                    index_dir=getattr(settings.faiss, "index_dir", "data/faiss"),
                    dimension=getattr(settings.faiss, "embedding_dimension", 384),
                    index_type=getattr(settings.faiss, "index_type", "FLAT_IP"),
                )
    return _resume_index_instance


def get_job_faiss_index() -> FAISSVectorIndex:
    """Gets process-wide singleton FAISSVectorIndex for Jobs."""
    global _job_index_instance
    if _job_index_instance is None:
        with _index_lock:
            if _job_index_instance is None:
                _job_index_instance = FAISSVectorIndex(
                    index_name=getattr(settings.faiss, "job_index_name", "jobs.index"),
                    index_dir=getattr(settings.faiss, "index_dir", "data/faiss"),
                    dimension=getattr(settings.faiss, "embedding_dimension", 384),
                    index_type=getattr(settings.faiss, "index_type", "FLAT_IP"),
                )
    return _job_index_instance


# High-Level Business Domain Indexing & Search API

def index_resume(
    resume_id: Union[str, Any],
    structured_resume: Union[StructuredResume, Dict[str, Any]],
    model_name: Optional[str] = None,
) -> FAISSIndexResult:
    """Generates Day 31 resume embedding and indexes it into the Resume FAISS index."""
    if resume_id is None:
        raise ValueError("resume_id cannot be None.")
    str_resume_id = str(resume_id).strip()
    if not str_resume_id:
        raise ValueError("resume_id cannot be empty.")

    if structured_resume is None:
        raise ValueError("structured_resume cannot be None.")
    if isinstance(structured_resume, dict):
        structured_resume = StructuredResume.model_validate(structured_resume)
    elif not isinstance(structured_resume, StructuredResume):
        raise ValueError("structured_resume must be an instance of StructuredResume or valid dict.")

    text = build_resume_embedding_text(structured_resume)
    embedding = generate_embedding(text, model_name=model_name)

    resume_index = get_resume_faiss_index()
    meta = {
        "full_name": structured_resume.full_name,
        "email": structured_resume.email,
        "domain": structured_resume.classification.domain if structured_resume.classification else None,
        "role": getattr(structured_resume.classification, "primary_role", getattr(structured_resume.classification, "role", None)) if structured_resume.classification else None,
        "text_length": len(text),
        "indexed_at": time.time(),
    }
    total_count = resume_index.add(embedding, str_resume_id, metadata=meta)

    return FAISSIndexResult(
        entity_id=str_resume_id,
        entity_type="resume",
        indexed=True,
        dimension=resume_index.dimension,
        index_type=resume_index.index_type,
        vector_count=total_count,
        metadata=meta,
    )


def index_job(
    job_id: Union[str, Any],
    job_requirements: Union[JobRequirements, Dict[str, Any]],
    model_name: Optional[str] = None,
) -> FAISSIndexResult:
    """Generates Day 31 job embedding and indexes it into the Job FAISS index."""
    if job_requirements is None:
        raise ValueError("job_requirements cannot be None.")
    if isinstance(job_requirements, dict):
        job_requirements = JobRequirements.model_validate(job_requirements)
    elif not isinstance(job_requirements, JobRequirements):
        raise ValueError("job_requirements must be an instance of JobRequirements or valid dict.")

    raw_id = job_id or job_requirements.job_id or f"job_{time.time()}"
    str_job_id = str(raw_id).strip()
    if not str_job_id:
        raise ValueError("job_id cannot be empty.")

    text = build_job_embedding_text(job_requirements)
    embedding = generate_embedding(text, model_name=model_name)

    job_index = get_job_faiss_index()
    meta = {
        "title": job_requirements.title,
        "required_skills": job_requirements.required_skills,
        "required_domains": job_requirements.required_domains,
        "text_length": len(text),
        "indexed_at": time.time(),
    }
    total_count = job_index.add(embedding, str_job_id, metadata=meta)

    return FAISSIndexResult(
        entity_id=str_job_id,
        entity_type="job",
        indexed=True,
        dimension=job_index.dimension,
        index_type=job_index.index_type,
        vector_count=total_count,
        metadata=meta,
    )


def remove_resume_index(resume_id: Union[str, Any]) -> bool:
    """Removes candidate resume from Resume FAISS index."""
    resume_index = get_resume_faiss_index()
    return resume_index.remove(resume_id)


def remove_job_index(job_id: Union[str, Any]) -> bool:
    """Removes job requirements from Job FAISS index."""
    job_index = get_job_faiss_index()
    return job_index.remove(job_id)


def search_jobs_for_resume(
    structured_resume: Union[StructuredResume, Dict[str, Any]],
    top_k: int = 10,
    model_name: Optional[str] = None,
) -> FAISSSearchResult:
    """Uses candidate resume embedding to search Job FAISS index for top-k matching jobs."""
    if structured_resume is None:
        raise ValueError("structured_resume cannot be None.")
    if isinstance(structured_resume, dict):
        structured_resume = StructuredResume.model_validate(structured_resume)
    elif not isinstance(structured_resume, StructuredResume):
        raise ValueError("structured_resume must be an instance of StructuredResume or valid dict.")

    text = build_resume_embedding_text(structured_resume)
    query_vec = generate_embedding(text, model_name=model_name)
    job_index = get_job_faiss_index()
    return job_index.search(query_vec, top_k=top_k, query_type="resume_to_jobs")


def search_resumes_for_job(
    job_requirements: Union[JobRequirements, Dict[str, Any]],
    top_k: int = 10,
    model_name: Optional[str] = None,
) -> FAISSSearchResult:
    """Uses job requirements embedding to search Resume FAISS index for top-k matching candidate resumes."""
    if job_requirements is None:
        raise ValueError("job_requirements cannot be None.")
    if isinstance(job_requirements, dict):
        job_requirements = JobRequirements.model_validate(job_requirements)
    elif not isinstance(job_requirements, JobRequirements):
        raise ValueError("job_requirements must be an instance of JobRequirements or valid dict.")

    text = build_job_embedding_text(job_requirements)
    query_vec = generate_embedding(text, model_name=model_name)
    resume_index = get_resume_faiss_index()
    return resume_index.search(query_vec, top_k=top_k, query_type="job_to_resumes")
