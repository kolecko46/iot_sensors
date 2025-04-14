from modules import config
# import config
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from modules.schemas import TokenData

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCES_TOKEN_EXPIRE_TIME = int(config.ACCES_TOKEN_EXPIRE_TIME)

user_data = {'user_id':'6',
             'user_role':'admin'}

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data):
    data_to_encode = data.copy()

    expire_time = datetime.now(UTC) + timedelta(minutes=ACCES_TOKEN_EXPIRE_TIME)
    data_to_encode.update({'exp':expire_time})

    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

access_token = create_access_token(user_data)


def verify_access_token(token:str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        payload_id:str = str(payload.get('user_id'))

        if payload_id is None:
            raise credentials_exceptions

        token_data = TokenData(id=payload_id)

    except JWTError:
        raise credentials_exceptions

    return token_data

def get_current_user(token:str=Depends(oauth2_schema)):
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail='Could not valid credentials',
                                           headers={"WWW-authenticate":"Bearer"})
    
    return verify_access_token(token, credentials_exceptions)