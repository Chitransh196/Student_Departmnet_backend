from St_Pd import engine
from modelss import Base

Base.metadata.create_all(bind=engine)
print("✅ Tables created")
