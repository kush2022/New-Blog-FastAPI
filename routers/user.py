from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import database, schemas, models
from ..hashing import Hash

router = APIRouter(
     tags=['User'],
     prefix='/user'
)

get_db = database.get_db



@router.post('/', response_model=schemas.ShowUser)
async def createUser(request: schemas.User, db: Session=Depends(get_db)):

    

    newUser = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))

    db.add(newUser)
    db.commit()
    db.refresh(newUser)  

    return newUser


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail="User not found")
    
    return user

