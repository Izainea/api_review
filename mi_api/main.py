from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="API de Predicción", description="API para predecir el ingreso de una persona", version="1.0")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int,q: str = None):
    return {"item_id": item_id, "q": q, }

## HAcemos la ruta para consultar por Player en el dataset
@app.get("/players/{player_name}")
async def get_player(player_name: str):
    ## Cargamos el dataset
    df = pd.read_csv("Datos/Copa_Libertadores_2023_Complete_Goal_Scorers.csv")
    ## Consultamos por el jugador
    player = df[df["Player"].str.lower() == player_name.lower().replace("_", " ")]
    ## Si el jugador no existe, retornamos un mensaje
    if player.shape[0] == 0:
        return {"message": "Player not found"}
    ## Si el jugador existe, retornamos sus datos
    return player.to_dict(orient="records")

@app.get("/teams/{team_name}")
async def get_team(team_name: str):
    df = pd.read_csv("Datos/Copa_Libertadores_2023_Complete_Goal_Scorers.csv")
    team = df[df["Team"].str.lower() == team_name.lower().replace("_", " ")]
    if team.shape[0] == 0:
        return {"message": "Team not found"}
    return team.to_dict(orient="records")

### Mejores 10 jugadores
@app.get("/top_players")
async def get_top_players():
    df = pd.read_csv("Datos/Copa_Libertadores_2023_Complete_Goal_Scorers.csv")
    top_players = df.sort_values("Goals", ascending=False).head(10)
    return top_players.to_dict(orient="records")

### Mejores 10 equipos
@app.get("/top_teams")
async def get_top_teams():
    df = pd.read_csv("Datos/Copa_Libertadores_2023_Complete_Goal_Scorers.csv")
    top_teams = df.groupby("Team")["Goals"].sum().reset_index().sort_values("Goals", ascending=False).head(10)
    return top_teams.to_dict(orient="records")

### Todo el dataset
@app.get("/all_data")
async def get_all_data():
    df = pd.read_csv("Datos/Copa_Libertadores_2023_Complete_Goal_Scorers.csv")
    return df.to_dict(orient="records")



# Clase para recibir los datos de entrada
class Item(BaseModel):
    age: int
    workclass: str
    education: str
    education_num: int
    marital_status: str
    occupation: str
    relationship: str
    race: str
    sex: str
    capital_gain: int
    capital_loss: int
    hours_per_week: int
    native_country: str

## Cargar el modelo

model= joblib.load('Cuadernos/pipeline.pkl') # O el nombre correcto como pipeline.joblib

@app.post("/predict")
def predict(item: Item):
    diccionario_entrada = {
        'age': [item.age],
        'workclass': [item.workclass],
        'education': [item.education],
        'education-num': [item.education_num],
        'marital-status': [item.marital_status],
        'occupation': [item.occupation],
        'relationship': [item.relationship],
        'race': [item.race],
        'sex': [item.sex],
        'capital-gain': [item.capital_gain],
        'capital-loss': [item.capital_loss],
        'hours-per-week': [item.hours_per_week],
        'native-country': [item.native_country]
    }

    df= pd.DataFrame(diccionario_entrada)
    prediccion= model.predict_proba(df)

    return {"prediccion": prediccion[0][1].item() if hasattr(prediccion[0][1], "item") else prediccion[0][1]}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)