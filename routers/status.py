from fastapi import APIrouter, Depends
from ..modules.database_connector import check_db_connection, get_db

router = APIrouter()

@router.get('/status')
def get_status(db:Session=Depends(get_db)):
    pass