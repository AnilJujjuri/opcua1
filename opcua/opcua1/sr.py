import time
from opcua import ua, Server
from fastapi import FastAPI

sr = FastAPI()
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:8091/freeopcua/server/")

# setup our own namespace, not really necessary but should as spec
uri = "http://examples.freeopcua.github.io"
idx = server.register_namespace(uri)

# get Objects node, this is where we should put our nodes
objects = server.get_objects_node()

# populating our address space
myobj = objects.add_object(idx, "MyObject")
myvar = myobj.add_variable(idx, "MyVariable", 6.7)
myvar.set_writable() # Set MyVariable to be writable by clients

# starting server
server.start()
try:
    count = 0
    while True:
        time.sleep(0.1)
        count += 0.1
        myvar.set_value(count)
finally:
        #close connection, remove subscriptions, etc
        print("done")

@sr.get("/")
def read_root():
    return {"Hello": "World"}

@sr.get("/get_variable")
def read_variable():
    return {"value": myvar.get_value()}

@sr.put("/set_variable")
def write_variable(value: float):
    myvar.set_value(value)
    return {"success": True}

@sr.on_event("shutdown")
def shutdown_event():
    server.stop()







