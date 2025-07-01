import re, asyncio
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.chat_models import ChatGroq
from .config import get_settings
from .retriever import retrieve

SET = get_settings()

SYSTEM = (
    "Bạn là trợ lý pháp luật Việt Nam chính xác và súc tích.\n"
    "Luôn trích dẫn điều/khoản, văn bản dưới dạng [§Điều xxx] hoặc [§Khoản 2 Điều xxx].\n"
    "Nếu không tìm thấy căn cứ, hãy trả lời “Xin lỗi, tôi chưa tìm thấy quy định phù hợp.”\n"
)

prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM),
     ("user", "{question}"),
     ("context", "{context}")]
)

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

llm = ChatGroq(
    api_key=SET.groq_api_key,
    model_name=SET.llm_model,
    temperature=SET.llm_temperature,
    streaming=True,
)

chain = (
    {
        "question": RunnablePassthrough(),
        "context": RunnableLambda(lambda q: retrieve(q)) | RunnableLambda(format_docs),
    }
    | prompt
    | llm
)

async def stream_answer(question: str):
    full = ""
    async for chunk in chain.astream(question):
        full += chunk
        yield chunk
    # add citations list at the end (after streaming)
    cites = list(set(re.findall(r"§[^ ]+", full)))
    yield f"\n\n[CITATIONS] {', '.join(cites)}"
