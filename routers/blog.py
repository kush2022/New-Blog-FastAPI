from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, database, models
from .. OAuth2 import get_current_user

router = APIRouter(
    tags=['Blog'],
    prefix='/blog'
)

get_db = database.get_db

# get the blogs from the database 
@router.get('/', status_code=status.HTTP_200_OK)
async def blogs(db: Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()

    return blogs



@router.post("/", status_code=status.HTTP_201_CREATED)
async def createBlog(request: schemas.Blog, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):

    newBlog = models.Blog(title=request.title, body=request.body, creator_id=1)

    db.add(newBlog)
    db.commit()
    db.refresh(newBlog)


    return newBlog



# get a single blog 
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
async def blog(id, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog not found"
        )

    return blog


# delete blog 
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def deleteBlog(id, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog.delete(synchronize_session=False)
    db.commit()

    return "done"


# update blog 
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id, request: schemas.Blog, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog.update(request, synchronize_session=False)
    
    
    db.commit()


    return "updated"

