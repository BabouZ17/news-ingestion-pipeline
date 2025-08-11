from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class NewsEmbeddingsService:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=10)
        self.embeddings_model = OpenAIEmbeddings(model=model)

    def split_text(self, text: str) -> list[str]:
        return self.splitter.split_text(text=text)

    def create_tokens_embeddings(self, text: str) -> list[list[float]]:
        text_chunks: list[str] = self.split_text(text)
        return self.create_embeddings(text_chunks)

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        return self.embeddings_model.embed_documents(texts=texts)


async def get_news_embeddings_service():
    yield NewsEmbeddingsService()
