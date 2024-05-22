from fastapi import APIRouter, status

router = APIRouter(tags=["common"])


@router.get(
    "/healthz",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Health check",
    description="Health check operation",
    response_description="Health checked successfully",
)
async def get_healthz() -> None: ...
