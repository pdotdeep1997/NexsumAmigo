from .. import supabase_client


def update_question_as_answered_supabase(q_uid: str) -> dict:
    try:
        data = (
            supabase_client.table("amigo_question_uid_mapping")
            .update(
                {
                    "question_answered_state": True,
                }
            )
            .eq("id", q_uid)
            .execute()
        )
    except Exception as e:
        return None

    return data.data[0]

