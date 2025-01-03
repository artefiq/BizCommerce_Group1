from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas, datetime
# from datetime import datetime
from database import SessionLocal, engine
from jose import jwt

models.BaseDB.metadata.create_all(bind=engine)

app = FastAPI(title="Web Service UTS E-Business",
    description="Web service UTS Kelompok 1 2024",
    version="0.0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "ilkom_upi_top"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Dokumentasi API: [url]:8000/docs"}

######################### USERS #########################

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Error: Username sudah digunakan")
    return crud.create_user(db=db, user=user)

@app.post("/login")
async def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if not authenticate(db, user):
        raise HTTPException(status_code=400, detail="Username atau password tidak cocok")
    
    user_login = crud.get_user_by_username(db, user.username)
    if user_login:
        access_token = create_access_token(user.username)
        return {"user_id": user_login.id, "access_token": access_token}
    else:
        raise HTTPException(status_code=400, detail="User tidak ditemukan, kontak admin")

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

######################### AUTH #########################

def authenticate(db, user: schemas.UserCreate):
    user_db = crud.get_user_by_username(db=db, username=user.username)
    return user_db and crud.verify_password(user.password, user_db.hashed_password)

def create_access_token(username):
    expiration_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    return jwt.encode({"username": username, "exp": expiration_time}, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["username"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired, harap login ulang")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token tidak valid")

@app.post("/token", response_model=schemas.Token)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_data = schemas.UserCreate(username=form_data.username, password=form_data.password)
    if not authenticate(db, user_data):
        raise HTTPException(status_code=400, detail="Username atau password tidak cocok")
    return {"access_token": create_access_token(form_data.username), "token_type": "bearer"}

######################### CRUD Operations #########################

# Profile Endpoints
@app.post("/profile/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db=db, profile=profile)

@app.get("/profile/{user_id}", response_model=schemas.Profile)
def read_profile(user_id: int, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, user_id=user_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile

@app.put("/profile/{profile_id}", response_model=schemas.Profile)
def update_profile(profile_id: int, profile: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    return crud.update_profile(db=db, profile_id=profile_id, profile=profile)

@app.delete("/profile/{profile_id}")
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    crud.delete_profile(db, profile_id=profile_id)
    return {"message": "Profile deleted"}

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

@app.get("/produk/", response_model=List[schemas.Produk])
def read_all_produk(db: Session = Depends(get_db)):
    return crud.get_all_produk(db)

@app.get("/produk/{kategori_id}", response_model=List[schemas.Produk])
def read_produk_kategori_id(kategori_id: int, db: Session = Depends(get_db)):
    db_produk_kategori_id = crud.get_produk_category_id(db, kategori_id=kategori_id)
    if db_produk_kategori_id is None:
        raise HTTPException(status_code=404, detail="Produk not found")
    return db_produk_kategori_id

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

@app.get("/keranjang_by_user/{user_id}", response_model=list[schemas.Keranjang])
def get_keranjang_by_user(user_id: int, db: Session = Depends(get_db)):
    db_keranjang = crud.get_keranjang_by_user(db, user_id=user_id)
    if db_keranjang is None:
        raise HTTPException(status_code=404, detail="Keranjang not found")
    return db_keranjang

@app.get("/keranjang/", response_model=List[schemas.Keranjang])
def read_all_keranjang(db: Session = Depends(get_db)):
    return crud.get_all_keranjang(db)

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

@app.get("/review/", response_model=List[schemas.Review])
def read_all_review(db: Session = Depends(get_db)):
    return crud.get_all_review(db)

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

@app.get("/pesanan/user_id/{user_id}", response_model=List[schemas.Pesanan])
def read_pesanan_user_id(user_id: int, db: Session = Depends(get_db)):
    return crud.get_pesanan_user_id(db, user_id=user_id)
    # if db_pesanan is None:
    #     raise HTTPException(status_code=404, detail="Pesanan not found")
    # return db_pesanan

@app.get("/pesanan/", response_model=List[schemas.Pesanan])
def read_all_pesanan(db: Session = Depends(get_db)):
    return crud.get_all_pesanan(db)

@app.get("/pesanan_detail/pesanan_id/{pesanan_id}", response_model=List[schemas.PesananDetail])
def read_pesanan_detail_pesanan_id(pesanan_id: int, db: Session = Depends(get_db)):
    db_pesanan_detail = crud.get_detail_pesanan_pesanan_id(db, pesanan_id=pesanan_id)
    if db_pesanan_detail is None:
        raise HTTPException(status_code=404, detail="No Item Found")
    return db_pesanan_detail

@app.put("/pesanan/{pesanan_id}", response_model=schemas.Pesanan)
def update_pesanan(pesanan_id: int, pesanan: schemas.PesananUpdate, db: Session = Depends(get_db)):
    return crud.update_pesanan(db=db, pesanan_id=pesanan_id, pesanan=pesanan)

@app.delete("/pesanan/{pesanan_id}")
def delete_pesanan(pesanan_id: int, db: Session = Depends(get_db)):
    crud.delete_pesanan(db, pesanan_id=pesanan_id)
    return {"message": "Pesanan deleted"}

@app.post("/pesanan/checkout/{user_id}", response_model=schemas.Pesanan)
def checkout(user_id: int, db: Session = Depends(get_db)):
    # Ambil semua item dalam keranjang berdasarkan user_id
    keranjang_items = crud.get_keranjang_by_user(db, user_id=user_id)
    if not keranjang_items:
        raise HTTPException(status_code=404, detail="Keranjang is empty")

    try:
        # 1. Buat pesanan utama
        pesanan_data = schemas.PesananCreate(
            user_id=user_id,
            metode_bayar_id=1,  # Sesuaikan metode pembayaran
            tanggal=datetime.now().date().isoformat(),
            waktu=datetime.now().time().isoformat(),
            status_pesanan="pending",  # Status awal
            total_harga=0,  # Akan dihitung ulang nanti
        )
        pesanan = crud.create_pesanan(db=db, pesanan=pesanan_data)
        pesanan_id = pesanan.id  # Ambil ID pesanan untuk detail pesanan

        # 2. Pindahkan data dari keranjang ke detail pesanan
        total_harga_final = 0
        for item in keranjang_items:
            # Validasi produk
            produk = crud.get_produk(db, produk_id=item.produk_id)
            if not produk:
                raise HTTPException(status_code=400, detail=f"Produk with ID {item.produk_id} not found")

            # Hitung total harga untuk item ini
            total_harga_item = produk.harga * item.qty
            total_harga_final += total_harga_item

            # Buat entri detail pesanan
            detail_pesanan_data = schemas.PesananDetailCreate(
                pesanan_id=pesanan_id,
                produk_id=item.produk_id,
                qty=item.qty,
                harga=total_harga_item
            )
            crud.create_detail_pesanan(db=db, detail_pesanan=detail_pesanan_data)

        # 3. Hapus keranjang untuk user
        crud.delete_keranjang_by_user(db, user_id=user_id)

        # 4. Update total harga pesanan utama
        crud.update_pesanan_total_harga(db=db, pesanan_id=pesanan_id, total_harga=total_harga_final)

        db.commit()  # Commit semua perubahan
        return pesanan
    except Exception as e:
        db.rollback()  # Rollback jika terjadi error
        raise HTTPException(status_code=500, detail=str(e))


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

@app.get("/kategori/", response_model=List[schemas.Kategori])
def read_all_kategori(db: Session = Depends(get_db)):
    return crud.get_all_kategori(db)

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

@app.get("/metode/", response_model=List[schemas.Metode])
def read_all_metode(db: Session = Depends(get_db)):
    return crud.get_all_metode(db)

@app.put("/metode/{metode_id}", response_model=schemas.Metode)
def update_metode(metode_id: int, metode: schemas.MetodeUpdate, db: Session = Depends(get_db)):
    return crud.update_metode(db=db, metode_id=metode_id, metode=metode)

@app.delete("/metode/{metode_id}")
def delete_metode(metode_id: int, db: Session = Depends(get_db)):
    crud.delete_metode(db, metode_id=metode_id)
    return {"message": "Metode deleted"}

@app.get("/pesanan/history/{user_id}", response_model=List[schemas.Pesanan])
def read_order_history(user_id: int, db: Session = Depends(get_db)):
    db_orders = crud.get_orders_by_user_and_status(db, user_id=user_id, status="Selesai")
    if not db_orders:
        raise HTTPException(status_code=404, detail="No completed orders found for this user")
    return db_orders
