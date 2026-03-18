from ..supabase.state.get_all_forgotten_users import get_all_forgotten_users_supabase

class AllUsersDBAdapter:

    def __init__(self):
        pass


    def get_all_forgotten_users(self):
        return get_all_forgotten_users_supabase()

    