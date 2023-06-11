from typing import Optional, List, Dict
from typing_extensions import Literal
from pydantic import BaseModel, Field

class FormInput(BaseModel):
    comprimento: str
    largura: str
    altura: str
    classeConcreto: str
    classeAgressividade: str
    combAcoes: str
    constanteMolaEsq: str
    constanteMolaDir: str
    tramos: List
    cargas: List
