from motor import motor_asyncio
from decouple import config
from bson import ObjectId
from models.UsuarioModel import UsuarioModel, UsuarioCriarModel
from utils.AuthUtils import gerar_senha_criptografada

MONGODB_URL = config("MONGODB_URL")

cliente = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

database = cliente.devagram

usuario_collection = database.get_collection("usuario")


def usuario_helper(usuario):
    return {
        "_id":str(usuario["_id"]),
        "nome": usuario["nome"],
        "email": usuario["email"],
        "senha": usuario["senha"],
        "foto": usuario["foto"]
    }


async def criar_usuario(usuario: UsuarioCriarModel) -> dict:
    usuario.senha = gerar_senha_criptografada(usuario.senha)

    usuario_criado = await usuario_collection.insert_one(usuario.__dict__)

    novo_usuario = await usuario_collection.find_one({"_id":usuario_criado.inserted_id})

    return usuario_helper(novo_usuario)

async def listar_usuarios():
    return usuario_collection.find

async def buscar_usuario_por_email(email:str) -> dict:
    usuario = await usuario_collection.find_one({"email":email})

    if usuario:
        return usuario_helper(usuario)

async def atualizar_usuario(id:str, dados_usuario: dict):
    usuario = await usuario_collection.find_one({"_id": ObjectId(id)})
    if usuario:
        usuario_atualizado = await usuario_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": dados_usuario}
        )

        return usuario_helper(usuario_atualizado)

async def deletar_usuario(id:str):
    usuario = await usuario_collection.find_one({"_id": ObjectId(id)})

    if usuario:
        await usuario_collection.delete_one({"_id": ObjectId(id)})