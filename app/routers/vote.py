from fastapi import Depends, status, HTTPException, APIRouter
from app import schemas
from sqlalchemy.orm import Session
from app.database import get_db
from app.oauth2 import get_current_user
from app import models, schemas

router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("/")
def add_vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f"user has alreasy vote"
            )
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote successfully added"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"vote not found"
            )
        vote_query.delete()
        return {"message": "successfully deleted"}
