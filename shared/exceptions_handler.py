from fastapi import Request
from fastapi.responses import JSONResponse
from shared.exceptions import NotFoundExecption

async def not_found_exception_handler(request: Request, exc: NotFoundExecption):
     return JSONResponse(
        status_code=404,
        content={"message": f"Oops! {exc.name} não foi encontrado!"},
    )