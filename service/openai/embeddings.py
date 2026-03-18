from openai import OpenAI
from secret import OPEN_API_KEY

client = OpenAI(api_key=OPEN_API_KEY)


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding
