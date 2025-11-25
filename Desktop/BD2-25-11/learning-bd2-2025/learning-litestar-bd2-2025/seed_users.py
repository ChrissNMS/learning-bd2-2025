"""Script para insertar usuarios de prueba en la BD."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.config import settings
from app.models import User
from app.repositories.user import password_hasher

# Crear conexión a la BD
engine = create_engine(settings.database_url)

# Crear sesión
with Session(engine) as session:
    # Verificar si ya existen usuarios
    existing = session.query(User).filter(User.username == "alice").first()
    
    if not existing:
        # Crear usuarios de prueba
        alice = User(
            username="alice",
            password=password_hasher.hash("password123"),
            fullname="Alice Example",
        )
        bob = User(
            username="bob",
            password=password_hasher.hash("secret"),
            fullname="Bob Example",
        )
        
        session.add(alice)
        session.add(bob)
        session.commit()
        print("✅ Usuarios de prueba insertados:")
        print("  - alice / password123")
        print("  - bob / secret")
    else:
        print("ℹ️  Los usuarios ya existen en la BD.")
