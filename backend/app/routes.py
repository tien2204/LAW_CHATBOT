import re, json
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from .chains import router_chain, stream_answer

router = APIRouter(tags=["chat"])

@router.post("/chat")
async def chat(req: Request):
    q = (await req.json()).get("message", "")
    result = (await router_chain.ainvoke(q)).content  # 🔧 fix lỗi TypeError
    cites = list(set(re.findall(r"§[^ ]+|https?://\S+", result)))
    return JSONResponse({"answer": result, "citations": cites})



@router.get("/stream")
async def chat_stream(request: Request, q: str):
    async def event_gen():
        async for token in stream_answer(q):
            if await request.is_disconnected():
                break
            yield token
            
    return EventSourceResponse(event_gen())
