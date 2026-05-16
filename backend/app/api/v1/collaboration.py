"""Real-time collaboration API endpoints."""

from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_session
from app.models.collaboration import ThreadComment, CommentMention

router = APIRouter(prefix="/collaboration", tags=["collaboration"])


# Schemas
class ThreadCommentCreate(BaseModel):
    text: str
    patent_id: Optional[UUID] = None
    disclosure_id: Optional[UUID] = None
    parent_id: Optional[UUID] = None
    mentions: Optional[list[str]] = None  # List of user emails to mention


class ThreadCommentUpdate(BaseModel):
    text: Optional[str] = None
    resolved: Optional[bool] = None


class ThreadCommentResponse(BaseModel):
    id: UUID
    text: str
    user_name: str
    user_email: str
    resolved: bool
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class CommentThreadResponse(BaseModel):
    patent_id: Optional[UUID]
    disclosure_id: Optional[UUID]
    comments: list[ThreadCommentResponse]
    total_count: int


# Endpoints
@router.post("", response_model=ThreadCommentResponse)
async def create_comment(
    comment: ThreadCommentCreate,
    user_id: str = Query(...),
    user_name: str = Query(...),
    user_email: str = Query(...),
    session: AsyncSession = Depends(get_session),
):
    """Create comment on patent or disclosure."""
    if not comment.patent_id and not comment.disclosure_id:
        raise HTTPException(
            status_code=400,
            detail="Either patent_id or disclosure_id must be provided",
        )

    db_comment = ThreadComment(
        id=uuid4(),
        patent_id=comment.patent_id,
        disclosure_id=comment.disclosure_id,
        parent_id=comment.parent_id,
        user_id=user_id,
        user_name=user_name,
        user_email=user_email,
        text=comment.text,
    )
    session.add(db_comment)
    await session.commit()
    await session.refresh(db_comment)

    # Handle mentions
    if comment.mentions:
        for mentioned_email in comment.mentions:
            mention = CommentMention(
                id=uuid4(),
                comment_id=db_comment.id,
                mentioned_user_email=mentioned_email,
                mentioned_user_name=mentioned_email.split("@")[0],  # Extract name from email
            )
            session.add(mention)
        await session.commit()

    return db_comment


@router.get("/{comment_id}", response_model=ThreadCommentResponse)
async def get_comment(
    comment_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Get comment by ID."""
    result = await session.execute(select(ThreadComment).where(ThreadComment.id == comment_id))
    comment = result.scalar_one_or_none()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.put("/{comment_id}", response_model=ThreadCommentResponse)
async def update_comment(
    comment_id: UUID,
    comment: ThreadCommentUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Update comment."""
    result = await session.execute(select(ThreadComment).where(ThreadComment.id == comment_id))
    db_comment = result.scalar_one_or_none()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.text is not None:
        db_comment.text = comment.text
        db_comment.edited_at = datetime.utcnow()
    if comment.resolved is not None:
        db_comment.resolved = comment.resolved

    await session.commit()
    await session.refresh(db_comment)
    return db_comment


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Delete comment."""
    result = await session.execute(select(ThreadComment).where(ThreadComment.id == comment_id))
    db_comment = result.scalar_one_or_none()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    await session.delete(db_comment)
    await session.commit()
    return {"status": "deleted", "id": str(comment_id)}


@router.get("/patent/{patent_id}/thread", response_model=CommentThreadResponse)
async def get_patent_comments(
    patent_id: UUID,
    include_resolved: bool = Query(False),
    session: AsyncSession = Depends(get_session),
):
    """Get all comments on a patent (with threads)."""
    query = select(ThreadComment).where(
        and_(
            ThreadComment.patent_id == patent_id,
            ThreadComment.parent_id == None,  # Only root comments
        )
    )

    if not include_resolved:
        query = query.where(ThreadComment.resolved == False)

    query = query.order_by(ThreadComment.created_at.desc())
    result = await session.execute(query)
    comments = result.scalars().all()

    return {
        "patent_id": patent_id,
        "disclosure_id": None,
        "comments": comments,
        "total_count": len(comments),
    }


@router.get("/disclosure/{disclosure_id}/thread", response_model=CommentThreadResponse)
async def get_disclosure_comments(
    disclosure_id: UUID,
    include_resolved: bool = Query(False),
    session: AsyncSession = Depends(get_session),
):
    """Get all comments on a disclosure."""
    query = select(ThreadComment).where(
        and_(
            ThreadComment.disclosure_id == disclosure_id,
            ThreadComment.parent_id == None,
        )
    )

    if not include_resolved:
        query = query.where(ThreadComment.resolved == False)

    query = query.order_by(ThreadComment.created_at.desc())
    result = await session.execute(query)
    comments = result.scalars().all()

    return {
        "patent_id": None,
        "disclosure_id": disclosure_id,
        "comments": comments,
        "total_count": len(comments),
    }


@router.get("/{comment_id}/replies", response_model=list[ThreadCommentResponse])
async def get_comment_replies(
    comment_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Get replies to a comment (thread view)."""
    query = select(ThreadComment).where(ThreadComment.parent_id == comment_id).order_by(ThreadComment.created_at.asc())
    result = await session.execute(query)
    return result.scalars().all()


@router.get("/mentions/{user_email}")
async def get_user_mentions(
    user_email: str,
    unread_only: bool = Query(True),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
):
    """Get @mentions for a user."""
    query = select(CommentMention).where(CommentMention.mentioned_user_email == user_email)

    if unread_only:
        query = query.where(CommentMention.read == False)

    query = query.order_by(CommentMention.created_at.desc()).limit(limit)
    result = await session.execute(query)
    mentions = result.scalars().all()

    return {
        "user_email": user_email,
        "total_mentions": len(mentions),
        "unread_count": sum(1 for m in mentions if not m.read),
        "mentions": mentions,
    }


@router.post("/mentions/{mention_id}/read")
async def mark_mention_read(
    mention_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    """Mark mention as read."""
    result = await session.execute(select(CommentMention).where(CommentMention.id == mention_id))
    mention = result.scalar_one_or_none()
    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")

    mention.read = True
    await session.commit()
    return {"status": "marked_read", "mention_id": str(mention_id)}
