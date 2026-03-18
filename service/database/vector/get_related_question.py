
import vecs
from service.openai.embeddings import get_embedding
from secret import DB_CONNECTION


def get_relevant_document_ids_for_query(query: str,language: str, limit: int):
    with vecs.create_client(DB_CONNECTION) as vx:
        docs = vx.get_or_create_collection(name="question_vector", dimension=1536)

        docs.create_index() 

        query_embedding = get_embedding(query)

        print("QUERY EMBEDDING ", language)
        # print("language": language)

        context_ids = docs.query(
            data=query_embedding,  # required
            limit=limit,  # number of records to return
            filters={"language": {"$eq": language}},  # metadata filters
            measure="cosine_distance",  # distance measure to use
            include_value=False,  # should distance measure values be returned?
            include_metadata=True,  # should record metadata be returned?
        )
        print("CONTEXT IDS")
        print(context_ids)

        doc_ids = [d[0] for d in context_ids]

        return doc_ids