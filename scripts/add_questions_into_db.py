import vecs
from dotenv import load_dotenv
import os
from openai import OpenAI
from supabase import create_client, Client
# Load variables from .env into environment
load_dotenv()

# Access them using os.environ or os.getenv
DB_CONNECTION = os.getenv("DB_CONNECTION")
OPEN_API_KEY = os.getenv("OPEN_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# create vector store client
vx = vecs.create_client(DB_CONNECTION)


docs = vx.get_or_create_collection(name="question_vector", dimension=1536)

docs.create_index() 

client = OpenAI(api_key=OPEN_API_KEY)


url: str = SUPABASE_URL
key: str = SUPABASE_KEY

supabase_client: Client = create_client(url, key)


def insert_question(question: dict) -> dict:
    print(question)
    try:
        data = (
            supabase_client.table("hindi_questions")
            .insert(
                {
                    "question": question,
                }
            )
            .execute()
        )
    except Exception as e:
        return {"data": {}, "error": str(e)}

    return {"data": data.data}



def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding



def get_relevant_document_ids_for_query(query: str, limit: int):
    with vecs.create_client(DB_CONNECTION) as vx:
        docs = vx.get_or_create_collection(name="question_vector", dimension=1536)

        query_embedding = get_embedding(query)

        context_ids = docs.query(
            data=query_embedding,  # required
            limit=limit,  # number of records to return
            filters={},  # metadata filters
            measure="cosine_distance",  # distance measure to use
            include_value=False,  # should distance measure values be returned?
            include_metadata=True,  # should record metadata be returned?
        )

        doc_ids = [d[0] for d in context_ids]

        return doc_ids


def insert_questions_into_vec(
    question: str,
    options: list,
    correct_answer: int,
    topic: str
):
    with vecs.create_client(DB_CONNECTION) as vx:
        docs = vx.get_or_create_collection(name="question_vector", dimension=1536)

        questions_data = f"{question},{','.join(options)}"
        texts = [questions_data]

        print("PRINTING DOCUMENTS")
        records = []
        document = insert_question({
            "question": question,
            "options": options,
            "correct_answer": correct_answer
        })

        if "error" in document:
            raise Exception
        print(document)
        document_id = document["data"][0]["id"]

        print(document_id)

        embedding = get_embedding(text=questions_data)

        metadata = {
            "topic": topic,
        }

        records.append((document_id, embedding, metadata))

        docs.upsert(records=records)

import json


# Get the current script's directory (the folder containing this .py file)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Build the full path to the JSON file
json_path = os.path.join(script_dir, "beginner_questions.json")


# Load questions from JSON file
with open(json_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

# Insert each question into the vector DB
for q in questions:
    try:
        insert_questions_into_vec(
            question=q["question"],
            options=q["options"],
            correct_answer=q["correct_answer"],
            topic=q["topic"]
        )
        print(f"✅ Inserted: {q['question']}")
    except Exception as e:
        print(f"❌ Failed to insert: {q['question']} - Error: {str(e)}")
