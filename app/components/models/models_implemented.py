from .regression import statistical as stat
from .regression import ml
from .regression import bayesian as bayes
from .basemodel import BaseModel

IMPLEMENTED_MODELS = {
  'None': BaseModel,
  'OLS': stat.OLS,
  'Fixed Effects': stat.MixedEffects,
}