from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from contas_a_pagar_e_receber.routers import contas_a_pagar_e_receber_router, fornecedor_cliente_router
from shared.exceptions import NotFoundExecption
from shared.exceptions_handler import not_found_exception_handler

app = FastAPI()

@app.get("/")
def oi_eu_sou_programador() -> str:
    return "Oi, eu sou programador!"

app.include_router(contas_a_pagar_e_receber_router.router)
app.include_router(fornecedor_cliente_router.router)
app.add_exception_handler(NotFoundExecption, not_found_exception_handler)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)