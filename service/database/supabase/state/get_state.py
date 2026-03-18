from .. import supabase_client
from .initialise_state import initialise_state_supabase


def get_state_for_chat_id_supabase(chat_id: str, language: str) -> dict:
    try:
        data = (
            supabase_client.table("amigo_state")
            .select("*")
            .eq("chat_id" , chat_id)
            .eq("language", language)
            .execute()
        )
        if not data.data:
            return initialise_state_supabase(chat_id=chat_id, language=language)
        

    except Exception as e:
        return None

    return data.data[0]
