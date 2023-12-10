import pydantic as pyd
from ..models.basemodel import BaseModel
import pandas as pd
import numpy as np
import uuid
from typing import Optional


class SaveModel(pyd.BaseModel):
  model_config = pyd.ConfigDict(arbitrary_types_allowed=True)
  model: BaseModel
  time: pd.Timestamp
  id: uuid.UUID
  