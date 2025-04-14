import modules.schemas as schemas
from fastapi import APIRouter, HTTPException, status, Depends
from modules.database_connector import get_db
from modules.models import Base, Books
from sqlalchemy.orm import Session
from modules.oauth2 import get_current_user


router = APIRouter(
    prefix='/books'
)

@router.get('')
def get_books(db:Session=Depends(get_db), login_user:str=Depends(get_current_user)):
    data = db.query(Books).all()
    
    return{'data':data}


@router.get('/book')
def get_certain_book(data:schemas.GetBook, db: Session=Depends(get_db)):
    book_data = db.query(Books).filter(Books.name==data.name).first()

    if not book_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with name '{data.name}' not found")

    return{'data':book_data}


@router.post('', status_code=status.HTTP_201_CREATED)
def post_book(data:schemas.BookBody, db:Session=Depends(get_db)):
    new_book = Books(name=data.name,
                     author=data.author)

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return{'data':new_book}


@router.put('/book/{book_id}', status_code=status.HTTP_200_OK)
def updated_certain_book(book_id:str, data:schemas.BookBody, db:Session=Depends(get_db)):
    book_data = db.query(Books).filter(Books.id==book_id).first()

    if not book_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id '{book_id}' doesn't exist")

    book_data.name = data.name
    book_data.author = data.author

    db.commit()
    db.refresh(book_data)

    return{'update message':book_data}


@router.delete('/book/{book_id}',status_code=status.HTTP_200_OK)
def delete_certain_book(book_id:int, db:Session=Depends(get_db)):
    book_data = db.query(Books).filter(Books.id==book_id).first()

    if not book_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Book with id '{book_id} doesn't exist")

    db.delete(book_data)
    db.commit()

    return{'message':'Book entry deleted'}