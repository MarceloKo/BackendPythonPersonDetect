from datetime import datetime
from fastapi import FastAPI
from pymongo import MongoClient
from bson import ObjectId
from models.QuartoFluxo import Quartofluxomodel
from models.QuartoFluxoAcessosModel import Quartofluxoacessosmodel
from models.QuartoFluxoStatusModel import Quartofluxostatusmodel
from models.CargoModel import CargoModel

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
            {"bedroom": quarto.bedroom})
        return {"message": "Quarto cadastrado com sucesso"}


@app.put("/quarto")
async def UPDATE(id: str, bedroom: int):
    if(not id):
        return {"message": "Id não informado"}
    if(not bedroom):
        return {"message": "bedroom não informado"}

    response = Connection.Quartos.find_one({"_id": ObjectId(id)})
    if(response):
        Connection.Quartos.update_one({"_id": ObjectId(id)}, {
                                      "$set": {"bedroom": bedroom}})
        return {"message": "Quarto atualizado!"}
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


########################## CARGOS #########################

@app.get("/cargo")
async def GET():
    response = Connection.Cargo.find()
    lista = (str(list(response)))
    return {"message": lista}


@app.post("/cargo")
async def POST(cargos: CargoModel):

    Connection.Cargo.insert_one(
        {"Name": cargos.Name, "CostPerHour": cargos.CostPerHour})
    return {"message": "Adicionado com sucesso"}


@app.put("/cargo")
async def UPDATE(id: str, costperhour: float, name: str):
    if (not id):
        return {"message": "Id não informado"}
    elif (not costperhour):
        return {"message": "Custo por hora não informado"}
    elif (not name):
        return {"message": "Nome da função não informada"}

    Connection.Cargo.update_one({"_id": ObjectId(id)}, {
                                       "$set": {"CostPerHour": costperhour, "Name": name}})

    return {"message": "Cargo Atualizado"}


@app.delete("/cargo")
async def DELETE(id: str):

    if(not id):
        return {"message": "Id não informado"}

    response = Connection.Cargo.find_one({"_id": ObjectId(id)})
    if(response):
        Connection.Cargo.delete_one({"_id": ObjectId(id)})
        return {"message": "Cargo deletado"}
    else:
        return {"message": "Cargo não encontrado"}



#######################QUARTO FLUXO STATUS#############################
@app.get("/quartofluxostatus")
async def GET():
    response = Connection.QuartoFluxoStatus.find()
    lista = (str(list(response)))
    return {"message": lista}


@app.post("/quartofluxostatus")
async def POST(status: Quartofluxostatusmodel):

    Connection.QuartoFluxoStatus.insert_one(
        {"description": status.description})
    return {"message": "Adicionado com sucesso!"}


@app.put("/quartofluxostatus")
async def UPDATE(id: str, description: str):
    if (not id):
        return {"message": "Id não informado"}
    elif (not description):
        return {"message": "Nome do status não informado"}

    Connection.QuartoFluxoStatus.update_one({"_id": ObjectId(id)}, {
                                       "$set": {"description": description}})

    return {"message": "Atualizado com sucesso!"}


@app.delete("/quartofluxostatus")
async def DELETE(id: str):

    if(not id):
        return {"message": "Id não informado"}

    response = Connection.QuartoFluxoStatus.find_one({"_id": ObjectId(id)})
    print(response)
    if(response):
        Connection.QuartoFluxoStatus.delete_one({"_id": ObjectId(id)})
        return {"message": "Status deletado com sucesso!"}
    else:
        return {"message": "Status não encontrado"}


############################# QUARTO FLUXO #############################
@app.get("/quartofluxo")
async def GET():
    response = Connection.QuartoFluxo.find()
    lista = (str(list(response)))
    return {"message": lista}


@app.post("/quartofluxo")
async def POST(quartofluxo: Quartofluxomodel):
    dateNow = datetime.today().strftime('%d-%m-%Y')
    data = {"idQuarto": ObjectId(quartofluxo.idQuarto),
            "idQuartoFluxoStatus": ObjectId(quartofluxo.idQuartoFluxoStatus),
            "Date": dateNow,
            }
    response = Connection.QuartoFluxo.find_one({"Date": dateNow})
    if(response):
        return {"message": "Fluxo do dia já cadastrado"}
    
    Connection.QuartoFluxo.insert_one(data)
    return {"message": "Adicionado com sucesso"}


@app.put("/quartofluxo")
async def UPDATE(id:str,idQuartoFluxoStatus:str):
    if (not id):
        return {"message": "Id não informado"}
    elif (not idQuartoFluxoStatus):
        return {"message": "Id não informado"}

    Connection.QuartoFluxo.update_one({"_id": ObjectId(id)}, {"$set": {"idQuartoFluxoStatus":ObjectId(idQuartoFluxoStatus)}})
    return {"message": "Status do quarto alterado com sucesso"}


@app.delete("/quartofluxo")
async def DELETE(id: str):
    if(not id):
        return {"message": "Id não informado"}
    response = Connection.QuartoFluxo.find_one({"_id": ObjectId(id)})
    if(response):
        Connection.QuartoFluxo.delete_one({"_id": ObjectId(id)})
        return {"message": "Fluxo do quarto deletado com sucesso"}
    else:
        return {"message": "Fluxo do quarto não encontrado"}


############################# QUARTO FLUXO ACESSOS#############################

@app.get("/quartofluxoacessos")
async def GET():
    response = Connection.QuartoFluxoAcessos.find()
    lista = (str(list(response)))
    return {"message": lista}


@app.post("/quartofluxoacessos")
async def POST(quartofluxoacessos: Quartofluxoacessosmodel):
    dateNow = datetime.today().strftime('%H:%M:%S')
    data = {"idQuartoFluxo": ObjectId(quartofluxoacessos.idQuartoFluxo),
            "idCargo": ObjectId(quartofluxoacessos.idCargo),
            "idIARetangulo": quartofluxoacessos.idIARetangulo,
            "dateInitial": dateNow,
            "dateEnd": "",
            "timeAllocation": "00:00:00",
            }
    
    Connection.QuartoFluxoAcessos.insert_one(data)
    return {"message": "Adicionado com sucesso"}


@app.put("/quartofluxoacessos")
async def UPDATE(idIARetangulo:str):
    dateNow = datetime.today().strftime('%H:%M:%S')
    if (not idIARetangulo):
        return {"message": "Id não informado"}
    response = Connection.QuartoFluxoAcessos.find_one({"idIARetangulo": int(idIARetangulo)})
    if(response):
        dateInitial = datetime.strptime(response["dateInitial"],"%H:%M:%S")
        dateEnd = datetime.strptime(dateNow,"%H:%M:%S")
        timeAllocation = dateEnd - dateInitial
        Connection.QuartoFluxoAcessos.update_one({"idIARetangulo": int(idIARetangulo)}, {"$set": {"dateEnd": str(dateNow), "timeAllocation": str(timeAllocation)}})
        return {"message": "Fluxo acesso do quarto alterado com sucesso"}
    else:
        return {"message": "idIARetangulo não encontrado"}



@app.delete("/quartofluxoacessos")
async def DELETE(id: str):
    if(not id):
        return {"message": "Id não informado"}
    response = Connection.QuartoFluxoAcessos.find_one({"_id": ObjectId(id)})
    if(response):
        Connection.QuartoFluxoAcessos.delete_one({"_id": ObjectId(id)})
        return {"message": "Fluxo do quarto deletado com sucesso"}
    else:
        return {"message": "Fluxo do quarto não encontrado"}