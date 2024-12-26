from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import date, time

###############################
# User and Token

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

###############################
# Profile

class ProfileBase(BaseModel):
    user_id: int
    role: str
    nama: str
    alamat: str
    no_telp: str

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        from_attributes = True

###############################
# Produk

class ProdukBase(BaseModel):
    kategori_id: int
    nama: str
    deskripsi: str
    stok: int
    harga: int
    gambar: str

class ProdukCreate(ProdukBase):
    pass

class ProdukUpdate(ProdukBase):
    pass

class Produk(ProdukBase):
    id: int

    class Config:
        from_attributes = True

###############################
# Keranjang

class KeranjangBase(BaseModel):
    user_id: int
    produk_id: int
    qty: int

class KeranjangCreate(KeranjangBase):
    pass

class KeranjangUpdate(KeranjangBase):
    pass

class Keranjang(KeranjangBase):
    id: int

    class Config:
        from_attributes = True

###############################
# Review

class ReviewBase(BaseModel):
    pesanan_id: int
    produk_id: int
    rating: int
    review: str

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class Config:
        from_attributes = True

###############################
# Pesanan

class PesananBase(BaseModel):
    user_id: int
    metode_bayar_id: int
    tanggal: date
    waktu: time
    status_pesanan: str

class PesananCreate(PesananBase):
    detail: List[dict]

class PesananUpdate(PesananBase):
    status_pesanan: Optional[str]

class Pesanan(PesananBase):
    id: int
    detail_pesanan: List[dict]

    class Config:
        from_attributes = True

###############################
# Kategori

class KategoriBase(BaseModel):
    nama_kategori: str

class KategoriCreate(KategoriBase):
    pass

class KategoriUpdate(KategoriBase):
    pass

class Kategori(KategoriBase):
    id: int

    class Config:
        from_attributes = True

###############################
# Metode

class MetodeBase(BaseModel):
    nama_metode: str

class MetodeCreate(MetodeBase):
    pass

class MetodeUpdate(MetodeBase):
    pass

class Metode(MetodeBase):
    id: int

    class Config:
        from_attributes = True