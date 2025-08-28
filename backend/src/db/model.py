import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, Mapped, mapped_column,sessionmaker, relationship

engine = sa.create_engine('postgresql://user:password@localhost/dbname')
Session= sessionmaker(bind=engine)
Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(sa.String(50),nullable=False)
    email: Mapped[str] = mapped_column(sa.String(150), nullable=False, unique=True)
    created_at: Mapped[sa.DateTime] = mapped_column(default=sa.func.now())
    updated_at: Mapped[sa.DateTime] = mapped_column(default=sa.func.now(), onupdate=sa.func.now())

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    university: Mapped["University"] = relationship(back_populates="courses") 
    university_id: Mapped[int] = mapped_column(sa.ForeignKey("universities.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at: Mapped[sa.DateTime] = mapped_column(default=sa.func.now())
    updated_at: Mapped[sa.DateTime] = mapped_column(default=sa.func.now(), onupdate=sa.func.now())

class University(Base):
    __tablename__ = "universities"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    courses: Mapped[list["Course"]] = relationship(back_populates="university")
    created_at: Mapped[sa.DateTime] = mapped_column(default=sa.func.now())
    updated_at: Mapped[sa.DateTime] = mapped_column(default=sa.func.now(), onupdate=sa.func.now())

class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))
    summary_id: Mapped[int] = mapped_column(sa.ForeignKey('summaries.id'))
    content: Mapped[str] = mapped_column(sa.Text, nullable=False)
    summary: Mapped["Summary"] = relationship(back_populates="comments")
    created_at: Mapped[sa.DateTime] = mapped_column(default=sa.func.now())
    updated_at: Mapped[sa.DateTime] = mapped_column(default=sa.func.now(), onupdate=sa.func.now())
class SummaryStar(Base):
    __tablename__ = "summary_stars"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))
    summary: Mapped["Summary"] = relationship(back_populates="stars")
    summary_id: Mapped[int] = mapped_column(sa.ForeignKey('summaries.id'))
    created_at: Mapped[sa.DateTime] = mapped_column(default=sa.func.now())
class Summary(Base):
    __tablename__ = "summaries"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, index=True)
    owner: Mapped[str] = mapped_column(sa.String(50), nullable=False, default="")
    uploader_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(sa.String(200), nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, default="")
    url: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    course_id: Mapped[int] = mapped_column(sa.ForeignKey('courses.id'))
    stars: Mapped[list["SummaryStar"]] = relationship(back_populates="summary", cascade="all, delete-orphan")
    downloaded: Mapped[int] = mapped_column(default=0)
    comments: Mapped[list["Comment"]] = relationship(back_populates="summary", cascade="all, delete-orphan")
    pages: Mapped[int] = mapped_column(default=0)
    file_size: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[sa.DateTime] = mapped_column(default=sa.func.now())
    updated_at: Mapped[sa.DateTime] = mapped_column(default=sa.func.now(), onupdate=sa.func.now())
    
def main()->None:
    Base.metadata.create_all(engine)

    with Session() as session:
        print(session.query(User).all())