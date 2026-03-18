import os
from supabase import create_client, Client
from secret import SUPABASE_URL
from secret import  SUPABASE_KEY

url: str = SUPABASE_URL
key: str = SUPABASE_KEY

supabase_client: Client = create_client(url, key)
