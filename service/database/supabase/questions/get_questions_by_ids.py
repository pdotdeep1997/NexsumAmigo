from .. import supabase_client


def list_question_by_ids_supabase(question_ids: list[str], language: str) -> list:
    try:
        data = (
            supabase_client.table("amigo_questions")
            .select("*")
            .in_("id", question_ids)
            .execute()
        )
    except Exception as e:
        return None

    return data.data

def get_question_by_id_supabase(question_id: str, language: str) -> dict:
    print("FETCHING QUESTION BY ID", question_id, language)
    try:
        data = (
            supabase_client.table("amigo_questions")
            .select("*")
            .eq("id", question_id)
            .execute()
        )
    except Exception as e:
        return None

    return data.data[0]

