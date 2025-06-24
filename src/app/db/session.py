from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine_content = create_engine(getenv("DATABASE_URL1"))
SessionContent = sessionmaker(bind=engine_content, autocommit=False, autoflush=False)

engine_logs = create_engine(getenv("DATABASE_URL2"))
SessionLogs = sessionmaker(bind=engine_logs, autocommit=False, autoflush=False)
