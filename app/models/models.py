from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Usuarios(Base):
    __tablename__ = "usuarios"
    id_usuario = Column(String, primary_key=True)
    id_area = Column(String, ForeignKey("areas.id_area"))
    id_empresa = Column(String)
    nombre = Column(String)
    correo = Column(String, unique=True)
    contraseña = Column(String)
    rol = Column(String, ForeignKey("roles.id_rol"))
    activo = Column(Boolean)
    roles = relationship("Roles", back_populates="rol_usuario")
    area = relationship("Area", back_populates="area_usuario")

    def __repr__(self):
        return f"<Usuarios(id_usuario={self.id_usuario}, nombre={self.nombre}, correo={self.correo}, rol={self.roles}, id_area={self.id_area}, id_empresa={self.id_empresa})>"


class Roles(Base):
    __tablename__ = "roles"
    id_rol = Column(String, primary_key=True)
    rol = Column(String)
    rol_usuario = relationship("Usuarios", back_populates="roles")

    def __repr__(self):
        return self.rol


class Area(Base):
    __tablename__ = "areas"
    id_area = Column(String, primary_key=True)
    id_empresa = Column(String)
    asistente = Column(String)
    vectores = Column(String)
    area_usuario = relationship("Usuarios", back_populates="area")

    def __repr__(self):
        return f"<Areas(id_area={self.id_area}, id_empresa={self.id_empresa})>"


class Empresa(Base):
    __tablename__ = "empresa"
    id_empresa = Column(String, primary_key=True)
    nombre_empresa = Column(String)

    def __repr__(self):
        return self.nombre_empresa


class id_archivos_openai(Base):
    __tablename__ = "id_archivos_openai"
    id_archivo = Column(String, primary_key=True)
    nombre_documento = Column(String)
    id_area = Column(String)

    def __repr__(self):
        return f"<id_archivos_openai(id_archivo={self.id_archivo}, nombre_documento={self.nombre_documento}, id_area={self.id_area})>"
