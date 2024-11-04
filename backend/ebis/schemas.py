from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, time, datetime
from typing import Optional

###############################
# user and token

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
# profile 

class ProfileBase(BaseModel):
    user:int
    role:str
    nama:str
    alamat:str
    no_telp:str

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileDelete(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int

    class Config:
        from_attributes = True

###############################
# produk
class ProdukBase(BaseModel):
    kategori:str
    nama:str
    deskripsi:str
    stok:str
    harga:int
    gambar:str
    
class ProdukCreate(ProdukBase):
    pass

class ProdukUpdate(ProdukBase):
    pass

class ProdukDelete(ProdukBase):
    pass

class Produk(ProdukBase):
    id: int

    class Config:
        from_attributes = True

###############################
# keranjang
class keranjangBase(BaseModel):
    user:int
    produk:int
    qty:int

class keranjangCreate(keranjangBase):
    pass

class keranjangUpdate(keranjangBase):
    pass

class keranjangDelete(keranjangBase):
    pass

class keranjang(keranjangBase):
    id: int

    class Config:
        from_attributes = True

###############################
# review
class reviewBase(BaseModel):
    pesanan:int
    produk:int
    rating:int
    review:str

class reviewCreate(reviewBase):
    pass

class reviewUpdate(reviewBase):
    pass

class reviewDelete(reviewBase):
    pass

class review(reviewBase):
    id: int

    class Config:
        from_attributes = True

###############################
# pesanan
class pesananBase(BaseModel):
    user:int
    produk:int
    qty:int
    metode_bayar:int
    tanggal:str
    waktu:str
    status_pesanan:str

class pesananCreate(pesananBase):
    pass

class pesananUpdate(pesananBase):
    pass

class pesananDelete(pesananBase):
    pass

class pesanan(pesananBase):
    id: int

    class Config:
        from_attributes = True

    @field_validator("tanggal")
    def parse_tanggal(cls, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value

    @field_validator("waktu")
    def parse_waktu(cls, value):
        if isinstance(value, str):
            return time.fromisoformat(value)
        return value

    @property
    def formatted_tanggal(self):
        return self.tanggal.strftime("%d %m %Y")
    
    @property
    def formatted_waktu(self):
        return self.waktu.strftime("%H:%M:%S")

###############################
# kategori
class kategoriBase(BaseModel):
    kategori:str

class kategoriCreate(kategoriBase):
    pass

class kategoriUpdate(kategoriBase):
    pass

class kategoriDelete(kategoriBase):
    pass

class kategori(kategoriBase):
    id: int

    class Config:
        from_attributes = True

###############################
# metode
class metodeBase(BaseModel):
    metode_bayar:str

class metodeCreate(metodeBase):
    pass

class metodeUpdate(metodeBase):
    pass

class metodeDelete(metodeBase):
    pass

class metode(metodeBase):
    id: int

    class Config:
        from_attributes = True