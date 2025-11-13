"""
Example showing how to integrate monitoring with SQLAlchemy database.

This enables daily statistics reports with user and project counts.
"""

from datetime import datetime
from typing import Optional
from fastapi import FastAPI
from sqlalchemy import create_engine, select, func, and_
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from monitoring import setup_monitoring, monitoring_config, DatabaseAdapter


# Database setup (example)
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    last_active_at: Mapped[Optional[datetime]]


class Project(Base):
    __tablename__ = "projects"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    user_id: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)


# Implement DatabaseAdapter
class SQLAlchemyDatabaseAdapter(DatabaseAdapter):
    """
    Adapter for SQLAlchemy database integration.
    This enables monitoring to collect statistics about your data.
    """
    
    def __init__(self, session_maker):
        self.session_maker = session_maker
    
    async def get_new_users_count(self, start_date: datetime, end_date: datetime) -> int:
        """Count users created in the given period"""
        async with self.session_maker() as session:
            result = await session.execute(
                select(func.count())
                .select_from(User)
                .where(
                    and_(
                        User.created_at >= start_date,
                        User.created_at < end_date
                    )
                )
            )
            return result.scalar() or 0
    
    async def get_active_users_count(self, start_date: datetime, end_date: datetime) -> int:
        """Count users active in the given period"""
        async with self.session_maker() as session:
            result = await session.execute(
                select(func.count())
                .select_from(User)
                .where(
                    and_(
                        User.last_active_at >= start_date,
                        User.last_active_at < end_date
                    )
                )
            )
            return result.scalar() or 0
    
    async def get_total_users_count(self) -> int:
        """Get total number of users"""
        async with self.session_maker() as session:
            result = await session.execute(
                select(func.count()).select_from(User)
            )
            return result.scalar() or 0
    
    async def get_new_projects_count(self, start_date: datetime, end_date: datetime) -> int:
        """Count projects created in the given period"""
        async with self.session_maker() as session:
            result = await session.execute(
                select(func.count())
                .select_from(Project)
                .where(
                    and_(
                        Project.created_at >= start_date,
                        Project.created_at < end_date
                    )
                )
            )
            return result.scalar() or 0
    
    async def get_updated_projects_count(self, start_date: datetime, end_date: datetime) -> int:
        """Count projects updated in the given period (excluding new ones)"""
        async with self.session_maker() as session:
            result = await session.execute(
                select(func.count())
                .select_from(Project)
                .where(
                    and_(
                        Project.updated_at >= start_date,
                        Project.updated_at < end_date,
                        Project.created_at < start_date  # Exclude new projects
                    )
                )
            )
            return result.scalar() or 0
    
    async def get_total_projects_count(self) -> int:
        """Get total number of projects"""
        async with self.session_maker() as session:
            result = await session.execute(
                select(func.count()).select_from(Project)
            )
            return result.scalar() or 0
    
    async def health_check(self, timeout: float = 5.0) -> bool:
        """Check if database connection is healthy"""
        try:
            async with self.session_maker() as session:
                # Simple query to check connection
                await session.execute(select(1))
                return True
        except Exception:
            return False


# Setup FastAPI app with monitoring
app = FastAPI()

# Configure monitoring
monitoring_config.TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
monitoring_config.TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

# Create database adapter
db_adapter = SQLAlchemyDatabaseAdapter(async_session_maker)

# Setup monitoring with database adapter
setup_monitoring(
    app,
    database_adapter=db_adapter
)


@app.get("/users")
async def list_users():
    async with async_session_maker() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        return {"users": [{"id": u.id, "email": u.email} for u in users]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)