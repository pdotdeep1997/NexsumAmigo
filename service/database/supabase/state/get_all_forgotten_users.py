from datetime import datetime, timedelta, timezone
from .. import supabase_client

from secret import IS_PROD


def get_all_forgotten_users_supabase() -> list:
    try:
        # Calculate the timestamp for 12 hours ago
        twelve_hours_ago = datetime.now(timezone.utc) - timedelta(hours=12)

        if IS_PROD:
            # Query users where last_message_sent is less than 12 hours ago
            response = (
                supabase_client.table("amigo_state")
                .select("*")
                .lt("last_message_time", twelve_hours_ago.isoformat())  # ISO 8601 format
                .execute()
            )
        
        else:
            print("RUNNING LOCAL NOW")
            response = (
                supabase_client.table("amigo_state")
                .select("*")
                .eq("chat_id" , "293742291")
                .execute()
            )

        return response.data

    except Exception as e:
        print(f"Error fetching forgotten users: {e}")
        return []
