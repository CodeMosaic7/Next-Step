import uuid
from datetime import datetime, date
from sqlalchemy import (
    Column, String, DateTime, Boolean, Enum, ForeignKey,
    Integer, Text, Date, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# --- USERS ---
class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firebase_uid = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    display_name = Column(String)
    phone_number = Column(String)
    profile_picture_url = Column(String)
    status = Column(Enum("active", "inactive", "suspended", "deleted", name="user_status"), default="active")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, index=True)
    created_by_ip = Column(String)
    metadata = Column(JSONB, default={})

    # Relationships
    profiles = relationship("UserProfile", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")


# --- USER_PROFILES ---
class UserProfile(Base):
    __tablename__ = "user_profiles"

    profile_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), index=True, nullable=False)
    birth_date = Column(Date)
    gender = Column(Enum("male", "female", "other", "prefer_not_to_say", name="gender_enum"))
    preferred_language = Column(String, index=True)
    timezone = Column(String)
    accessibility_enabled = Column(Boolean, default=False)
    accessibility_preferences = Column(JSONB, default={})
    bio = Column(Text)
    emergency_contacts = Column(JSONB, default={})
    data_collection_consent = Column(Boolean, default=True)
    profile_completed_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    version = Column(Integer, default=1)

    # Relationships
    user = relationship("User", back_populates="profiles")


# --- ROLES ---
class Role(Base):
    __tablename__ = "roles"

    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_name = Column(String, unique=True, nullable=False)  # student|mentor|admin|super_admin
    description = Column(Text)
    permissions = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    assignments = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")


# --- USER_ROLES ---
class UserRole(Base):
    __tablename__ = "user_roles"

    role_assignment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), index=True, nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.role_id"), index=True, nullable=False)

    assigned_at = Column(DateTime, default=datetime.utcnow, index=True)
    expires_at = Column(DateTime, index=True, nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    # Relationships
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="assignments")
