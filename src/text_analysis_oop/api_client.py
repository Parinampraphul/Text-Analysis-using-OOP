from collections import Counter
import re
from typing import Any

from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError


class TextAnalysisApiError(RuntimeError):
    pass


class HuggingFaceClient:
    def __init__(
        self,
        token: str,
        sentiment_model: str,
        ner_model: str,
        sarcasm_model: str,
        abuse_model: str,
    ) -> None:
        self.token = token
        self.client = InferenceClient(provider="hf-inference", api_key=token or None)
        self.sentiment_model = sentiment_model
        self.ner_model = ner_model
        self.sarcasm_model = sarcasm_model
        self.abuse_model = abuse_model

    def sentiment(self, text: str) -> dict[str, Any]:
        result = self._classify(text, self.sentiment_model)
        return {"model": self.sentiment_model, "sentiment": result}

    def named_entities(self, text: str) -> dict[str, Any]:
        self._ensure_token()
        try:
            result = self.client.token_classification(
                text,
                model=self.ner_model,
                aggregation_strategy="simple",
            )
        except (HfHubHTTPError, ValueError, TimeoutError) as exc:
            raise TextAnalysisApiError(f"Hugging Face NER request failed: {exc}") from exc

        return {"model": self.ner_model, "entities": _to_dicts(result)}

    def sarcasm(self, text: str) -> dict[str, Any]:
        result = self._classify(text, self.sarcasm_model)
        return {"model": self.sarcasm_model, "sarcasm": result}

    def abuse(self, text: str) -> dict[str, Any]:
        result = self._classify(text, self.abuse_model)
        return {"model": self.abuse_model, "abuse": result}

    def keywords(self, text: str) -> dict[str, Any]:
        words = re.findall(r"[A-Za-z][A-Za-z'-]{2,}", text.lower())
        counts = Counter(word for word in words if word not in STOP_WORDS)
        keywords = [{"keyword": word, "count": count} for word, count in counts.most_common(10)]
        return {"method": "local_frequency", "keywords": keywords}

    def _classify(self, text: str, model: str) -> list[dict[str, Any]]:
        self._ensure_token()
        try:
            result = self.client.text_classification(
                text,
                model=model,
                top_k=5,
            )
        except (HfHubHTTPError, ValueError, TimeoutError) as exc:
            raise TextAnalysisApiError(f"Hugging Face classification request failed: {exc}") from exc

        return _to_dicts(result)

    def _ensure_token(self) -> None:
        if not self.token:
            raise TextAnalysisApiError(
                "Missing HF_TOKEN. Add your Hugging Face token to the .env file."
            )


def _to_dicts(items: Any) -> list[dict[str, Any]]:
    output = []
    for item in items:
        if isinstance(item, dict):
            output.append(item)
        elif hasattr(item, "model_dump"):
            output.append(item.model_dump())
        elif hasattr(item, "__dict__"):
            output.append(vars(item))
        else:
            output.append({"value": str(item)})
    return output


STOP_WORDS = {
    "about",
    "after",
    "again",
    "also",
    "because",
    "been",
    "before",
    "being",
    "between",
    "could",
    "from",
    "have",
    "into",
    "more",
    "only",
    "other",
    "over",
    "should",
    "than",
    "that",
    "their",
    "there",
    "these",
    "they",
    "this",
    "through",
    "under",
    "were",
    "when",
    "where",
    "which",
    "while",
    "with",
    "would",
    "your",
}
