from fastapi import APIRouter,  HTTPException, status, Depends
from .. import schemas, database, models, token
from sqlalchemy.orm import Session
from ..hashing import Hash
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm


router =  APIRouter(
    tags=['Authentication']
)



@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Invalid Credentials"
        )
    
    if not Hash.verify(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect password"
        )

    # generate a jwt 
    
    access_token = token.create_access_token(
        data={"sub": user.email},
    
    )
    return {"access_token": access_token, "token_type": "bearer"}


    
