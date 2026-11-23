from fastapi import FastAPI, Body, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status
app = FastAPI()

class Book:
    def __init__(self, id, title, author, description, rating,published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date=published_date

class BookRequest(BaseModel):
    id:Optional[int] = None 
    title:str = Field(min_length=1, description="The title of the book")
    author:str=Field(min_length=1, description="The author of the book")
    description:str=Field(min_length=1, description="A brief description of the book")
    rating:float=Field(gt=0, lt=6, description="The rating of the book (1-5)")
    published_date:Optional[str] = Field(default=None, description="The published date of the book in YYYY-MM-DD format")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Book Title",
                "author": "Author Name",
                "description": "A brief description of the book",
                "rating": 4.5
            }
        }
    }




BOOKS = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "A novel set in the Roaring Twenties.", 4.5, "1925-04-10"),
    Book(2, "To Kill a Mockingbird", "Harper Lee", "A novel about racial injustice in the Deep South.", 4.8, "1960-07-11"),
    Book(3, "1984", "George Orwell", "A dystopian novel about totalitarianism.", 4.7, "1948-06-08"),
    Book(4, "Pride and Prejudice", "Jane Austen", "A classic romance novel.", 4.6, "1813-01-28"),
    Book(5, "The Catcher in the Rye", "J.D. Salinger", "A novel about teenage rebellion and alienation.", 4.3, "1951-07-16"),
    Book(6, "The Hobbit", "J.R.R. Tolkien", "A fantasy novel about a hobbit's adventure.", 4.9, "1937-09-21"),
    Book(7, "Moby-Dick", "Herman Melville", "A novel about the pursuit of a giant whale.", 4.2, "1851-10-18"),
    Book(8, "War and Peace", "Leo Tolstoy", "A historical novel set during the Napoleonic Wars.", 4.4, "1869-01-01"),
    Book(9, "The Odyssey", "Homer", "An epic poem about the journey of Odysseus.", 4.5, "1925-04-10"),
    Book(10, "The Divine Comedy", "Dante Alighieri", "An epic poem about the afterlife.", 4.6, "1948-06-08"),
    Book(11, "The Brothers Karamazov", "Fyodor Dostoevsky", "A philosophical novel about morality and faith.", 4.7, "1880-01-01"),
    Book(12, "Crime and Punishment", "Fyodor Dostoevsky", "A novel about guilt and redemption.", 4.8, "1866-01-01"),
    Book(13, "The Iliad", "Homer", "An epic poem about the Trojan War.", 4.5, "1925-04-10"),
    Book(14, "The Aeneid", "Virgil", "An epic poem about the founding of Rome.", 4.4, "1925-04-10"),
    Book(15, "The Canterbury Tales", "Geoffrey Chaucer", "A collection of stories told by pilgrims on their way to Canterbury.", 4.3, "1925-04-10")
]
@app.get("/books/{book_id}")
async def read_book(book_id:int = Path(title="The ID of the book to retrieve", gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item Not FOund")

@app.get("/books/")
async def read_book_by_rating(rating:float = Query(title="The rating of the books to retrieve", ge=0, le=5)):
    books_to_return = []    
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books")
async def read_books():
    return BOOKS

@app.post("/create_book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_bookid(new_book))
    
def find_bookid(book:Book):
    if len(BOOKS)>0:
        book.id=BOOKS[-1].id+1
    else:
        book.id=1
    return book
    

@app.put("/books/update_book", status_code=status.HTTP_200_OK)
async def update_book(book: BookRequest):
    book_changed=False
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=book
            book_changed=True
        if not book_changed:
            raise HTTPException(status_code=404,detail="Item Not Found")

@app.delete("/books/delete_book/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id:int):
    for i in range(len(BOOKS)):
        book_changed=False
        if BOOKS[i].id==book_id:
            del BOOKS[i]
            book_changed=True
    if not book_changed:
        raise HTTPException(status_code=404,detail="Item aint there lol")

@app.get("/books/bydate/")
async def read_book_by_date(published_date: str):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return