from .regression import statistical as stat
from .regression import ml
from .regression import bayesian as bayes

IMPLEMENTED_MODELS = {
  'OLS': stat.OLS,
  'Fixed Effects': stat.MixedEffects,
}