from app.services.db import engine
from app.models.db_models import Base

# Drops old tables and recreates them with the new URL column!
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Database reset successfully! All tables recreated.")
