from fastapi import APIRouter, Request, Depends, HTTPException, status, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from dependencies import get_current_user, get_current_user_optional, get_password_hash, verify_password
from schemas import UserCreate, UserLogin, PostCreate
from typing import List
from models import User, Post
from sqlalchemy import desc
from fastapi.responses import HTMLResponse, RedirectResponse
import logging
from PIL import Image
import torch
from torchvision import transforms
import albumentations as A
import torch.nn.functional as F
from albumentations.pytorch import ToTensorV2
import numpy as np
from tourlist import cave, flower, market, mountains, museum, night_view, sea, temple, theme_park
import os
from uuid import uuid4
from fastapi.security import APIKeyCookie
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime, timedelta
from jose import JWTError, jwt


router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger(__name__)

# 세션 미들웨어 설정
SECRET_KEY = "your-secret-key"  # 안전한 비밀키로 변경해야 합니다
cookie_sec = APIKeyCookie(name="session")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
categories = ["cave", "flower", "market", "mountains", "museum", "night_view", "sea", "temple", "theme_park"]

def preprocess_image(image_data, image_size=224):
    transform = A.Compose([
        A.Resize(image_size, image_size),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])
    image = transform(image=np.array(image_data))['image']
    image = image.unsqueeze(0)  # 배치 형태로 변환
    return image

# 모델 로드 및 예측 함수
def predict_image(model, image, class_names, device):
    model.eval()  # 평가 모드로 전환
    model = model.to(device)

    # 예측 수행
    with torch.no_grad():
        image = image.to(device)
        outputs = model(image)

        # Softmax로 각 클래스에 대한 확률 계산
        probabilities = F.softmax(outputs, dim=1)
        top_prob, preds = torch.max(probabilities, 1)

    # 예측된 클래스 이름 및 확률 반환
    predicted_class = class_names[preds[0].item()]
    probabilities = probabilities.cpu().numpy()[0]  # 각 클래스에 대한 확률을 가져옴

    return predicted_class, probabilities

# ---------------------------- 비밀번호 암호화 ----------------------------
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
# ---------------------------- 회원관리 ----------------------------
# 회원가입
from sqlalchemy.exc import IntegrityError

@router.post("/signup", response_model=schemas.User)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        # 사용자 이름 중복 확인
        existing_user_by_username = db.query(models.User).filter(models.User.username == user.username).first()
        if existing_user_by_username:
            raise HTTPException(status_code=400, detail="이미 존재하는 사용자 이름입니다.")

        # 이메일 중복 확인
        existing_user_by_email = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user_by_email:
            raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

        # 사용자 생성
        hashed_password = get_password_hash(user.password)
        new_user = models.User(
            username=user.username,
            email=user.email,
            country=user.country,
            hashed_password=hashed_password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()  # 오류 발생 시 트랜잭션 롤백
        raise HTTPException(status_code=400, detail="데이터베이스 오류가 발생했습니다.")

@router.post("/login")
async def login(request: Request, form_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    request.session["user_id"] = user.id
    return {"message": "Logged in successfully"}

@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}

#------------------------------------------------------------------------------------
@router.post("/uploadimage", response_class=HTMLResponse)
async def upload_image(image: UploadFile = File(...)):
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_path = "model.pth"  # 모델 경로
        class_names = ['동굴', '정원', '시장', '산', '박물관', '야경', '바다', '궁/사찰', '테마파크']

        # 모델 로드
        model = torch.load(model_path, map_location=device)

        # 이미지 열기 및 전처리
        image_data = Image.open(image.file).convert("RGB")
        img_tensor = preprocess_image(image_data)

        # 예측 수행
        _, probabilities = predict_image(model, img_tensor, class_names, device)

        # 유사도 순위가 높은 3개 클래스 선택
        top_3_indices = np.argsort(probabilities)[-3:][::-1]  # 상위 3개의 인덱스를 내림차순으로 가져옴

        # 테마 이름과 확률을 각각 따로 리스트에 저장
        top_3_themes = [class_names[i] for i in top_3_indices]
        top_3_probs = [f"{probabilities[i] * 100:.2f}%" for i in top_3_indices]  # 확률을 퍼센트로 소수점 2자리까지만 저장

        tourtitle = []
        touraddr = []
        tourimg = []
        tourex = []
        for theme in top_3_themes:
            if theme == '동굴':
                df=cave()
                df=df.sample(3)
                a = df['title'].tolist()
                b = df['addr1'].tolist()
                c = df['firstimage'].tolist()
                d="자연이 만들어 낸 예술작품, 동굴을 찾으시는 군요! 한국의 동굴은 지역별로 석회암 동굴과 화산동굴인 용암 동굴로 나뉘어요. 동굴을 탐험하며 구석구석에서 다양한 지형을 만나보세요. 독특한 분위기의 인생샷을 남기기에도 좋아요!"
                tourtitle.append(a)
                touraddr.append(b)
                tourimg.append(c)
                tourex.append(d)

            elif theme == '정원':
                df=flower()
                df=df.sample(3)
                a = df['title'].tolist()
                b = df['addr1'].tolist()
                c = df['firstimage'].tolist()
                d="한국은 봄, 여름, 가을, 겨울 사계절을 가지고 있어, 계절 별로 피는 꽃이 달라요. 전국에서 계절마다 피는 꽃으로 축제를 열어요. 개화 시기를 확인하고 꽃 명소를 방문하세요. 향기까지 카메라에 담길거에요."
                tourtitle.append(a)
                touraddr.append(b)
                tourimg.append(c)
                tourex.append(d)

            elif theme == '시장':
                df=market()
                df=df.sample(3)
                a = df['title'].tolist()
                b = df['addr1'].tolist()
                c = df['firstimage'].tolist()
                d="한국의 시장을 방문해보실래요? 길게는 수백 년에서 짧게는 수십 년까지, 저마다의 역사와 특징을 지닌 채 여전히 열려있는 전통시장은 항상 사람이 붐벼요. 저렴한 가격으로, 현지인처럼 쇼핑을 즐기세요."
                tourtitle.append(a)
                touraddr.append(b)
                tourimg.append(c)
                tourex.append(d)

            elif theme == '산':
                df=mountains()
                df=df.sample(3)
                a = df['title'].tolist()
                b = df['addr1'].tolist()
                c = df['firstimage'].tolist()
                d="한국은 산의 나라라고 해도 과언이 아니죠. 국토의 70% 이상이 산으로 이루어져 있어요. 한국의 산은 대체로 낮고 완만하여 사람을 반기는 덕분에 친화적인 산악문화도 발달했어요. 어느 산을 가도 사계절마다 다른 풍경을 감상할 수 있어요!"
                tourtitle.append(a)
                touraddr.append(b)
                tourimg.append(c)
                tourex.append(d)

            elif theme == '박물관':
                df=museum()
                df=df.sample(3)
                a = df['title'].tolist()
                b = df['addr1'].tolist()
                c = df['firstimage'].tolist()
                d="어떤 나라를 여행한다는 것은 그 나라의 예술과 역사의 발자취를 따라가는 것이에요. 과거와 현재, 미래가 함께 숨 쉬는 박물관을 추천해드려요. 외국어 해설이 준비된 박물관도 있으니 꼭 확인하고 방문하세요."
                tourtitle.append(a)
                touraddr.append(b)
                tourimg.append(c)
                tourex.append(d)

            elif theme == '야경':
                df=night_view()
                df=df.sample(3)
                a = df['title'].tolist()
                b = df['addr1'].tolist()
                c = df['firstimage'].tolist()
                d="도시의 풍경은 밤이 되면 화려한 야경이 돼요. 환상적인 뷰, 소박한 도시의 뷰 어떤 것을 경험하든 이번 여행의 추억의 한 페이지가 될거에요."
                tourtitle.append(a)
                touraddr.append(b)
                tourimg.append(c)
                tourex.append(d)

            elif theme == '바다':
                df=sea()
                df=df.sample(3)
                a = df['title'].tolist()
                b = df['addr1'].tolist()
                c = df['firstimage'].tolist()
                d="바다를 방문하고 싶으세요?삼면이 바다인 한국은 바다와 항상 닿아있어요.깊고 맑은 물의 동해와 갯벌이 특징인 서해, 섬이 많은 남해까지 우리의 바다는 각기 다른 매력을 품고있어요."
                tourtitle.append(a)
                touraddr.append(b)
                tourimg.append(c)
                tourex.append(d)

            elif theme == '궁/사찰':
                df=temple()
                df=df.sample(3)
                a = df['title'].tolist()
                b = df['addr1'].tolist()
                c = df['firstimage'].tolist()
                d="오래된 건축물에는 역사와 문화의 흔적이 그대로 담겨있어요. 자연 지형과 조화를 이뤄 아름다움을 자랑하는 궁과 한옥을 방문해보세요. 역사 깊은 한국의 불교 문화가 궁금하다면 절에 찾아가보세요. 다양한 탑과 석상을 구경하며 경이로움을 느끼는 동시에, 겸손하고 차분한 분위기에서 철학적인 가르침을 받을 수 있어요."
                tourtitle.append(a)
                touraddr.append(b)
                tourimg.append(c)
                tourex.append(d)

            elif theme == '테마파크':
                df=theme_park()
                df=df.sample(3)
                a = df['title'].tolist()
                b = df['addr1'].tolist()
                c = df['firstimage'].tolist()
                d="익사이팅한 경험이 하고 싶은신가요?가상의 세계에 몰입하고 싶으신가요? 한국의 테마파크를 방문해보세요. 짜릿한 어트랙션, 화려한 퍼레이드가 당신을 기다리고 있어요."
                tourtitle.append(a)
                touraddr.append(b)
                tourimg.append(c)
                tourex.append(d)
            
        # 결과 페이지 렌더링
        return templates.TemplateResponse("recommend_result.html", {
            "request": {},
            "top_3_themes": top_3_themes,
            "top_3_probs": top_3_probs,
            "tourtitle" : tourtitle,
            "touraddr" : touraddr,
            "tourimg" : tourimg,
            'tourex':tourex
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred: {str(e)}")



# 로그인 관련 ------------------------------------------------------------------------

# 로그아웃 라우터로 필요없어서 삭제
@router.get("/login")
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/mypage")
async def get_mypage(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    
    posts = db.query(models.Post).filter(models.Post.user_id == user_id).order_by(models.Post.created_at.desc()).all()
    
    return templates.TemplateResponse("mypage.html", {
        "request": request,
        "username": user.username,
        "posts": posts
    })

@router.get("/signup")
async def get_login_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.get("/signup_complete")
async def get_login_page(request: Request):
    return templates.TemplateResponse("signup_complete.html", {"request": request})

@router.get("/recommend")
async def get_login_page(request: Request):
    return templates.TemplateResponse("recommend.html", {"request": request})

@router.get("/uploadimage")
async def get_login_page(request: Request):
    return templates.TemplateResponse("uploadimage.html", {"request": request})

@router.get("/recommend_result")
async def get_login_page(request: Request):
    return templates.TemplateResponse("recommend_result.html", {"request": request})

# 탈퇴
@router.post("/delete-account")
async def delete_account(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}


# ---------------------------- 게시판 ----------------------------
# 게시판 메인 화면
from sqlalchemy.orm import joinedload

@router.get("/board")
async def board(request: Request, db: Session = Depends(get_db), page: int = 1):
    try:
        posts_per_page = 5
        offset = (page - 1) * posts_per_page
        page = max(1, page)
        
        # 전체 게시글 수 조회
        total_posts = db.query(models.Post).count()
        
        # 페이지네이션된 게시글 조회 (작성자 정보 포함)
        posts = db.query(models.Post, models.User.username.label("author_name"))\
            .join(models.User, models.Post.user_id == models.User.id)\
            .order_by(desc(models.Post.created_at))\
            .offset(offset).limit(posts_per_page).all()
        
        # 결과를 딕셔너리 리스트로 변환
        posts = [
            {
                "id": post.Post.id,
                "title": post.Post.title,
                "content": post.Post.content,
                "created_at": post.Post.created_at,
                "author_name": post.author_name
            } for post in posts
        ]
        
        total_pages = (total_posts - 1) // posts_per_page + 1
        
        context = {
            "request": request,
            "posts": posts,
            "current_page": page,
            "total_pages": total_pages
        }
        
        return templates.TemplateResponse("board.html", context)
    except Exception as e:
        print(f"Error in board route: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    

#작성
@router.get("/write")
async def write_get(request: Request):
    return templates.TemplateResponse("boardcreate.html", {"request": request})

import traceback
from fastapi.responses import JSONResponse
from uuid import uuid4
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/write")
async def write_post(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        post_data = {
            "title": title,
            "content": content,
            "user_id": user_id
        }

        if image:
            # 이미지 저장 로직
            upload_dir = os.path.join("resources", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            
            file_name = f"{uuid4()}.{image.filename.split('.')[-1]}"
            file_path = os.path.join(upload_dir, file_name)
            
            with open(file_path, "wb") as buffer:
                buffer.write(await image.read())
            
            post_data["image_url"] = f"/resources/uploads/{file_name}"

        db_post = models.Post(**post_data)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        
        logger.info(f"Post created successfully: {db_post.id}")
        return JSONResponse(content={"message": "Post created successfully", "post_id": db_post.id})
    except Exception as e:
        db.rollback()
        error_msg = f"Error creating post: {str(e)}"
        logger.error(error_msg)
        return JSONResponse(status_code=500, content={"detail": str(e)})

@router.get("/posts", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts

# 글 조회
from fastapi.responses import HTMLResponse

@router.get("/post/{post_id}", response_class=HTMLResponse)
async def view_post(
    request: Request, 
    post_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user_optional)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    
    author = db.query(models.User).filter(models.User.id == post.user_id).first()
    
    can_edit = current_user and current_user.id == post.user_id
    
    return templates.TemplateResponse("post.html", {
        "request": request,
        "post": post,
        "author": author,
        "can_edit": can_edit
    })
    
@router.get("/boardupdate/{post_id}", response_class=HTMLResponse)
async def edit_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if post.user_id != user_id:
        raise HTTPException(status_code=403, detail="이 게시글을 수정할 권한이 없습니다.")
    
    return templates.TemplateResponse("boardupdate.html", {
        "request": request,
        "post": post
    })


@router.get("/api/post/{post_id}")
async def get_post_data(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return {
        "title": post.title,
        "content": post.content,
        "image_url": post.image_url
    }

@router.post("/boardupdate/{post_id}")
async def update_post(
    request: Request,
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),
    delete_image: bool = Form(False),
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")
    
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    if db_post.user_id != user_id:
        raise HTTPException(status_code=403, detail="이 게시글을 수정할 권한이 없습니다.")
    
    db_post.title = title
    db_post.content = content

    if delete_image:
        if db_post.image_url:
            # 기존 이미지 파일 삭제
            old_image_path = os.path.join("resources", db_post.image_url.lstrip("/"))
            if os.path.exists(old_image_path):
                os.remove(old_image_path)
        db_post.image_url = None
    elif image:
        # 새 이미지 업로드
        upload_dir = os.path.join("resources", "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        file_name = f"{uuid4()}.{image.filename.split('.')[-1]}"
        file_path = os.path.join(upload_dir, file_name)
        with open(file_path, "wb") as buffer:
            buffer.write(await image.read())
        db_post.image_url = f"/resources/uploads/{file_name}"
    
    db.commit()
    db.refresh(db_post)
    return {"message": "게시글이 성공적으로 수정되었습니다.", "post_id": db_post.id}

# 글 삭제
@router.post("/delete-post/{post_id}")
async def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post or post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    db.delete(post)
    db.commit()
    return {"success": True}


# 글 삭제 전 패스워드 확인
@router.post("/verify-password")
async def verify_password_for_post(
    request: Request,
    post_data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    post_id = post_data.get("post_id")
    password = post_data.get("password")

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post or post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="권한이 없습니다.")

    if verify_password(password, current_user.hashed_password):
        return {"success": True}
    else:
        return {"success": False}