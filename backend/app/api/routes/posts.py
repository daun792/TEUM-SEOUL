from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.post import Post
from app.models.post_like import PostLike
from app.schemas.post import (
    LikeToggleResult,
    PasswordPayload,
    PostCreate,
    PostList,
    PostRead,
    PostUpdate,
)

router = APIRouter(tags=["posts"])


def _get_post(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return post


@router.get("/posts", response_model=PostList)
def list_posts(
    q: str = Query(default="", max_length=100),
    category: str = Query(default=""),
    ids: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
) -> PostList:
    query = select(Post)
    count_query = select(func.count()).select_from(Post)
    if q.strip():
        pattern = f"%{q.strip()}%"
        condition = or_(Post.title.ilike(pattern), Post.content.ilike(pattern))
        query = query.where(condition)
        count_query = count_query.where(condition)
    if category:
        query = query.where(Post.category == category)
        count_query = count_query.where(Post.category == category)
    if ids:
        try:
            id_values = [int(value) for value in ids.split(",") if value]
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="북마크 ID 형식이 올바르지 않습니다.") from exc
        query = query.where(Post.id.in_(id_values))
        count_query = count_query.where(Post.id.in_(id_values))
    total = db.scalar(count_query) or 0
    items = db.scalars(
        query.order_by(Post.created_at.desc()).offset((page - 1) * size).limit(size)
    ).all()
    return PostList(
        total=total,
        page=page,
        size=size,
        items=[PostRead.model_validate(item) for item in items],
    )


@router.get("/posts/{post_id}", response_model=PostRead)
def get_post(post_id: int, db: Session = Depends(get_db)) -> PostRead:
    post = _get_post(db, post_id)
    post.view_count += 1
    db.commit()
    db.refresh(post)
    return PostRead.model_validate(post)


@router.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, db: Session = Depends(get_db)) -> PostRead:
    post = Post(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return PostRead.model_validate(post)


@router.put("/posts/{post_id}", response_model=PostRead)
def update_post(post_id: int, payload: PostUpdate, db: Session = Depends(get_db)) -> PostRead:
    post = _get_post(db, post_id)
    if payload.password != post.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")
    for field, value in payload.model_dump().items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return PostRead.model_validate(post)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, payload: PasswordPayload, db: Session = Depends(get_db)) -> Response:
    post = _get_post(db, post_id)
    if payload.password != post.password:
        raise HTTPException(status_code=403, detail="비밀번호가 일치하지 않습니다.")
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/posts/{post_id}/likes/toggle", response_model=LikeToggleResult)
def toggle_like(
    post_id: int,
    x_client_id: str = Header(min_length=8, max_length=64),
    db: Session = Depends(get_db),
) -> LikeToggleResult:
    post = _get_post(db, post_id)
    existing = db.scalar(
        select(PostLike).where(
            PostLike.post_id == post_id,
            PostLike.client_id == x_client_id,
        )
    )
    if existing:
        db.delete(existing)
        liked = False
    else:
        db.add(PostLike(post_id=post_id, client_id=x_client_id))
        liked = True
    db.flush()
    count = db.scalar(
        select(func.count()).select_from(PostLike).where(PostLike.post_id == post_id)
    ) or 0
    post.like_count = count
    db.commit()
    return LikeToggleResult(liked=liked, like_count=count)
