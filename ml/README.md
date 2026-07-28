# Machine Learning (ML) Engine

The `ml/` folder houses the components responsible for core data analytics, resume parsing, ATS screening models, semantic job matching embeddings, and recruitment recommendations.

## Directory Responsibilities

- **`parser/`**: Modules parsing resumes from PDFs/DOCX/Images into raw layout text.
- **`preprocessing/`**: Text normalizers, section segmenters, and regex cleaning pipelines.
- **`feature_engineering/`**: Vectorizers, TF-IDF weights, vocabulary mapping.
- **`skill_extraction/`**: NLP NER (Named Entity Recognition) extracting skills, experience, and educational markers.
- **`classifier/`**: Classifiers categorizing resumes into departments/domains.
- **`ats_engine/`**: Scoring algorithms, keywords alignment metrics, rule engines.
- **`embeddings/`**: Vectorizers based on sentence transformers converting text into semantic spaces.
- **`recommender/`**: FAISS similarity searching and matching candidate vectors against job specifications.
- **`training/`**: Training pipelines, model optimization scripts, hyperparameter adjustments.
- **`inference/`**: Serving models, lightweight local runtimes, pipeline packaging.
- **`models/`**: Placeholders for trained weights, serialized models (e.g. joblib, pickle, pt).
- **`datasets/`**: Reference text corpuses, training/test splits, benchmark data.
- **`notebooks/`**: Jupyter notebooks for exploratory data analysis, pipeline prototyping, and visualization.
- **`evaluation/`**: Accuracy evaluation, confusion matrices, custom score validators.
- **`utils/`**: Generic tokenizers, sentence splitters, ML-specific logging.
