from database import BaseDB
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time, Table
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

# Model Definitions

class User(BaseDB):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    profile = relationship("Profile", back_populates="user_relation")
    keranjang = relationship("Keranjang", back_populates="user_relation")
    pesanan = relationship("Pesanan", back_populates="user_relation")


class Profile(BaseDB):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    role = Column(String, index=True, nullable=False)
    nama = Column(String, index=True, nullable=False)
    alamat = Column(String, nullable=False)
    no_telp = Column(String, index=True, nullable=False)

    user_relation = relationship("User", back_populates="profile")


class Produk(BaseDB):
    __tablename__ = "produk"
    id = Column(Integer, primary_key=True)
    kategori_id = Column(Integer, ForeignKey('kategori.id'), nullable=False)
    nama = Column(String, index=True, nullable=False)
    deskripsi = Column(String, nullable=False)
    stok = Column(Integer, nullable=False)
    harga = Column(Integer, nullable=False)
    gambar = Column(String, nullable=False)

    kategori_relation = relationship("Kategori", back_populates="produk")
    keranjang_items = relationship("Keranjang", back_populates="produk_relation")
    pesanan_items = relationship("PesananDetail", back_populates="produk_relation")


class Keranjang(BaseDB):
    __tablename__ = "keranjang"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    produk_id = Column(Integer, ForeignKey('produk.id'), nullable=False)
    qty = Column(Integer, nullable=False)

    user_relation = relationship("User", back_populates="keranjang")
    produk_relation = relationship("Produk", back_populates="keranjang_items")


class Pesanan(BaseDB):
    __tablename__ = "pesanan"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    metode_bayar_id = Column(Integer, ForeignKey('metode.id'), nullable=False)
    tanggal = Column(Date, nullable=False)
    waktu = Column(Time, nullable=False)
    status_pesanan = Column(String, nullable=False)

    user_relation = relationship("User", back_populates="pesanan")
    metode_bayar_relation = relationship("Metode", back_populates="pesanan")
    detail_pesanan = relationship("PesananDetail", back_populates="pesanan_relation")

    @hybrid_property
    def formatted_tanggal(self):
        return self.tanggal.strftime("%d-%m-%Y")

    @hybrid_property
    def formatted_waktu(self):
        return self.waktu.strftime("%H:%M:%S")


class PesananDetail(BaseDB):
    __tablename__ = "pesanan_detail"
    id = Column(Integer, primary_key=True)
    pesanan_id = Column(Integer, ForeignKey('pesanan.id'), nullable=False)
    produk_id = Column(Integer, ForeignKey('produk.id'), nullable=False)
    qty = Column(Integer, nullable=False)
    harga = Column(Integer, nullable=False)

    pesanan_relation = relationship("Pesanan", back_populates="detail_pesanan")
    produk_relation = relationship("Produk", back_populates="pesanan_items")


class Kategori(BaseDB):
    __tablename__ = "kategori"
    id = Column(Integer, primary_key=True)
    nama_kategori = Column(String, nullable=False, unique=True)

    produk = relationship("Produk", back_populates="kategori_relation")


class Metode(BaseDB):
    __tablename__ = "metode"
    id = Column(Integer, primary_key=True)
    nama_metode = Column(String, nullable=False, unique=True)

    pesanan = relationship("Pesanan", back_populates="metode_bayar_relation")
