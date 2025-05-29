# Concrete Evaporation API

A FastAPI application that predicts concrete temperature and evaporation risk based on environmental conditions.

## Endpoints

### POST `/evaporation`
Takes in:
- Ambient Temp
- High/Low for past 3 days
- Humidity
- Wind speed

Returns:
- Predicted concrete temperature
- Evaporation rate
- Risk classification and flag color

## Deployment
Use Docker or Render (Docker runtime) for hosting.

## Example Deployment (Render)
- Connect your GitHub repo
- Choose Docker environment
- Port: 10000