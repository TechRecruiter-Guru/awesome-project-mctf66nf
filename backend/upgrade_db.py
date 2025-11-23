#!/usr/bin/env python3
"""
Upgrade script to add missing columns to Application table
"""
import sqlite3
import sys

DB_PATH = './instance/ats.db'

def upgrade_database():
    """Add missing columns to Application table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(application)")
        columns = [row[1] for row in cursor.fetchall()]
        
        print("📋 Current Application table columns:")
        for col in columns:
            print(f"   - {col}")
        
        # Add missing columns
        to_add = []
        if 'hiring_intelligence' not in columns:
            to_add.append(('hiring_intelligence', 'TEXT'))
        if 'hidden_signal' not in columns:
            to_add.append(('hidden_signal', 'TEXT'))
        if 'position' not in columns:
            to_add.append(('position', 'VARCHAR(255)'))
        
        if not to_add:
            print("\n✅ All required columns already exist!")
            return True
        
        print(f"\n📝 Adding {len(to_add)} missing columns...")
        for col_name, col_type in to_add:
            try:
                cursor.execute(f"ALTER TABLE application ADD COLUMN {col_name} {col_type}")
                print(f"   ✅ Added {col_name} ({col_type})")
            except sqlite3.OperationalError as e:
                print(f"   ❌ Error adding {col_name}: {e}")
                return False
        
        conn.commit()
        
        # Verify
        cursor.execute("PRAGMA table_info(application)")
        updated_columns = [row[1] for row in cursor.fetchall()]
        print(f"\n✅ Database upgraded successfully!")
        print(f"   Total columns: {len(updated_columns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    success = upgrade_database()
    sys.exit(0 if success else 1)
