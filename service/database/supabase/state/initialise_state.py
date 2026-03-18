from .. import supabase_client


def initialise_state_supabase(chat_id: str, language: str) -> dict:
    try:
        data = (
            supabase_client.table("amigo_state")
            .insert(
                {
                    "chat_id": chat_id,
                    "language": language,
                    "state": "MESSAGE"
                }
            )
            .execute()
        )
    except Exception as e:
        return None

    return data.data[0]
