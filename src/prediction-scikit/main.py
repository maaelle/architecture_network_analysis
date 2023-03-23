import warnings

from constants import MODEL_PATH
from fs import load_model

warnings.filterwarnings("ignore")


def lambda_handler(event):
    model = load_model(MODEL_PATH)
