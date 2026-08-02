from config.database import Base
from config.database import engine
# Import your models
import models.chat_model

Base.metadata.create_all(bind=engine)

print("Database created successfully.")