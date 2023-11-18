import pydantic as pyd
from ..models.basemodel import BaseModel
import pandas as pd
import numpy as np
import uuid
from typing import Optional


class SaveModel(pyd.BaseModel):
  model_config = pyd.ConfigDict(arbitrary_types_allowed=True)
  model: BaseModel
  ind: pd.DataFrame|np.ndarray
  dep: Optional[pd.DataFrame|pd.Series|np.ndarray] = None
  transformation_details: pd.DataFrame
  time: pd.Timestamp
  id: uuid.UUID
  