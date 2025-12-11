import uuid

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.author.models import Author
from src.domains.book.models import Book
from src.domains.book.schema import BookCreateSchema, BookFilters, BookReadSchema, BookUpdateSchema
from src.domains.common.association.author_book import AuthorBook
from src.exceptions.entity import EntityIntegrityException, EntityNotFound


async def create_book(session: AsyncSession, book: BookCreateSchema) -> BookReadSchema:
    new_book = Book(
        title=book.title,
        genre_id=book.genre_id,
    )

    session.add(new_book)
    if book.authors:
        authors_result = await session.execute(select(Author).where(Author.id.in_(book.authors)))
        authors = authors_result.scalars().all()

        if len(authors) != len(book.authors):
            raise EntityNotFound({"authors": book.authors}, "auhtors")

        await session.flush()
        rows = [{"author_id": a.id, "book_id": new_book.id} for a in authors]
        await session.execute(insert(AuthorBook), rows)

    try:
        await session.commit()
    except IntegrityError as err:
        await session.rollback()
        raise EntityIntegrityException(str(err)) from None

    return BookReadSchema.model_validate(new_book)


async def get_book_by_id(
    session: AsyncSession,
    id: uuid.UUID,
) -> BookReadSchema:
    result = await session.execute(select(Book).where(Book.id == id))
    book = result.scalar_one_or_none()

    if not book:
        raise EntityNotFound({"id": id}, "book")

    return BookReadSchema.model_validate(book)


async def get_books_list(
    session: AsyncSession,
    filters: BookFilters,
) -> list[BookReadSchema]:
    query = select(Book)

    if filters.title:
        query = query.where(Book.title.ilike(f"%{filters.title}%"))

    if filters.genre_id:
        query = query.where(Book.genre_id == filters.genre_id)

    if filters.author_id:
        query = query.join(Book.authors).where(Author.id == filters.author_id)

    query = query.limit(filters.limit).offset(filters.offset)

    result = await session.execute(query)
    books = result.scalars().all()

    return [BookReadSchema.model_validate(b) for b in books]


async def update_book(
    session: AsyncSession,
    id: uuid.UUID,
    data: BookUpdateSchema,
) -> BookReadSchema:
    result = await session.execute(select(Book).where(Book.id == id))
    book = result.scalar_one_or_none()

    if not book:
        raise EntityNotFound({"id": id}, "book")

    if data.title is not None:
        book.title = data.title

    if data.genre_id is not None:
        book.genre_id = data.genre_id

    if data.authors is not None:
        authors_result = await session.execute(select(Author).where(Author.id.in_(data.authors)))
        authors = authors_result.scalars().all()

        if len(authors) != len(data.authors):
            raise EntityIntegrityException("Some authors do not exist")

        await session.execute(delete(AuthorBook).where(AuthorBook.book_id == book.id))
        await session.execute(
            insert(AuthorBook),
            [{"author_id": a.id, "book_id": book.id} for a in authors],
        )

    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise EntityIntegrityException("Integrity error") from None

    return BookReadSchema.model_validate(book)


async def delete_book(
    session: AsyncSession,
    id: uuid.UUID,
):
    stmt = delete(Book).where(Book.id == id).returning(Book.id, Book.title, Book.genre_id)

    result = await session.execute(stmt)

    if result.fetchone() is None:
        raise EntityNotFound({"id": id}, "book")
    await session.commit()
