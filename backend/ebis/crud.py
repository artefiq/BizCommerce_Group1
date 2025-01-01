from sqlalchemy.orm import Session, joinedload
import models, schemas
from sqlalchemy import desc
import bcrypt
from passlib.context import CryptContext

# Constants
SALT = b'$2b$12$UoS.62CnRhwU6YGBLYx.6.'

#######################################################################################################
# User CRUD

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def delete_all_users(db: Session):
    deleted_count = db.query(models.User).delete()
    db.commit()
    return deleted_count

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), SALT)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

#######################################################################################################
# Profile CRUD

def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_profile(db: Session, user_id: int):
    return db.query(models.Profile).filter(models.Profile.user_id == user_id).first()

def update_profile(db: Session, profile_id: int, profile: schemas.ProfileUpdate):
    db_profile = db.query(models.Profile).filter(models.Profile.id == profile_id).first()
    if db_profile:
        for key, value in profile.dict(exclude_unset=True).items():
            setattr(db_profile, key, value)
        db.commit()
        db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: int):
    db.query(models.Profile).filter(models.Profile.id == profile_id).delete()
    db.commit()

#######################################################################################################
# Produk CRUD

def create_produk(db: Session, produk: schemas.ProdukCreate):
    db_produk = models.Produk(**produk.dict())
    db.add(db_produk)
    db.commit()
    db.refresh(db_produk)
    return db_produk

def get_produk(db: Session, produk_id: int):
    return db.query(models.Produk).filter(models.Produk.id == produk_id).first()

def get_produk_category_id(db: Session, kategori_id: int):
    return db.query(models.Produk).filter(models.Produk.kategori_id == kategori_id)

def get_all_produk(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Produk).offset(skip).limit(limit).all()

def update_produk(db: Session, produk_id: int, produk: schemas.ProdukUpdate):
    db_produk = db.query(models.Produk).filter(models.Produk.id == produk_id).first()
    if db_produk:
        for key, value in produk.dict(exclude_unset=True).items():
            setattr(db_produk, key, value)
        db.commit()
        db.refresh(db_produk)
    return db_produk

def delete_produk(db: Session, produk_id: int):
    db.query(models.Produk).filter(models.Produk.id == produk_id).delete()
    db.commit()

#######################################################################################################
# Keranjang CRUD

def create_keranjang(db: Session, keranjang: schemas.KeranjangCreate):
    db_keranjang = models.Keranjang(**keranjang.dict())
    db.add(db_keranjang)
    db.commit()
    db.refresh(db_keranjang)
    return db_keranjang

def get_keranjang(db: Session, keranjang_id: int):
    return db.query(models.Keranjang).filter(models.Keranjang.id == keranjang_id).first()

def get_all_keranjang(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Keranjang).offset(skip).limit(limit).all()

def update_keranjang(db: Session, keranjang_id: int, keranjang: schemas.KeranjangUpdate):
    db_keranjang = db.query(models.Keranjang).filter(models.Keranjang.id == keranjang_id).first()
    if db_keranjang:
        for key, value in keranjang.dict(exclude_unset=True).items():
            setattr(db_keranjang, key, value)
        db.commit()
        db.refresh(db_keranjang)
    return db_keranjang

def delete_keranjang(db: Session, keranjang_id: int):
    db.query(models.Keranjang).filter(models.Keranjang.id == keranjang_id).delete()
    db.commit()

#######################################################################################################
# Review CRUD

def create_review(db: Session, review: schemas.ReviewCreate):
    db_review = models.Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def get_all_review(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Review).offset(skip).limit(limit).all()

def update_review(db: Session, review_id: int, review: schemas.ReviewUpdate):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        for key, value in review.dict(exclude_unset=True).items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int):
    db.query(models.Review).filter(models.Review.id == review_id).delete()
    db.commit()

#######################################################################################################
# Pesanan CRUD

def create_pesanan(db: Session, pesanan: schemas.PesananCreate):
    db_pesanan = models.Pesanan(
        user_id=pesanan.user_id,
        metode_bayar_id=pesanan.metode_bayar_id,
        tanggal=pesanan.tanggal,
        waktu=pesanan.waktu,
        status_pesanan=pesanan.status_pesanan,
        detail_pesanan=pesanan.detail
    )
    db.add(db_pesanan)
    db.commit()
    db.refresh(db_pesanan)
    return db_pesanan

def get_pesanan(db: Session, pesanan_id: int):
    return db.query(models.Pesanan).filter(models.Pesanan.id == pesanan_id).options(joinedload(models.Pesanan.detail_pesanan)).first()

def get_all_pesanan(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pesanan).offset(skip).limit(limit).all()

def update_pesanan(db: Session, pesanan_id: int, pesanan: schemas.PesananUpdate):
    db_pesanan = db.query(models.Pesanan).filter(models.Pesanan.id == pesanan_id).first()
    if db_pesanan:
        for key, value in pesanan.dict(exclude_unset=True).items():
            setattr(db_pesanan, key, value)
        db.commit()
        db.refresh(db_pesanan)
    return db_pesanan

def delete_pesanan(db: Session, pesanan_id: int):
    db.query(models.Pesanan).filter(models.Pesanan.id == pesanan_id).delete()
    db.commit()

#######################################################################################################
# Kategori CRUD

def create_kategori(db: Session, kategori: schemas.KategoriCreate):
    db_kategori = models.Kategori(**kategori.dict())
    db.add(db_kategori)
    db.commit()
    db.refresh(db_kategori)
    return db_kategori

def get_kategori(db: Session, kategori_id: int):
    return db.query(models.Kategori).filter(models.Kategori.id == kategori_id).first()

def get_all_kategori(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Kategori).offset(skip).limit(limit).all()

def update_kategori(db: Session, kategori_id: int, kategori: schemas.KategoriUpdate):
    db_kategori = db.query(models.Kategori).filter(models.Kategori.id == kategori_id).first()
    if db_kategori:
        for key, value in kategori.dict(exclude_unset=True).items():
            setattr(db_kategori, key, value)
        db.commit()
        db.refresh(db_kategori)
    return db_kategori

def delete_kategori(db: Session, kategori_id: int):
    db.query(models.Kategori).filter(models.Kategori.id == kategori_id).delete()
    db.commit()

#######################################################################################################
# Metode CRUD

def create_metode(db: Session, metode: schemas.MetodeCreate):
    db_metode = models.Metode(**metode.dict())
    db.add(db_metode)
    db.commit()
    db.refresh(db_metode)
    return db_metode

def get_metode(db: Session, metode_id: int):
    return db.query(models.Metode).filter(models.Metode.id == metode_id).first()

def get_all_metode(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Metode).offset(skip).limit(limit).all()

def update_metode(db: Session, metode_id: int, metode: schemas.MetodeUpdate):
    db_metode = db.query(models.Metode).filter(models.Metode.id == metode_id).first()
    if db_metode:
        for key, value in metode.dict(exclude_unset=True).items():
            setattr(db_metode, key, value)
        db.commit()
        db.refresh(db_metode)
    return db_metode

def delete_metode(db: Session, metode_id: int):
    db.query(models.Metode).filter(models.Metode.id == metode_id).delete()
    db.commit()
