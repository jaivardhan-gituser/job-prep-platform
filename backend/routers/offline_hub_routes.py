from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import Organization, OfflineForm, Submission, User
from schemas import OrganizationOut, OfflineFormOut, SubmissionCreate, SubmissionUpdate, SubmissionOut
from routers.auth_routes import get_current_user

router = APIRouter(prefix="/offline-hub", tags=["offline-hub"])


@router.get("/organizations", response_model=list[OrganizationOut])
async def list_organizations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Organization))
    return result.scalars().all()


@router.get("/forms", response_model=list[OfflineFormOut])
async def list_forms(organization_id: int | None = None, db: AsyncSession = Depends(get_db)):
    query = select(OfflineForm)
    if organization_id is not None:
        query = query.where(OfflineForm.organization_id == organization_id)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/submissions", response_model=SubmissionOut)
async def create_submission(
    submission_in: SubmissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_submission = Submission(user_id=current_user.id, form_id=submission_in.form_id)
    db.add(new_submission)
    await db.commit()
    await db.refresh(new_submission)
    return new_submission


@router.get("/submissions", response_model=list[SubmissionOut])
async def list_my_submissions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Submission).where(Submission.user_id == current_user.id))
    return result.scalars().all()


@router.patch("/submissions/{submission_id}", response_model=SubmissionOut)
async def update_submission(
    submission_id: int,
    update: SubmissionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Submission).where(Submission.id == submission_id))
    submission = result.scalar_one_or_none()
    if submission is None or submission.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Submission not found")

    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(submission, field, value)

    await db.commit()
    await db.refresh(submission)
    return submission