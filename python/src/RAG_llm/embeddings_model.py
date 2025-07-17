import os
from sentence_transformers import SentenceTransformer

# Get the absolute path to the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(script_dir, 'models')

embedding_model = SentenceTransformer(
    'hkunlp/instructor-large', cache_folder=cache_dir)


def get_model():
    return embedding_model


# Define a function to generate embeddings
def get_embedding(data, precision="float32"):
    return embedding_model.encode(data, precision=precision).tolist()
