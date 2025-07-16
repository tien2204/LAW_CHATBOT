import re, asyncio, json
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableBranch
from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOpenAI
from .config import get_settings
from .retriever import hybrid_retrieve
from .web_fallback import search_web

SET = get_settings()

# ---------- Prompt templates ----------
SYSTEM_MAIN = (
    "Bạn là trợ lý pháp luật Việt Nam chính xác và súc tích.\n"
    "Luôn trích dẫn điều/khoản, văn bản dưới dạng [§Điều xxx] hoặc [§Khoản 2 Điều xxx].\n"
    "Nếu không tìm thấy căn cứ, hãy trả lời “Xin lỗi, tôi chưa tìm thấy quy định phù hợp.”\n"
)
SYSTEM_WEB  = ("Không tìm thấy quy định trong kho dữ liệu nội bộ."
               "Hãy trả lời dựa trên thông tin web sau, kèm URL cuối mỗi trích dẫn.")

PROMPT_MAIN = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MAIN),
    ("system", "{context}"),
    ("user", "{question}"),
])

PROMPT_WEB = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_WEB),
    ("system", "{web_snippets}"),
    ("user", "{question}"),
])

llm = ChatGroq(api_key=SET.groq_api_key,
               model_name=SET.llm_model,
               temperature=SET.llm_temperature,
               streaming=True)

# ---------- Runnable helpers ----------
def _ctx(docs_scores):
    docs = [d.page_content for d, _ in docs_scores]
    return "\n\n".join(docs)

def _max_score(docs_scores):
    return docs_scores[0][1] if docs_scores else 0.0

def _need_fallback(docs_scores):
    return (_max_score(docs_scores) < SET.score_threshold) or (len(docs_scores)==0)

def _build_web(query):
    snippets = search_web(query)
    return "\n".join(f"• {s}" for s in snippets)

# ---------- Branching chain ----------
main_branch = (
    {"question": RunnablePassthrough(),
     "context": RunnableLambda(lambda q: hybrid_retrieve(q)) | RunnableLambda(_ctx)}
    | PROMPT_MAIN
    | llm
)

web_branch = (
    {"question": RunnablePassthrough(),
     "web_snippets": RunnableLambda(_build_web)}
    | PROMPT_WEB
    | llm
)

router_chain = RunnableBranch(
    (lambda q: _need_fallback(hybrid_retrieve(q)), web_branch),
    main_branch          # default
)

# ---------- Streaming wrapper ----------
async def stream_answer(question: str):
    answer = ""
    async for chunk in router_chain.astream(question):
        answer += chunk
        yield chunk
    # citations
    cites = re.findall(r"§[^ ]+|https?://\S+", answer)
    yield f"\n\n[CITATIONS] {', '.join(set(cites))}"
