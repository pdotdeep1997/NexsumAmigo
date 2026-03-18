from .. import supabase_client


def update_question_id_mapping_with_message_id_supabase(q_uid: str, message_id: str) -> dict:
    try:
        data = (
            supabase_client.table("amigo_question_uid_mapping")
            .update(
                {
                    "message_id": message_id,
                }
            )
            .eq("id", q_uid)
            .execute()
        )
    except Exception as e:
        return None

    return data.data[0]

