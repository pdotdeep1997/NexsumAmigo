from .. import supabase_client
import random

def update_state_for_chat_id_to_messaging_state(chat_id: str, language: str) -> dict:
    try:
        data = (
            supabase_client.table("amigo_state")
            .update(
                {
                    "state": "MESSAGE",
                }
            )
            .eq("chat_id", chat_id)
            .eq("language", language)
            .execute()
        )
    except Exception as e:
        return None

    return data.data[0]

def update_state_for_chat_id_to_quiz_state(chat_id: str, language: str) -> dict:
    try:
        data = (
            supabase_client.table("amigo_state")
            .update(
                {
                    "state": "QUIZ",
                }
            )
            .eq("chat_id", chat_id)
            .eq("language", language)
            .execute()
        )
    except Exception as e:
        return None

    return data.data[0]


def update_last_active_state(chat_id: str, language: str) -> dict:
    try:
        data = (
            supabase_client.table("amigo_state")
            .update(
                {
                    "random_val": random.random(),
                }
            )
            .eq("chat_id", chat_id)
            .eq("language", language)
            .execute()
        )
    except Exception as e:
        return None

    return data.data[0]