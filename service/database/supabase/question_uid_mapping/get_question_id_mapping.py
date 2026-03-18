from .. import supabase_client


def get_question_id_mapping_supabase(question_uid: str) -> dict:
    try:
        data = (
            supabase_client.table("amigo_question_uid_mapping")
            .select("*")
            .eq("id", question_uid)
            .execute()
        )
    except Exception as e:
        return None

    return data.data[0]

