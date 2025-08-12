import os
import streamlit as st
from enum import StrEnum
from news_api_ui.utils.load_data import load_data
from typing import Any, List

NEWS_API_URL = os.getenv("NEWS_API_URL")
assert NEWS_API_URL is not None, "Invalid 'NEWS_API_URL' received"


class SEARCH_TYPE(StrEnum):
    KEYWORD_SEARCH = "keywordSearch"
    HYBRID_SEARCH = "hybridSearch"
    SEMANTIC_SEARCH = "semanticSearch"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


st.title("News Ingestion Search")
st.caption("A news ingestion search dashboard")

if "query" not in st.session_state:
    st.session_state.query = None

if "news" not in st.session_state:
    st.session_state.news = None

selected_search = st.selectbox("Select search type", SEARCH_TYPE.list())

query_text: str = st.text_input(label="Type your query", key="query_text", max_chars=50)

if query_text:
    st.session_state.query = query_text
    st.session_state.news = load_data(
        url=NEWS_API_URL, path=selected_search, query=query_text
    )

if st.session_state.news is not None:
    for news in st.session_state.news:
        with st.container():
            st.title(news["title"])
            st.header(news["source"])
            st.write(news["body"])
            st.write(news["published_at"])
            st.markdown("---")
