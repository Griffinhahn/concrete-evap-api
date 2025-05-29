
from fastapi import FastAPI
from pydantic import BaseModel
import math

app = FastAPI()

# Linear regression model coefficients from training
COEFFICIENTS = {
    'Ambient Temp': 0.265247262821375,
    'Phigh': 0.09026664432083344,
    'Plow': 0.07795810660749394,
    '2High': -0.06126155201789177,
    '2Low': 0.062033376197684224,
    '3High': -0.04796402318852745,
    '3Low': 0.1467509219942576
}
INTERCEPT = 0  # You can update this if available

# Input schema
class EvaporationInput(BaseModel):
    ambient_temp: float
    phigh: float
    plow: float
    high2: float
    low2: float
    high3: float
    low3: float
    rh: float  # relative humidity
    wind: float  # wind speed

# Risk classification with beach flag colors
def classify_evaporation_risk(rate):
    if rate <= 0.1:
        return {"level": "Safe", "flag": "Green"}
    elif rate <= 0.175:
        return {"level": "Caution", "flag": "Yellow"}
    elif rate <= 0.25:
        return {"level": "Severe", "flag": "Red"}
    else:
        return {"level": "Concrete Death", "flag": "Black"}

# Concrete temperature prediction
def predict_concrete_temp(data: EvaporationInput):
    return sum([
        COEFFICIENTS['Ambient Temp'] * data.ambient_temp,
        COEFFICIENTS['Phigh'] * data.phigh,
        COEFFICIENTS['Plow'] * data.plow,
        COEFFICIENTS['2High'] * data.high2,
        COEFFICIENTS['2Low'] * data.low2,
        COEFFICIENTS['3High'] * data.high3,
        COEFFICIENTS['3Low'] * data.low3,
    ]) + INTERCEPT

# Evaporation rate formula
def calculate_evaporation_rate(tc, ta, rh, wind):
    evap = ((tc ** 2.5) - ((rh / 100) * (ta ** 2.5))) * (1 + (0.4 * wind)) * 0.000001
    return round(evap, 6)

@app.post("/evaporation")
def compute_evaporation(input_data: EvaporationInput):
    concrete_temp = predict_concrete_temp(input_data)
    evap_rate = calculate_evaporation_rate(
        concrete_temp,
        input_data.ambient_temp,
        input_data.rh,
        input_data.wind
    )
    risk_info = classify_evaporation_risk(evap_rate)
    return {
        "predicted_concrete_temp": round(concrete_temp, 2),
        "evaporation_rate": evap_rate,
        "risk_level": risk_info["level"],
        "flag_color": risk_info["flag"]
    }
