import sympy as sp
import numpy as np
from scipy.integrate import quad
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import math

app = FastAPI(title="FormulaPy - Symbolic Integrator", version="3.0")

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
    numeric_if_fails: bool = True

class IntegrateResponse(BaseModel):
    result: str
    latex: str
    numeric_value: Optional[float] = None
    success: bool
    error: str = ""

@app.post("/api/integrate", response_model=IntegrateResponse)
async def integrate(req: IntegrateRequest):
    try:
        x = sp.Symbol(req.variable)
        expr = sp.sympify(req.expression)
        
        # انتگرال معین یا نامعین
        if req.lower_bound is not None and req.upper_bound is not None:
            # ابتدا تلاش نمادین
            try:
                integral = sp.integrate(expr, (x, req.lower_bound, req.upper_bound))
                numeric = float(integral) if integral.is_number else None
                return IntegrateResponse(
                    result=str(integral),
                    latex=sp.latex(integral),
                    numeric_value=numeric,
                    success=True
                )
            except Exception:
                if req.numeric_if_fails:
                    # انتگرال‌گیری عددی با SciPy
                    f = sp.lambdify(x, expr, modules=['numpy'])
                    try:
                        val, _ = quad(f, req.lower_bound, req.upper_bound)
                        return IntegrateResponse(
                            result="",
                            latex="",
                            numeric_value=val,
                            success=True
                        )
                    except Exception as e:
                        return IntegrateResponse(
                            result="", latex="", success=False, error=f"Numerical integration failed: {str(e)}"
                        )
                else:
                    raise
        else:
            # انتگرال نامعین
            integral = sp.integrate(expr, x)
            return IntegrateResponse(
                result=str(integral),
                latex=sp.latex(integral),
                success=True
            )
    except Exception as e:
        return IntegrateResponse(result="", latex="", success=False, error=str(e))

@app.get("/api/health")
async def health():
    return {"status": "ok", "engine": "SymPy", "version": sp.__version__}

@app.get("/api/expand")
async def expand(expr: str, variable: str = "x"):
    try:
        x = sp.Symbol(variable)
        e = sp.sympify(expr)
        expanded = sp.expand(e)
        return {"result": str(expanded), "latex": sp.latex(expanded), "success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/simplify")
async def simplify(expr: str, variable: str = "x"):
    try:
        x = sp.Symbol(variable)
        e = sp.sympify(expr)
        simplified = sp.simplify(e)
        return {"result": str(simplified), "latex": sp.latex(simplified), "success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/derivative")
async def derivative(expr: str, variable: str = "x", order: int = 1):
    try:
        x = sp.Symbol(variable)
        e = sp.sympify(expr)
        deriv = sp.diff(e, x, order)
        return {"result": str(deriv), "latex": sp.latex(deriv), "success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/limit")
async def limit(expr: str, variable: str = "x", point: float = 0, direction: str = "+"):
    try:
        x = sp.Symbol(variable)
        e = sp.sympify(expr)
        dir_sym = '+' if direction == '+' else '-'
        lim = sp.limit(e, x, point, dir_sym)
        return {"result": str(lim), "latex": sp.latex(lim), "success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/api/series")
async def series(expr: str, variable: str = "x", point: float = 0, order: int = 5):
    try:
        x = sp.Symbol(variable)
        e = sp.sympify(expr)
        ser = sp.series(e, x, point, order)
        return {"result": str(ser), "latex": sp.latex(ser), "success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}
