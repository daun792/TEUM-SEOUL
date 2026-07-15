from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Post
from app.schemas.posts import PasswordConfirm, PostCreate, PostPage, PostRead, PostUpdate
from app.services.passwords import hash_password, verify_password

router = APIRouter(prefix="/api/posts", tags=["posts"])


def _get_post_or_404(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def _verify_or_403(post: Post, password: str) -> None:
    if not verify_password(password, post.password_hash):
        raise HTTPException(status_code=403, detail="Password does not match")


@router.get("", response_model=PostPage)
def list_posts(
    q: str | None = Query(default=None, max_length=100),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    filters = []
    if q:
        keyword = f"%{q.strip()}%"
        filters.append(or_(Post.title.ilike(keyword), Post.content.ilike(keyword)))
    total = db.scalar(select(func.count()).select_from(Post).where(*filters)) or 0
    posts = db.scalars(
        select(Post)
        .where(*filters)
        .order_by(Post.created_at.desc(), Post.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    ).all()
    return PostPage(
        items=[PostRead.model_validate(post) for post in posts],
        total=total,
        page=page,
        size=size,
        pages=ceil(total / size) if total else 0,
    )


@router.get("/{post_id}", response_model=PostRead)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return _get_post_or_404(db, post_id)


@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    post = Post(
        title=payload.title.strip(),
        content=payload.content.strip(),
        author=payload.author.strip() or "익명",
        password_hash=hash_password(payload.password),
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.post("/{post_id}/verify-password", status_code=status.HTTP_204_NO_CONTENT)
def verify_post_password(post_id: int, payload: PasswordConfirm, db: Session = Depends(get_db)):
    post = _get_post_or_404(db, post_id)
    _verify_or_403(post, payload.password)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=PostRead)
def update_post(post_id: int, payload: PostUpdate, db: Session = Depends(get_db)):
    post = _get_post_or_404(db, post_id)
    _verify_or_403(post, payload.password)
    post.title = payload.title.strip()
    post.content = payload.content.strip()
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, payload: PasswordConfirm, db: Session = Depends(get_db)):
    post = _get_post_or_404(db, post_id)
    _verify_or_403(post, payload.password)
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
