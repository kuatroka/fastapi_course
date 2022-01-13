from .. import models, schemas, utils
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel

# DB stuff
from ..database import get_db
from app import schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):
    print(limit)

    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(
            limit=limit).offset(skip).all()

    results = db.query(models.Post,
                       func.count(models.Vote.post_id).label("votes")).join(
                           models.Vote,
                           models.Vote.post_id == models.Post.id,
                           isouter=True).group_by(models.Post.id).filter(
                               models.Post.title.contains(search)).limit(
                                   limit=limit).offset(skip).all()

    print(results)
    return results


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    # post = db.query(models.Post).filter(models.Post.id == id)

    post = db.query(models.Post,
                    func.count(models.Vote.post_id).label("votes")).join(
                        models.Vote,
                        models.Vote.post_id == models.Post.id,
                        isouter=True).group_by(models.Post.id).filter(
                            models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    # if post.first().owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #             detail="Not authorised to perform this action")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if not deleted_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised to perform this action")

    deleted_post.delete(synchronize_session=False)
    db.commit()
    return {'message': f'post with id: {id} was succesfully deleted'}


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int,
                post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if updated_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorised \
        to perform this action")

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()