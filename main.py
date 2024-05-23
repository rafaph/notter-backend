import os

import uvicorn

from src.common.settings import settings

if settings.testing:
    from pytest_cov.embed import cleanup_on_sigterm  # type: ignore

    cleanup_on_sigterm()


if __name__ == "__main__":
    uvicorn.run(
        app="src.app:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.SERVER_RELOAD,
        workers=settings.SERVER_WORKERS,
        root_path=settings.SERVER_ROOT_PATH,
        proxy_headers=settings.SERVER_PROXY_HEADERS,
        log_level=os.environ.get("LOG_LEVEL", "DEBUG").lower(),
        log_config=None,
    )
