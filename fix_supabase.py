import os
from dotenv import load_dotenv
from supabase import create_client
import json

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase client initialized")
        
        # Create user_progress table using SQL
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS user_progress (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            user_id TEXT NOT NULL,
            completed_modules TEXT,
            quiz_scores JSONB DEFAULT '{}'::json,
            training_status TEXT,
            interviews_completed INTEGER DEFAULT 0,
            overall_score INTEGER DEFAULT 0,
            resume_analyzed BOOLEAN DEFAULT FALSE,
            training_plans_viewed INTEGER DEFAULT 0,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Execute table creation using RPC
        try:
            result = supabase.rpc('exec_sql', {
                'sql': create_table_sql
            }).execute()
            print(f"✅ Table creation result: {result}")
        except Exception as e:
            print(f"❌ Failed to create table: {e}")
            
        # Test table by inserting sample data
        try:
            test_data = {
                'user_id': 'test-user',
                'quiz_scores': {'software-engineer': 85},
                'interviews_completed': 1,
                'overall_score': 85,
                'resume_analyzed': False,
                'training_plans_viewed': 0
            }
            
            result = supabase.table("user_progress").insert(test_data).execute()
            print(f"✅ Test insert result: {result}")
            
            # Test fetching data
            result = supabase.table("user_progress").select("*").eq("user_id", "test-user").execute()
            if result.data:
                print(f"✅ Test fetch result: {result.data[0]}")
            else:
                print("❌ Test fetch failed")
                
        except Exception as e:
            print(f"❌ Failed to test table: {e}")
            
    except Exception as e:
        print(f"❌ Failed to initialize Supabase client: {e}")
else:
    print("⚠️ SUPABASE_URL or SUPABASE_KEY not found in environment")
