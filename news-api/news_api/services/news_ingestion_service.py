import os
from datetime import datetime

from langchain_community.utils.math import cosine_similarity
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from news_api.models.news import News, NewsEmbedding

# Corpus of words to compare relevancy upon
CORPUS: list[str] = ["cybersecurity threats", "major outages", "software bugs"]

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY is not None, "Invalid OPENAI_API_KEY"


class NewsIngestionService:
    def __init__(
        self,
        model: str = "text-embedding-3-small",
        ingestion_threshold: float = 0.5,
    ):
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=10)
        self.embeddings_model = OpenAIEmbeddings(model=model)
        self.ingestion_threshold = ingestion_threshold
        self._embedded_corpus = dict()

    def _split_text(self, text: str) -> list[str]:
        return self.splitter.split_text(text)

    def embedded_corpus(self) -> dict[str, list[list[float]]]:
        """Compute the embeddings of the corpus

        Only done once to avoid extra cost.

        Returns:
            dict[str, list[list[float]]]
        """
        if len(self._embedded_corpus) == 0:
            for corpus_sentence in CORPUS:
                self._embedded_corpus[corpus_sentence] = self._create_embeddings(
                    self._split_text(corpus_sentence)
                )
        return self._embedded_corpus

    def _create_embeddings(self, sentences: list[str]) -> list[list[float]]:
        """Compute embeddings for a list of sentences

        Args:
            sentences (list[str]): Sentences to embed
        Returns:
            list[list[float]]
        """
        return self.embeddings_model.embed_documents(sentences)

    def should_ingest(self, news: News) -> tuple[bool, list[NewsEmbedding]]:
        """Check if a news content is relevant enough to be ingested

        To do so, we tokenize the news content. Then we compute the
        embeddings for each split. We compute the cosine similarity
        for each split. We compute the average of the split and if
        it's higher or equal to the given threshold, the content can
        be ingested.

        Args:
            news (News): News to ingest

        Returns:
            tuple[boolean, list[NewsEmbedding]]
        """
        # Split the raw content
        text_chunks: list[str] = self._split_text(
            text=news.body if news.body is not None else ""
        )

        # Compute embeddings for text chunks
        text_embeddings = self._create_embeddings(text_chunks)

        corpus_similarities_scores: list[float] = list()
        for corpus_embedding in self.embedded_corpus().values():
            corpus_similarities_scores.append(
                cosine_similarity(corpus_embedding, text_embeddings)[0][0]
            )

        # Map NewsEmbedding
        news_embeddings: list[NewsEmbedding] = list()
        for embedding, chunk in zip(text_embeddings, text_chunks):
            news_embeddings.append(NewsEmbedding(chunk=chunk, embedding=embedding))

        corpus_similarities_scores.sort()
        return (
            corpus_similarities_scores[-1] >= self.ingestion_threshold,
            news_embeddings,
        )


if __name__ == "__main__":

    exemples = [
        News(
            id="1",
            source="dev",
            title="Cybersecurity",
            body="Major cybersecurity threats have occured recently. Amazon has received no less than 5 millions daily attacks in 2025",
            published_at=datetime(year=2025, month=1, day=1),
        ),
        News(
            id="2",
            source="dev",
            title="Software updates",
            body="Software updates are a critical aspect of cybersecurity, with outdated software providing an easy entry point for hackers. To protect against software-related threats, it's essential to implement robust software update practices, including regular updates and patching. This can help prevent cyber attacks and protect sensitive data.",
            published_at=datetime(year=2025, month=1, day=1),
        ),
        News(
            id="3",
            source="dev",
            title="Useless",
            body="The sky is blue",
            published_at=datetime(year=2025, month=1, day=1),
        ),
    ]

    service = NewsIngestionService()
    for ex in exemples:
        result, _ = service.should_ingest(ex)
        print(result)
