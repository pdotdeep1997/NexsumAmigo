from .. import supabase_client


def insert_question_supabase(question: dict, language: str) -> dict:
    try:
        data = (
            supabase_client.table("questions")
            .insert(
                {
                    "question": question,
                    "language": language
                }
            )
            .execute()
        )
    except Exception as e:
        return None

    return data.data[0]
