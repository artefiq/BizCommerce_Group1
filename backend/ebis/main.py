# package: fastapi, bcrypt, sqlalchemy, python-jose

# test lokal uvicorn main:app --host 0.0.0.0 --port 8000 --reload --

# kalau deploy di server: pip install gunicorn
# gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --daemon
# mematikan gunicorn (saat mau update):
# ps ax|grep gunicorn 
# pkill gunicorn

from os import path
from fastapi import Depends, Request, FastAPI, HTTPException

from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from pydantic import BaseModel

from sqlalchemy.orm import Session

import crud, models, schemas, shutil, datetime
from database import SessionLocal, engine
models.BaseDB.metadata.create_all(bind=engine)
from pathlib import Path

from jose import jwt

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile


app = FastAPI(title="Web service uts e business",
    description="Web service uts kelompok 1 2024",
    version="0.0.1",)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def root():
    return {"message": "Dokumentasi API: [url]:8000/docs"}

######################### USERS

# create user 
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Error: Username sudah digunakan")
    return crud.create_user(db=db, user=user)

# hasil adalah akses token    
@app.post("/login") #,response_model=schemas.Token
async def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not authenticate(db,user):
        raise HTTPException(status_code=400, detail="Username atau password tidak cocok")

    # ambil informasi username
    user_login = crud.get_user_by_username(db,user.username)
    if user_login:
        access_token = create_access_token(user.username)
        user_id = user_login.id
        return {"user_id":user_id,"access_token": access_token}
    else:
        raise HTTPException(status_code=400, detail="User tidak ditemukan, kontak admin")

#lihat detil user_id
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    usr =  verify_token(token) 
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

######################## AUTH

# periksa apakah username ada dan passwordnya cocok
# return boolean TRUE jika username dan password cocok
def authenticate(db,user: schemas.UserCreate):
    user_cari = crud.get_user_by_username(db=db, username=user.username)
    if user_cari:
        return (user_cari.hashed_password == crud.hashPassword(user.password))
    else:
        return False    
    
SECRET_KEY = "ilkom_upi_top"

def create_access_token(username):
    # membuat token dengan waktu expire
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    access_token = jwt.encode({"username": username, "exp": expiration_time}, SECRET_KEY, algorithm="HS256")
    return access_token

def verify_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=["HS256"])  # bukan algorithm,  algorithms (set)
        username = payload["username"]  

    # exception jika token invalid
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Unauthorize token, expired signature, harap login")
    except jwt.JWSError:
        raise HTTPException(status_code=401, detail="Unauthorize token, JWS Error")
    except jwt.JWTClaimsError:
        raise HTTPException(status_code=401, detail="Unauthorize token, JWT Claim Error")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Unauthorize token, JWT Error")   
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorize token, unknown error"+str(e))
    
    return {"user_name": username}

# internal untuk testing, jangan dipanggil langsung
# untuk swagger  .../doc supaya bisa auth dengan tombol gembok di kanan atas
# kalau penggunaan standard, gunakan /login

@app.post("/token", response_model=schemas.Token)
async def token(req: Request, form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):

    f = schemas.UserCreate
    f.username = form_data.username
    f.password = form_data.password
    if not authenticate(db,f):
        raise HTTPException(status_code=400, detail="username or password tidak cocok")

    #info = crud.get_user_by_username(form_data.username)
    # email = info["email"]   
    # role  = info["role"]   
    username  = form_data.username

    #buat access token\
    # def create_access_token(user_name,email,role,nama,status,kode_dosen,unit):
    access_token  = create_access_token(username)

    return {"access_token": access_token, "token_type": "bearer"}

####################################################################################################
# punya e bis

UPLOAD_DIRECTORY = "./../img"

# -------------------- PRODUK CRUD Endpoints --------------------

@app.post("/produk/", response_model=schemas.Produk)
def create_produk(produk: schemas.ProdukCreate, db: Session = Depends(get_db)):
    return crud.create_produk(db=db, produk=produk)

@app.get("/produk/{produk_id}", response_model=schemas.Produk)
def read_produk(produk_id: int, db: Session = Depends(get_db)):
    db_produk = crud.get_produk(db, produk_id=produk_id)
    if db_produk is None:
        raise HTTPException(status_code=404, detail="Produk not found")
    return db_produk

@app.put("/produk/{produk_id}", response_model=schemas.Produk)
def update_produk(produk_id: int, produk: schemas.ProdukUpdate, db: Session = Depends(get_db)):
    return crud.update_produk(db=db, produk_id=produk_id, produk=produk)

@app.delete("/produk/{produk_id}")
def delete_produk(produk_id: int, db: Session = Depends(get_db)):
    crud.delete_produk(db, produk_id=produk_id)
    return {"message": "Produk deleted"}

# -------------------- KERANJANG CRUD Endpoints --------------------

@app.post("/keranjang/", response_model=schemas.Keranjang)
def create_keranjang(keranjang: schemas.KeranjangCreate, db: Session = Depends(get_db)):
    return crud.create_keranjang(db=db, keranjang=keranjang)

@app.get("/keranjang/{keranjang_id}", response_model=schemas.Keranjang)
def read_keranjang(keranjang_id: int, db: Session = Depends(get_db)):
    db_keranjang = crud.get_keranjang(db, keranjang_id=keranjang_id)
    if db_keranjang is None:
        raise HTTPException(status_code=404, detail="Keranjang not found")
    return db_keranjang

@app.put("/keranjang/{keranjang_id}", response_model=schemas.Keranjang)
def update_keranjang(keranjang_id: int, keranjang: schemas.KeranjangUpdate, db: Session = Depends(get_db)):
    return crud.update_keranjang(db=db, keranjang_id=keranjang_id, keranjang=keranjang)

@app.delete("/keranjang/{keranjang_id}")
def delete_keranjang(keranjang_id: int, db: Session = Depends(get_db)):
    crud.delete_keranjang(db, keranjang_id=keranjang_id)
    return {"message": "Keranjang deleted"}

# -------------------- REVIEW CRUD Endpoints --------------------

@app.post("/review/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db=db, review=review)

@app.get("/review/{review_id}", response_model=schemas.Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    db_review = crud.get_review(db, review_id=review_id)
    if db_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@app.put("/review/{review_id}", response_model=schemas.Review)
def update_review(review_id: int, review: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    return crud.update_review(db=db, review_id=review_id, review=review)

@app.delete("/review/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    crud.delete_review(db, review_id=review_id)
    return {"message": "Review deleted"}

# -------------------- PESANAN CRUD Endpoints --------------------

@app.post("/pesanan/", response_model=schemas.Pesanan)
def create_pesanan(pesanan: schemas.PesananCreate, db: Session = Depends(get_db)):
    return crud.create_pesanan(db=db, pesanan=pesanan)

@app.get("/pesanan/{pesanan_id}", response_model=schemas.Pesanan)
def read_pesanan(pesanan_id: int, db: Session = Depends(get_db)):
    db_pesanan = crud.get_pesanan(db, pesanan_id=pesanan_id)
    if db_pesanan is None:
        raise HTTPException(status_code=404, detail="Pesanan not found")
    return db_pesanan

@app.put("/pesanan/{pesanan_id}", response_model=schemas.Pesanan)
def update_pesanan(pesanan_id: int, pesanan: schemas.PesananUpdate, db: Session = Depends(get_db)):
    return crud.update_pesanan(db=db, pesanan_id=pesanan_id, pesanan=pesanan)

@app.delete("/pesanan/{pesanan_id}")
def delete_pesanan(pesanan_id: int, db: Session = Depends(get_db)):
    crud.delete_pesanan(db, pesanan_id=pesanan_id)
    return {"message": "Pesanan deleted"}

# -------------------- KATEGORI CRUD Endpoints --------------------

@app.post("/kategori/", response_model=schemas.Kategori)
def create_kategori(kategori: schemas.KategoriCreate, db: Session = Depends(get_db)):
    return crud.create_kategori(db=db, kategori=kategori)

@app.get("/kategori/{kategori_id}", response_model=schemas.Kategori)
def read_kategori(kategori_id: int, db: Session = Depends(get_db)):
    db_kategori = crud.get_kategori(db, kategori_id=kategori_id)
    if db_kategori is None:
        raise HTTPException(status_code=404, detail="Kategori not found")
    return db_kategori

@app.put("/kategori/{kategori_id}", response_model=schemas.Kategori)
def update_kategori(kategori_id: int, kategori: schemas.KategoriUpdate, db: Session = Depends(get_db)):
    return crud.update_kategori(db=db, kategori_id=kategori_id, kategori=kategori)

@app.delete("/kategori/{kategori_id}")
def delete_kategori(kategori_id: int, db: Session = Depends(get_db)):
    crud.delete_kategori(db, kategori_id=kategori_id)
    return {"message": "Kategori deleted"}

# -------------------- METODE CRUD Endpoints --------------------

@app.post("/metode/", response_model=schemas.Metode)
def create_metode(metode: schemas.MetodeCreate, db: Session = Depends(get_db)):
    return crud.create_metode(db=db, metode=metode)

@app.get("/metode/{metode_id}", response_model=schemas.Metode)
def read_metode(metode_id: int, db: Session = Depends(get_db)):
    db_metode = crud.get_metode(db, metode_id=metode_id)
    if db_metode is None:
        raise HTTPException(status_code=404, detail="Metode not found")
    return db_metode

@app.put("/metode/{metode_id}", response_model=schemas.Metode)
def update_metode(metode_id: int, metode: schemas.MetodeUpdate, db: Session = Depends(get_db)):
    return crud.update_metode(db=db, metode_id=metode_id, metode=metode)

@app.delete("/metode/{metode_id}")
def delete_metode(metode_id: int, db: Session = Depends(get_db)):
    crud.delete_metode(db, metode_id=metode_id)
    return {"message": "Metode deleted"}

