#main
# pip install -r requirements.txt
# python main.py
# OR
# uvicorn main:app --host 127.0.0.1 --port 8000 --reload

### python -m pip install --upgrade pip setuptools wheel


from fastapi import FastAPI
import uvicorn
from api.routers import routers

app = FastAPI(title="My FastAPI App")

# Подключение роутеров
for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
