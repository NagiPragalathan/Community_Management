import os
import uvicorn

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "QuizApp.settings")
    uvicorn.run("QuizApp.asgi:application", host="127.0.0.1", port=8000, log_level="info")
