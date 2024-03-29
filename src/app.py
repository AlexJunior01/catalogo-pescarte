from typing import List, Optional

from fastapi import FastAPI, Depends, Query
from starlette.responses import JSONResponse

from src.database import get_db, Session
from src.models import SuggestedCommonNames, Community
from src.models.suggested_common_names import SuggestedCommonNameStatus

from src.routes.gear import router as gear_router
from src.routes.community import router as community_router
from src.routes.habitat import router as habitat_router
from src.routes.lookup import router as lookup_router

from src.schemas import SuggestCommonNameBody, SuggestedCommonNameResponse

app = FastAPI(title='Catalogo Pescarte API', version='0.0.1')

app.include_router(gear_router, tags=["Gear"])
app.include_router(community_router, tags=["Community"])
app.include_router(habitat_router, tags=["Habitat"])
app.include_router(lookup_router, tags=["Lookups"])


@app.get('/healthcheck')
async def health_check():
    return {"message": "Up and running"}


@app.get('/suggested-common-names', response_model=List[SuggestedCommonNameResponse])
async def get_suggested_common_names(
        db: Session = Depends(get_db),
        status: Optional[SuggestedCommonNameStatus] = Query(None)
):
    if status:
        suggested_names = db.query(SuggestedCommonNames).filter(SuggestedCommonNames.status == status.value).all()
    else:
        suggested_names = db.query(SuggestedCommonNames).all()
    return suggested_names


@app.post('/suggested-common-names')
async def suggest_common_name(
        suggestion: SuggestCommonNameBody,
        db: Session = Depends(get_db)
):
    community = db.query(Community).filter(Community.id == suggestion.community_id).first()
    if not community:
        return JSONResponse(
            status_code=404,
            content={"message": "Community not found"}
        )

    suggested_common_name_model = SuggestedCommonNames(
        name=suggestion.name,
        email=suggestion.email,
        suggested_name=suggestion.suggested_name,
        fish_id=suggestion.fish_id,
        community_id=suggestion.community_id
    )
    saved, error = suggested_common_name_model.save(db)

    if saved:
        return suggested_common_name_model
    else:
        return JSONResponse(
            status_code=500,
            content={"message": "Error while saving task",
                     "detail": error}
        )
