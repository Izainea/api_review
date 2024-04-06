from fastapi import FastAPI
import uvicorn
import pandas as pd

## Creamos la instancia de FastAPI
app = FastAPI(debug=True, title="Mi primera API",summary="Esto es un resumen",description="Esto es una descripción")
## Vamos a hacer un api para consultar los datos de el dataset "Datos/Copa_Libertadores_2023_Complete_Goal_Scorers.csv"

@app.get("/")
async def root():
    return {"message": "Hello World"}

## async def es para que la función sea asincrona, es decir, 
## que se ejecute en segundo plano, para que no se bloquee el servidor

## HAcemos la ruta para consultar por Player en el dataset
@app.get("/players/{player_name}")
async def get_player(player_name: str):
    ## Cargamos el dataset
    df = pd.read_csv("../Datos/Copa_Libertadores_2023_Complete_Goal_Scorers.csv")
    ## Consultamos por el jugador
    player = df[df["Player"].str.lower() == player_name.lower().replace("_", " ")]
    ## Si el jugador no existe, retornamos un mensaje
    if player.shape[0] == 0:
        return {"message": "Player not found"}
    ## Si el jugador existe, retornamos sus datos
    return player.to_dict(orient="records")

@app.get("/teams/{team_name}")
async def get_team(team_name: str):
    df = pd.read_csv("../Datos/Copa_Libertadores_2023_Complete_Goal_Scorers.csv")
    team = df[df["Team"].str.lower() == team_name.lower().replace("_", " ")]
    if team.shape[0] == 0:
        return {"message": "Team not found"}
    return team.to_dict(orient="records")

### Mejores 10 jugadores
@app.get("/top_players")
async def get_top_players():
    df = pd.read_csv("../Datos/Copa_Libertadores_2023_Complete_Goal_Scorers.csv")
    top_players = df.sort_values("Goals", ascending=False).head(10)
    return top_players.to_dict(orient="records")

### Mejores 10 equipos
@app.get("/top_teams")
async def get_top_teams():
    df = pd.read_csv("../Datos/Copa_Libertadores_2023_Complete_Goal_Scorers.csv")
    top_teams = df.groupby("Team")["Goals"].sum().reset_index().sort_values("Goals", ascending=False).head(10)
    return top_teams.to_dict(orient="records")

### Todo el dataset
@app.get("/all_data")
async def get_all_data():
    df = pd.read_csv("../Datos/Copa_Libertadores_2023_Complete_Goal_Scorers.csv")
    return df.to_dict(orient="records")




### Terminamos de definir la API
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)