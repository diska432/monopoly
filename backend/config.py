import os
from pathlib import Path
from dotenv import load_dotenv

_backend_dir = Path(__file__).resolve().parent
_project_root = _backend_dir.parent

for env_path in [_backend_dir / ".env", _project_root / ".env"]:
    if env_path.is_file():
        load_dotenv(env_path, override=False)

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_JWT_SECRET: str = os.getenv("SUPABASE_JWT_SECRET", "")
FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
