from datetime import datetime
import string
import json
from urllib import response

from fastapi import FastAPI
from pydantic import Json
from pymongo import MongoClient
from bson import BSON, ObjectId
from models.FluxosDeHorasModel import Fluxosdehorasmodel
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
    response = Connection.Quartos.find()
    lista = (str(list(response)))
    return {"message": lista}


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
async def UPDATE(id: str, status: bool):
    if(not id):
        return {"message": "Id não informado"}
    if(not status):
        return {"message": "Status não informado"}

    response = Connection.Quartos.find_one({"_id": ObjectId(id)})
    if(response):
        Connection.Quartos.update_one({"_id": ObjectId(id)}, {
                                      "$set": {"occupied": status}})
        return {"message": "Atualizar Quarto"}
    else:
        return {"message": "Quarto não encontrado"}

    # print(resposta)


@app.delete("/quarto")
async def DELETE(id: str):
    if(not id):
        return {"message": "Id não informado"}

    response = Connection.Quartos.find_one({"_id": ObjectId(id)})
    if(response):
        Connection.Quartos.delete_one({"_id": ObjectId(id)})
        return {"message": "Quarto deletado"}
    else:
        return {"message": "Quarto não encontrado"}


########################## FUNCIONARIOS #########################

@app.get("/funcionario")
async def GET():
    response = Connection.Funcionarios.find()
    lista = (str(list(response)))
    return {"message": lista}


@app.post("/funcionario")
async def POST(funcionarios: FuncionariosModel):

    Connection.Funcionarios.insert_one(
        {"Name": funcionarios.Name, "Function": funcionarios.Function, "CostPerHour": funcionarios.CostPerHour})
    return {"message": "Adicionado com sucesso"}


@app.put("/funcionario")
async def UPDATE(id: str, costperhour: float, function: str):
    if (not id):
        return {"message": "Id não informado"}
    elif (not costperhour):
        return {"message": "Custo por hora não informado"}
    elif (not function):
        return {"message": "Função não informada"}

    Connection.Funcionarios.update_one({"_id": ObjectId(id)}, {
                                       "$set": {"CostPerHour": costperhour, "Function": function}})

    return {"message": "Funcionario deletado"}


@app.delete("/funcionario")
async def DELETE(id: str):

    if(not id):
        return {"message": "Id não informado"}

    response = Connection.Funcionarios.find_one({"_id": ObjectId(id)})
    if(response):
        Connection.Funcionarios.delete_one({"_id": ObjectId(id)})
        return {"message": "Funcionario deletado"}
    else:
        return {"message": "Funcionario não encontrado"}


#######################FLUXO DE HORAS#############################

@app.get("/fluxodehoras")
async def GET():
    response = Connection.Fluxodehoras.find()
    lista = (str(list(response)))
    return {"message": lista}


@app.post("/fluxodehoras")
async def POST(fluxo: Fluxosdehorasmodel):
    dateNow = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    data = {"RoomNumber": ObjectId(fluxo.RoomNumber),
            "Employees": fluxo.Employees,
            "EntryTime": fluxo.EntryTime,
            "ExitTime": fluxo.ExitTime,
            "Date": dateNow,
            "TotalCostForTheRoom": fluxo.TotalCostForTheRoom,
            }
    Connection.Fluxodehoras.insert_one(data)
    return {"message": "Adicionado com sucesso"}


@app.post("/fluxodehoras/incrementemployees")
async def POST(id: str, employee: str):
    if(not id):
        return {"message": "Id da tabela de fluxo de horas não informado"}
    elif(not employee):
        return {"message": "Id do funcionário não informado"}

    response = Connection.Fluxodehoras.find_one({"_id": ObjectId(id)})
    verifyUser = Connection.Funcionarios.find_one({"_id": ObjectId(employee)})
    
    if(not response):
        return {"message": "Fluxo de horas não encontrado"}
    elif(not verifyUser):
        return {"message": "Funcionario não encontrado"}
    for x in response["Employees"]:
        if(str(x) == str(employee)):
            return {"message": "Funcionario já cadastrado"}  

    Connection.Fluxodehoras.update_one(
        {"_id": ObjectId(id)}, {"$push": {"Employees": ObjectId(employee)}})

    return {"message": "Adicionado com sucesso"}

    # @app.put("/fluxodehoras")
    # async def UPDATE(id:str,costperhour:float,function:str):
    #     if (not id):
    #         return {"message": "Id não informado"}
    #     elif (not costperhour):
    #         return {"message": "Custo por hora não informado"}
    #     elif (not function):
    #         return {"message": "Função não informada"}

    #     Connection.Fluxodehoras.update_one({"_id": ObjectId(id)}, {"$set": {"CostPerHour":costperhour, "Function":function}})

    #     return {"message": "Funcionario deletado"}


@app.delete("/fluxodehoras")
async def DELETE(id: str):
    if(not id):
        return {"message": "Id não informado"}

    response = Connection.Fluxodehoras.find_one({"_id": ObjectId(id)})
    if(response):
        Connection.Fluxodehoras.delete_one({"_id": ObjectId(id)})
        return {"message": "Fluxo de horas deletado"}
    else:
        return {"message": "Fluxo de horas não encontrado"}
