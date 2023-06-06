from typing import List, Optional
from fastapi import APIRouter, Body, Depends, Path, Query, Request, Response, Form, HTTPException
from controllers.calculation_control import CalculatorControl
from models.calculation_model import FormInput


api_calculate = APIRouter(prefix='/calculate')


@api_calculate.post('/')
async def calculations(request: Request, dados: FormInput):
    try:
        res = CalculatorControl().perform_calculations(dados=dados)
        return res
    except Exception as e:
        print(e)


@api_calculate.post("/structure-plot/")
async def plot_structure(request: Request, dados: FormInput):
    res = CalculatorControl().perform_calculations(dados=dados, tipo_resultado='plot', tipo_plot='structure')
    return res


@api_calculate.post("/bending-moment-plot/")
async def plot_bending_moment(request: Request, dados: FormInput):
    try:
        res = CalculatorControl().perform_calculations(dados=dados, tipo_resultado='plot', tipo_plot='moment')
        return res
    except Exception as e:
        print(e)


@api_calculate.post("/shear-force-plot/")
async def plot_shear_force(request: Request, dados: FormInput):
    res = CalculatorControl().perform_calculations(dados=dados, tipo_resultado='plot', tipo_plot='shear')
    return res
