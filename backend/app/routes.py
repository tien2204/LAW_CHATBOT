import re, json
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse, EventSourceResponse
from .chains import chain, stream_answer

router = APIRouter(tags=["chat"])

@router.post("/chat")
async def chat(req: Request):
    q = (await req.json()).get("message", "")
    result = await chain.ainvoke(q)
    cites = list(set(re.findall(r"§[^ ]+", result)))
    return JSONResponse({"answer": result, "citations": cites})

@router.get("/stream")
async def chat_stream(request: Request, q: str):
    async def event_gen():
        async for token in stream_answer(q):
            if await request.is_disconnected():
                break
            yield f"data: {token}\n\n"
    return EventSourceResponse(event_gen())
