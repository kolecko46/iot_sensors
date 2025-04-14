import modules.schemas as schemas
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from modules.database_connector import get_db
from modules.models import Base, Users
from modules.utils import password_hashing, verify_password
from modules.oauth2 import create_access_token
from sqlalchemy.orm import Session

router= APIRouter()

@router.post('/registration')
def reg_user(data:schemas.User, db:Session=Depends(get_db)):
    hashed_password = password_hashing(data.password)

    new_user = Users(name=data.name,
                     password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return{'message':f"new user '{data.name}' created"}


@router.post('/login', response_model=schemas.Token)
def login_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user = db.query(Users).filter(Users.name==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid credentials') 

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid credentials')

    access_token = create_access_token({'user_id':user.id})

    return{'access_token':access_token, 'token_type':'Bearer'}