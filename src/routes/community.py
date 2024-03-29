from uuid import UUID
from typing import List

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse, Response

from src.database import get_db, Session
from src.models import Community
from src.schemas import ErrorMessage
from src.schemas.community import CommunityInput, CommunityPatchInput, CommunityOutput

router = APIRouter(prefix='/community')


@router.get('/', response_model=List[CommunityOutput])
async def get_all_communities(db: Session = Depends(get_db)):
    return Community.get_all(db)


@router.get('/{community_id}', response_model=CommunityOutput, responses={404: {'model': ErrorMessage}})
async def get_community(
        community_id: UUID,
        db: Session = Depends(get_db)
):
    community = Community.get_by_id(db, community_id)
    if community:
        return community
    else:
        return JSONResponse(
            status_code=404,
            content={"message": "Community not found"}
        )


@router.post('/', response_model=CommunityOutput)
async def create_community(
        community: CommunityInput,
        db: Session = Depends(get_db)
):
    community_model = Community(**community.dict())
    saved, error = community_model.save(db)

    if saved:
        return saved
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving community",
                     "detail": error}
        )


@router.patch('/{community_id}', response_model=CommunityOutput, responses={404: {'model': ErrorMessage}})
async def update_community(
        community_id: UUID,
        community_payload: CommunityPatchInput,
        db: Session = Depends(get_db)
):
    community = Community.get_by_id(db, community_id)

    if not community:
        return JSONResponse(
            status_code=404,
            content={"message": "community not found"}
        )

    updated, error = community.update(db, community_payload.dict(exclude_none=True))

    if updated:
        return updated
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating community",
                     "detail": error}
        )


@router.delete('/{community_id}', status_code=204, response_class=Response, responses={404: {'model': ErrorMessage}})
async def delete_community(
        community_id: UUID,
        db: Session = Depends(get_db)
):
    community = Community.get_by_id(db, community_id)

    if not community:
        return JSONResponse(
            status_code=404,
            content={"message": "Community not found"}
        )

    deleted, error = community.delete(db)

    if deleted:
        return None
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while updating community",
                     "detail": error}
        )
