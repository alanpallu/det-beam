from typing import Optional, List, Dict
from typing_extensions import Literal
from pydantic import BaseModel, Field

class FormInput(BaseModel):
    largura: int
    altura: int
