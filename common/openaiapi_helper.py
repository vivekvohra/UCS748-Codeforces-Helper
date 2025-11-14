from dotenv import load_dotenv
import os

load_dotenv()

# Environment-configurable behavior:
# - If GEMINI_API_KEY is present, use the local gemini adapter below
# - Otherwise fall back to the existing OpenAI model wrappers (if available)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Default OpenAI-related env vars (kept for backward compatibility)
embedder_locator = os.environ.get("EMBEDDER_LOCATOR", "text-embedding-ada-002")
api_key = os.environ.get("OPENAI_API_TOKEN", "")
model_locator = os.environ.get("MODEL_LOCATOR", "gpt-3.5-turbo")
max_tokens = int(os.environ.get("MAX_TOKENS", 200))
temperature = float(os.environ.get("TEMPERATURE", 0.0))


if GEMINI_API_KEY:
    # Use Gemini via the project's gemini_client. Provide pathway UDFs so that
    # existing imports (openai_embedder/openai_chat_completion) continue to work
    # inside the Pathway pipeline (they were previously used inside .select).
    import pathway as pw
    import gemini_client

    @pw.udf
    def openai_embedder(data):
        # gemini_client.get_embedding returns a list[float]
        return gemini_client.get_embedding(data)

    @pw.udf
    def openai_chat_completion(prompt):
        return gemini_client.generate_answer(prompt)

else:
    # Fall back to OpenAI wrappers if available. Keep imports lazy to avoid hard
    # dependency when using Gemini only.
    try:
        from llm_app.model_wrappers import OpenAIEmbeddingModel, OpenAIChatGPTModel
    except Exception:
        OpenAIEmbeddingModel = None
        OpenAIChatGPTModel = None

    def openai_embedder(data):
        if OpenAIEmbeddingModel is None:
            raise RuntimeError(
                "OpenAI wrappers not available and GEMINI_API_KEY not set."
            )
        embedder = OpenAIEmbeddingModel(api_key=api_key)
        return embedder.apply(text=data, locator=embedder_locator)

    def openai_chat_completion(prompt):
        if OpenAIChatGPTModel is None:
            raise RuntimeError(
                "OpenAI wrappers not available and GEMINI_API_KEY not set."
            )
        model = OpenAIChatGPTModel(api_key=api_key)
        return model.apply(
            prompt,
            locator=model_locator,
            temperature=temperature,
            max_tokens=max_tokens,
        )
