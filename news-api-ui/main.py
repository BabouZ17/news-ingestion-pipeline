import streamlit as st

st.title = "News Ingestion Search"
st.caption("A news ingestion search dashboard")

searches = ["keyword_search", "hybrid_search", "knn_search"]

selected_options = st.multiselect("Select search type", searches)


with st.container():
    st.write("ads will be there")
