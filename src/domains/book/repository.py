import uuid

from sqlalchemy import delete, func, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.domains.author.models import Author
from src.domains.author.schema import AuthorReadSchema
from src.domains.book.models import Book
from src.domains.book.schema import (
    BookCreateSchema,
    BookFilters,
    BookReadSchema,
    BookUpdateSchema,
)
from src.domains.common.association.author_book import AuthorBook
from src.domains.review.models import Review
from src.domains.review.schema import ReviewWithUserSchema
from src.exceptions.entity import EntityIntegrityException, EntityNotFound


async def create_book(session: AsyncSession, book: BookCreateSchema) -> BookReadSchema:
    new_book = Book(
        title=book.title,
        genre_id=book.genre_id,
    )

    try:
        session.add(new_book)
        if book.authors:
            authors_result = await session.execute(
                select(Author).where(Author.id.in_(book.authors))
            )
            authors = authors_result.scalars().all()

            if len(authors) != len(book.authors):
                raise EntityNotFound({"authors": book.authors}, "auhtors")

            await session.flush()
            rows = [{"author_id": a.id, "book_id": new_book.id} for a in authors]
            await session.execute(insert(AuthorBook), rows)

            await session.commit()
    except IntegrityError as err:
        await session.rollback()
        raise EntityIntegrityException(str(err._message())) from None

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
        authors_result = await session.execute(
            select(Author).where(Author.id.in_(data.authors))
        )
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
    stmt = (
        delete(Book).where(Book.id == id).returning(Book.id, Book.title, Book.genre_id)
    )

    result = await session.execute(stmt)

    if result.fetchone() is None:
        raise EntityNotFound({"id": id}, "book")
    await session.commit()


async def get_book_information(session: AsyncSession, id: uuid.UUID):
    book_stmt = select(Book).where(Book.id == id).options(
        joinedload(Book.authors).joinedload(Author.genres)
    )
    book_result = await session.execute(book_stmt)
    book = book_result.unique().scalar_one_or_none()

    if not book:
        raise EntityNotFound({"id": id}, "book")

    rating_stmt = select(func.avg(Review.rating), func.count(Review.id)).where(
        Review.book_id == id
    )
    rating_result = await session.execute(rating_stmt)
    avg_rating, total_ratings = rating_result.one()

    max_rating_stmt = select(func.count(Review.id)).where(
        Review.book_id == id, Review.rating == 5
    )
    max_rating_result = await session.execute(max_rating_stmt)
    max_rating_count = max_rating_result.scalar()

    text_reviews_stmt = select(func.count(Review.id)).where(
        Review.book_id == id, Review.text.isnot(None), Review.text != ""
    )
    text_reviews_result = await session.execute(text_reviews_stmt)
    text_reviews_count = text_reviews_result.scalar()

    reviews_stmt = (
        select(Review)
        .options(joinedload(Review.user))
        .where(Review.book_id == id)
        .order_by(Review.create_at.desc())
        .limit(10)
    )
    reviews_result = await session.execute(reviews_stmt)
    reviews = reviews_result.scalars().all()

    latest_reviews = [
        ReviewWithUserSchema(
            id=r.id,
            user_id=r.user_id,
            username=r.user.username,
            book_id=r.book_id,
            rating=r.rating,
            text=r.text,
            created_at=r.create_at.strftime("%Y-%m-%d %H:%M"),
        )
        for r in reviews
    ]

    authors_data = [
        AuthorReadSchema(
            id=author.id,
            first_name=author.first_name,
            last_name=author.last_name,
            birth_date=author.birth_date,
            genres=[g.id for g in author.genres] if author.genres else [],
        )
        for author in book.authors
    ]

    return {
        "id": book.id,
        "title": book.title,
        "authors": authors_data,
        "description": book.description,
        "genre_id": book.genre_id,
        "category_id": book.category_id,
        "average_rating": float(avg_rating) if avg_rating else None,
        "total_ratings": total_ratings,
        "max_rating_count": max_rating_count,
        "text_reviews_count": text_reviews_count,
        "latest_reviews": latest_reviews,
    }
