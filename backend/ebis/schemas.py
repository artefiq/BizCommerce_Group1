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
# produk
class ProdukBase(BaseModel):
    pass
    
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
    pass

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
    pass

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
    pass

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

###############################
# kategori
class kategoriBase(BaseModel):
    pass

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
    pass

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

###############################
# doctor

class DoctorBase(BaseModel):
    nama: str
    pengalaman: int
    foto: str
    polyId: int

class Doctor(DoctorBase):
    id: int

    class Config:
        from_attributes = True

###############################
# appointment

class AppointmentBase(BaseModel):
    patientId: int
    doctorId: int
    facilityId: int
    status: str
    waktu: str
    metodePembayaran: str
    antrian: int
    relasiJudulPoliId: int

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int

    class Config:
        from_attributes = True

    # @field_validator("waktu")
    # def parse_waktu(cls, value):
    #     if isinstance(value, str):
    #         return int(value)
    #     return value

###############################
# Doctor Schedule

class DoctorScheduleBase(BaseModel):
    tanggal: date
    mulai: time
    selesai: time
    maxBooking: int
    currentBooking: int
    doctorId: int

class DoctorScheduleCreate(DoctorScheduleBase):
    pass

class DoctorScheduleUpdate(DoctorScheduleBase):
    pass

class DoctorSchedule(DoctorScheduleBase):
    id: int

    class Config:
        from_attributes = True

    @field_validator("tanggal")
    def parse_tanggal(cls, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value

    @field_validator("mulai")
    def parse_mulai(cls, value):
        if isinstance(value, str):
            return time.fromisoformat(value)
        return value

    @field_validator("selesai")
    def parse_selesai(cls, value):
        if isinstance(value, str):
            return time.fromisoformat(value)
        return value

    @property
    def formatted_tanggal(self):
        return self.tanggal.strftime("%d %m %Y")
    
    @property
    def formatted_mulai(self):
        return self.mulai.strftime("%H:%M:%S")
    
    @property
    def formatted_selesai(self):
        return self.selesai.strftime("%H:%M:%S")

###############################
# article

class HealthArticle(BaseModel):
    id: int
    title: str
    content: str
    coverImage: str
    topics: str
    recommendedDoctors: int
    references: str

    class Config:
        from_attributes = True

###############################
# health facillity

class HealthFacility(BaseModel):
    id: int
    namaFasilitas: str
    alamatFasilitas: str
    kecamatanFasilitas: str
    kotaKabFasilitas: str
    kodePosFasilitas: str
    tingkatFasilitas: str
    jumlahPoliklinik: str
    daftarPoliklinik: str
    fotoFaskes: str
    logoFaskes: str

    class Config:
        from_attributes = True

###############################
# medical record

class MedicalRecordBase(BaseModel):
    patientId: int
    date: Optional[date]
    appointmentId: int
    relasiJudulPoliId : int

class MedicalRecordCreate(MedicalRecordBase):
    pass

class MedicalRecordUpdate(MedicalRecordBase):
    pass

class MedicalRecord(MedicalRecordBase):
    id: int

    class Config:
        from_attributes = True

    @field_validator("date")
    def parse_dateTime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

###############################
# Referral

class ReferralBase(BaseModel):
    fromFacilityId: int
    toFacilityId: int
    patientId: int
    tanggal: date
    alasan: str

class ReferralCreate(ReferralBase):
    pass

class ReferralDelete(ReferralBase):
    pass

class Referral(ReferralBase):
    id: int
    class Config:
        from_attributes = True

###############################
# relasiDokterRsPoli

class RelasiDokterRsPoliBase(BaseModel):
    doctorId: int
    relasiRsPoliId: int

class RelasiDokterRsPoliCreate(RelasiDokterRsPoliBase):
    pass

class RelasiDokterRsPoliUpdate(RelasiDokterRsPoliBase):
    pass

class RelasiDokterRsPoli(RelasiDokterRsPoliBase):
    id: int

    class Config:
        from_attributes = True

###############################
# relasiJudulPoli

class RelasiJudulPoliBase(BaseModel):
    judul: str
    tindakan: str
    polyclinicId: int

class RelasiJudulPoliCreate(RelasiJudulPoliBase):
    pass

class RelasiJudulPoliUpdate(RelasiJudulPoliBase):
    pass

class RelasiJudulPoli(RelasiJudulPoliBase):
    id: int

    class Config:
        from_attributes = True

###############################
# relasiRsPoli

class RelasiRsPoliBase(BaseModel):
    rsId: int
    poliId: int

class RelasiRsPoliCreate(RelasiRsPoliBase):
    pass

class RelasiRsPoliUpdate(RelasiRsPoliBase):
    pass

class RelasiRsPoli(RelasiRsPoliBase):
    id: int

    class Config:
        from_attributes = True

###############################
# Review

class ReviewBase(BaseModel):
    reviewerId: int
    revieweeDoctorId: int
    revieweeFaskesId: int
    rating: int
    komentar: str
    tanggal: date

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int

    class Config:
        from_attributes = True

    @field_validator("tanggal")
    def parse_tanggal(cls, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value
    
    @property
    def formatted_tanggal(self):
        return self.tanggal.strftime("%d %m %Y")

###############################
# service

class Service(BaseModel):
    id: int
    icon: str
    name: str
    childText: str
    status: str

    class Config:
        from_attributes = True

###############################
# specialist and polyclinic

class SpecialistAndPolyclinic(BaseModel):
    id: int
    icon: str
    name: str

    class Config:
        from_attributes = True
