import fastapi
from fastapi_socketio import SocketManager
from pydantic import BaseModel
from urllib import parse
from socketio.exceptions import ConnectionRefusedError
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI(debug=True)
sm = SocketManager(app=app, cors_allowed_origins=[], mount_location="/gateaway")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Message(BaseModel):
    sender: str
    content: str

users: dict[str, str] = {"": "System"}
messages: list[Message] = [Message(sender="System", content="Welcome the chat")]

@app.get("/users")
def get_users():
    return users

@app.get("/messages")
def get_messages():
    return messages

@sm.on("connect")
async def on_connect(sid, environ):
    name = parse.parse_qs(environ["asgi.scope"]["query_string"].decode()).get("name")
    if name is None or len(name) == 0:
        raise ConnectionRefusedError("no name found in auth")
    name = name[0]
    if sid in users:
        raise ConnectionRefusedError("already authenticated")
    elif name in users.values():
        raise ConnectionRefusedError("name already exist")
    users[sid] = name
    msg = Message(sender="System", content=f"{name} Joined the chat")
    messages.append(msg)
    await sm.emit("messageAdd", msg.dict())

@sm.on("messageAdd")
async def on_message_add(sid, data):
    user = users[sid]
    msg = data["msg"]
    msg["sender"] = user
    messages.append(Message.validate(msg))
    await sm.emit("messageAdd", msg)

