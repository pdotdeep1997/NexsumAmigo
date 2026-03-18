from .. import supabase_client


def insert_question_instance_supabase(question_id: str) -> dict:
    try:
        data = (
            supabase_client.table("amigo_question_uid_mapping")
            .insert(
                {
                    "question_id": question_id,
                    "question_answered_state": False
                }
            )
            .execute()
        )
    except Exception as e:
        return None

    return data.data[0]
