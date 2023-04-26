from typing import List, Optional
from fastapi import APIRouter, Body, Depends, Path, Query, Request, Response, Form, HTTPException
from controllers.calculation_control import CalculatorControl
from models.calculation_model import FormInput

api_calculate = APIRouter(prefix='/calculate')

@api_calculate.post('/')
async def calculations(request: Request, dados: FormInput = Body(None, description='FormInput')):
    try:
        res = CalculatorControl().perform_calculations(dados=dados)
        return res
    except Exception as e:
        print(e)
