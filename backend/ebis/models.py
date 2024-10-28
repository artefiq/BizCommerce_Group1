from database import BaseDB
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time, DateTime, Table
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(BaseDB):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique = True, index = True)
    hashed_password = Column(String)

# punya uts ebis
class Produk(BaseDB):
    __tablename__ = "produk"
    id = Column(Integer, primary_key=True)
    kategori = Column(Integer, ForeignKey('kategori.id'), nullable=False)
    nama = Column(String, unique=True, index=True)
    deskripsi = Column(String, nullable=False)
    stok = Column(Integer, nullable=False)
    harga = Column(Integer, nullable=False)

class Keranjang(BaseDB):
    __tablename__ = "keranjang"
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'), nullable=False)
    produk = Column(Integer, ForeignKey('produk.id'), nullable=False)
    qty = Column(Integer, nullable=False)

class Review(BaseDB):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True)
    pesanan = Column(Integer, ForeignKey('pesanan.id'), nullable=False)
    produk = Column(Integer, ForeignKey('produk.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(String, nullable=False)

class Pesanan(BaseDB):
    __tablename__ = "pesanan"
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'), nullable=False)
    Produk = Column(Integer, ForeignKey('produk.id'), nullable=False)
    metode_bayar = Column(Integer, ForeignKey('metode.id'), nullable=False)
    tanggal = Column(Date)
    waktu = Column(Time)
    status_pesanan = Column(String, nullable=False)

    @hybrid_property
    def formatted_tanggal(self):
        return self.tanggal.strftime("%d %m %Y")
    def formatted_waktu(self):
        return self.waktu.strftime("%H:%M:%S")

class Kategori(BaseDB):
    __tablename__ = "kategori"
    id = Column(Integer, primary_key=True)
    kategori = Column(String, nullable=False)

class Metode(BaseDB):
    __tablename__ = "metode"
    id = Column(Integer, primary_key=True)
    metode_bayar = Column(String, nullable=False)

########################################################################################################

# doctor = relationship('Doctor')
# facility = relationship('HealthFacility')