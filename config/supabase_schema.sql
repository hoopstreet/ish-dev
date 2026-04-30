-- ============================================================
-- HOOPSTREET SUPABASE SCHEMA
-- Run this in your Supabase SQL Editor
-- ============================================================

-- 1. CREDENTIALS TABLE (for tokens, API keys)
CREATE TABLE IF NOT EXISTS credentials (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT UNIQUE NOT NULL,
  value TEXT NOT NULL,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  user_id TEXT DEFAULT 'default'
);

-- 2. PROJECTS TABLE (for GitHub repos)
CREATE TABLE IF NOT EXISTS projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  repo_url TEXT NOT NULL,
  local_path TEXT,
  description TEXT,
  last_sync TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  user_id TEXT DEFAULT 'default',
  UNIQUE(name, user_id)
);

-- 3. SYSTEM_STATE TABLE (for agent state)
CREATE TABLE IF NOT EXISTS system_state (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  key TEXT UNIQUE NOT NULL,
  value JSONB,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 4. DNA_LOGS TABLE (for evolution tracking)
CREATE TABLE IF NOT EXISTS dna_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  version TEXT,
  task TEXT,
  files_changed JSONB,
  changes TEXT,
  impact TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. ACTIVITY_LOGS TABLE
CREATE TABLE IF NOT EXISTS activity_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event TEXT,
  level TEXT DEFAULT 'INFO',
  details JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ENABLE ROW LEVEL SECURITY
-- ============================================================
ALTER TABLE credentials ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE system_state ENABLE ROW LEVEL SECURITY;
ALTER TABLE dna_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;
-- ============================================================
-- CREATE POLICIES
-- ============================================================
CREATE POLICY "Enable all for authenticated users" ON credentials
  FOR ALL USING (true);

CREATE POLICY "Enable all for authenticated users" ON projects
  FOR ALL USING (true);

CREATE POLICY "Enable all for authenticated users" ON system_state
  FOR ALL USING (true);

CREATE POLICY "Enable all for authenticated users" ON dna_logs
  FOR ALL USING (true);

CREATE POLICY "Enable all for authenticated users" ON activity_logs
  FOR ALL USING (true);

-- ============================================================
-- CREATE INDEXES
-- ============================================================
CREATE INDEX idx_credentials_name ON credentials(name);
CREATE INDEX idx_projects_name ON projects(name);
CREATE INDEX idx_projects_user ON projects(user_id);
CREATE INDEX idx_system_state_key ON system_state(key);
CREATE INDEX idx_activity_logs_created ON activity_logs(created_at);

-- ============================================================
-- INSERT INITIAL SYSTEM STATE
-- ============================================================
INSERT INTO system_state (key, value) VALUES 
  ('version', '"v9.0.0"'),
  ('status', '"active"'),
  ('last_health_check', 'NOW()')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value, updated_at = NOW();

-- ============================================================
-- VERIFY TABLES
-- ============================================================
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
