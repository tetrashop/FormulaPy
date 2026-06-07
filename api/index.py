import sympy as sp
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="FormulaPy API", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExprRequest(BaseModel):
    expression: str
    variable: str = "x"

class IntegrateRequest(ExprRequest):
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None
    numeric_if_fails: bool = True

class DerivativeRequest(ExprRequest):
    order: int = 1

class LimitRequest(ExprRequest):
    point: float = 0
    direction: str = "+"  # +, -, +-

class SeriesRequest(ExprRequest):
    point: float = 0
    order: int = 5

# ---------- انتگرال ----------
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

# ---------- مشتق ----------
@app.post("/api/derivative")
async def derivative(req: DerivativeRequest):
    try:
        x = sp.Symbol(req.variable)
        expr = sp.sympify(req.expression)
        deriv = sp.diff(expr, x, req.order)
        return {"result": str(deriv), "latex": sp.latex(deriv), "success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ---------- حد ----------
@app.post("/api/limit")
async def limit(req: LimitRequest):
    try:
        x = sp.Symbol(req.variable)
        expr = sp.sympify(req.expression)
        dir_sym = None
        if req.direction == "+":
            dir_sym = '+'
        elif req.direction == "-":
            dir_sym = '-'
        lim = sp.limit(expr, x, req.point, dir_sym)
        return {"result": str(lim), "latex": sp.latex(lim), "success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ---------- بسط سری ----------
@app.post("/api/series")
async def series(req: SeriesRequest):
    try:
        x = sp.Symbol(req.variable)
        expr = sp.sympify(req.expression)
        ser = sp.series(expr, x, req.point, req.order)
        return {"result": str(ser), "latex": sp.latex(ser), "success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ---------- ساده‌سازی ----------
@app.post("/api/simplify")
async def simplify(req: ExprRequest):
    try:
        x = sp.Symbol(req.variable)
        expr = sp.sympify(req.expression)
        simp = sp.simplify(expr)
        return {"result": str(simp), "latex": sp.latex(simp), "success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ---------- بسط جبری ----------
@app.post("/api/expand")
async def expand(req: ExprRequest):
    try:
        x = sp.Symbol(req.variable)
        expr = sp.sympify(req.expression)
        expd = sp.expand(expr)
        return {"result": str(expd), "latex": sp.latex(expd), "success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ---------- سلامت ----------
@app.get("/api/health")
async def health():
    return {"status": "ok", "engine": "SymPy", "endpoints": ["integrate", "derivative", "limit", "series", "simplify", "expand"]}
