import sys
import sympy as sp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class IntegrateRequest(BaseModel):
    expression: str
    variable: str = "x"

class IntegrateResponse(BaseModel):
    result: str
    latex: str
    success: bool
    error: str = ""

@app.post("/api/integrate", response_model=IntegrateResponse)
async def integrate(request: IntegrateRequest):
    try:
        x = sp.Symbol(request.variable)
        expr = sp.sympify(request.expression)
        integral = sp.integrate(expr, x)
        return IntegrateResponse(
            result=str(integral),
            latex=sp.latex(integral),
            success=True
        )
    except Exception as e:
        return IntegrateResponse(
            result="",
            latex="",
            success=False,
            error=str(e)
        )

@app.get("/api/health")
async def health():
    return {"status": "ok"}
