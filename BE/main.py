from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from controllers import router
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import nest_asyncio

app = FastAPI()

# 세션 미들웨어 설정
SECRET_KEY = "your-secret-key-here"  # 안전한 비밀키로 변경해야 합니다
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {str(exc)}"}
    )

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영 환경에서는 구체적인 origin을 지정해야 합니다.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 설정
app.mount("/resources", StaticFiles(directory="resources"), name="resources")

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 라우터 포함
app.include_router(router)

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# 주피터 노트북 환경에서 실행할 경우
if __name__ == "__main__":
    import sys
    if "ipykernel" in sys.modules:  # 주피터 노트북에서 실행 중인지 확인
        nest_asyncio.apply()  # 중첩된 이벤트 루프 적용
        uvicorn.run(app, host="127.0.0.1", port=8000)
    else:
        uvicorn.run(app, host="127.0.0.1", port=8000)