import string
import json

from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from models.FuncionariosModel import FuncionariosModel

from models.QuartoModel import QuartoModel
app = FastAPI()
url = 'mongodb+srv://marceloakohlhase:6nZdVHRyJp6yBLDK@reconhecimento.dav0i6n.mongodb.net/?retryWrites=true&w=majority'
Connection = MongoClient(url).reconhecimento


@app.get("/")
async def home():
    return {"message": "Hello World"}

########################## QUARTOS #########################


@app.get("/quarto")
async def GET():
    return {"message": "Sucess"}


@app.post("/quarto")
async def POST(quarto: QuartoModel):
    resposta = Connection.Quartos.find_one({"bedroom": quarto.bedroom})
    if(resposta):
         return {"message": "Quarto já cadastrado"
            }
    else:
        Connection.Quartos.insert_one(
        {"bedroom": quarto.bedroom, "occupied": quarto.occupied})
        return {"message": "Quarto cadastrado com sucesso"}
   
  


@app.put("/quarto")
async def UPDATE():
    return {"message": "Atualizar Quarto"}


@app.delete("/quarto")
async def DELETE():
    Connection.Quartos.delete_one({""})
    return {"message": "Deletar Quarto"}



########################## FUNCIONARIOS #########################

@app.get("/funcionario")
async def GET():
    return {"message": "Sucess"}


@app.post("/funcionario")
async def POST(funcionarios: FuncionariosModel):

    Connection.Funcionarios.insert_one(
        {"Function": funcionarios.Function, "CostPerHour": funcionarios.CostPerHour})
    return {"message": "Adicionado com sucesso"}


@app.put("/funcionario")
async def UPDATE():
    return {"message": "Atualizar funcionario"}


@app.delete("/funcionario")
async def DELETE():
    
    return {"message": "Deletar funcionario"}