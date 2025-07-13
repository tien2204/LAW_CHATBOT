"""
Web search (SerpAPI) + simple filter 'site:thuvienphapluat.vn OR moj.gov.vn'
"""
from typing import List
from langchain.utilities import SerpAPIWrapper
from .config import get_settings

SET = get_settings()
_search = SerpAPIWrapper(serpapi_api_key=SET.serpapi_key,
                         k=5, gl="vn", hl="vi")

def search_web(query: str) -> List[str]:
    q = f"{query} site:thuvienphapluat.vn OR moj.gov.vn"
    results = _search.run(q)
    # `results` là str; giữ gọn 5 dòng đầu
    return results.split("\n")[:5]
