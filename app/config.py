import os


class Settings:
    # Point this at a sovereign model endpoint (Swisscom/Apertus, Mistral on-prem,
    # a local Ollama, etc). If unset, the app runs with a mock model so you can
    # build the pipeline offline before wiring up real infrastructure.
    MODEL_ENDPOINT = os.getenv("MODEL_ENDPOINT", "")
    MODEL_NAME = os.getenv("MODEL_NAME", "apertus-70b")
    MODEL_API_KEY = os.getenv("MODEL_API_KEY", "")
    AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", "audit.jsonl")


settings = Settings()
