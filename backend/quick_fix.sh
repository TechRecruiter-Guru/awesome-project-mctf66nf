#!/bin/bash
# Quick Fix Script for Render DATABASE_URL
# Run this in the morning - just copy/paste into Render Shell

echo "🔧 Setting up database connection..."

# Set the correct DATABASE_URL (hardcoded for safety)
export DATABASE_URL="postgresql://postgres.pctnqtdbcyayyqbqfcfx:Muses480%21@aws-0-us-west-2.pooler.supabase.com:6543/postgres"

# Initialize database tables
echo "📊 Creating database tables..."
python -c "from app import db; db.create_all(); print('✅ Tables created!')"

# Populate with sample data
echo "👥 Adding sample data..."
python populate_sample_data.py

echo "🎉 Done! Your ATS is ready!"
