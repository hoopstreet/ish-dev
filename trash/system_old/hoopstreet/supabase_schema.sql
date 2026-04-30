-- Supabase Public Schema for Credentials Manager
-- Run this in your Supabase SQL Editor

-- Create credentials table
CREATE TABLE IF NOT EXISTS public.credentials (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT UNIQUE NOT NULL,
  value TEXT NOT NULL,
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE public.credentials ENABLE ROW LEVEL SECURITY;

-- Create policy for public access (for iSH)
CREATE POLICY "Enable all for authenticated users" ON public.credentials
  FOR ALL USING (true);

-- Create index for faster lookups
CREATE INDEX idx_credentials_name ON public.credentials(name);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_credentials_updated_at
  BEFORE UPDATE ON public.credentials
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Insert sample credential (optional)
INSERT INTO public.credentials (name, value, notes)
VALUES ('SAMPLE_TOKEN', 'your-token-here', 'Example credential')
ON CONFLICT (name) DO NOTHING;

-- Verify table
SELECT * FROM public.credentials;
