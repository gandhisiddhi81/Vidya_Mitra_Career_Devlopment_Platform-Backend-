import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def list_tables():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        print("❌ Supabase config missing")
        return
    
    try:
        supabase = create_client(url, key)
        # There's no direct list_tables in the python sdk easily, 
        # but we can try to query some common tables or use postgrest.
        # Alternatively, the error hint said "Perhaps you meant the table 'public.users'"
        # Let's see if we can query 'users'
        response = supabase.table("users").select("*", count="exact").limit(1).execute()
        print(f"✅ Found 'users' table. Data: {response.data}")
        
        # Try to see if there's a profile or similar
        try:
            response = supabase.table("profiles").select("*").limit(1).execute()
            print(f"✅ Found 'profiles' table")
        except:
            print("❌ 'profiles' table not found")

    except Exception as e:
        print(f"❌ Supabase Error: {e}")

if __name__ == "__main__":
    list_tables()
