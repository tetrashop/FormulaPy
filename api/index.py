import sys
import sympy as sp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

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
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None

class IntegrateResponse(BaseModel):
    result: str
    latex: str
    success: bool
    error: str = ""

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/integrate")
async def integrate(req: IntegrateRequest):
    try:
        x = sp.Symbol(req.variable)
        expr = sp.sympify(req.expression)
        if req.lower_bound is not None and req.upper_bound is not None:
            integral = sp.integrate(expr, (x, req.lower_bound, req.upper_bound))
            return {"result": str(integral), "latex": sp.latex(integral), "success": True}
        else:
            integral = sp.integrate(expr, x)
            return {"result": str(integral), "latex": sp.latex(integral), "success": True}
    except Exception as e:
        return {"result": "", "latex": "", "success": False, "error": str(e)}

# برای اطمینان از اینکه Vercel متغیر app را پیدا می‌کند
app_handler = app
