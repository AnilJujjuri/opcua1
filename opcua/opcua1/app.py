import asyncio
import sys
from typing import Optional
from fastapi import FastAPI
from opcua import Client

app = FastAPI()

# set up the client
client = Client("opc.tcp://localhost:8091/freeopcua/server/")
client.connect()

# @app.on_event("startup")
# async def startup_event():
#     print("App started!")
#     asyncio.create_task(read_loop())

# get the variable we want to read
myvar = client.get_node("ns=2;i=2")



# define a route to read the variable
@app.get("/read_var")
async def read_var():
    value = myvar.get_value()
    return {"value": value}

# define a route to write to the variable
@app.put("/write_var")
async def write_var(value: float):
    myvar.set_value(value)
    return {"value": value}

# define a route to check if the server is running
@app.get("/health")
async def health():
    return {"status": "ok"}

# define a background task to read the variable periodically

async def read_loop():
    while True:
        value = myvar.get_value()
        print("Value is:", value)
        await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(read_loop())

@app.on_event("shutdown")
async def shutdown_event():
    client.disconnect()







