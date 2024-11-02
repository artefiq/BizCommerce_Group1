import numpy as np
import pandas as pd
from scipy.stats import mstats

# Membuat data tinggi badan contoh
data = {
    'Tinggi': [150, 160, 165, 170, 175, 180, 185, 190, 195, 200, 250]  # 250 adalah outlier
}

# Mengubah data menjadi DataFrame
df = pd.DataFrame(data)

# Menampilkan data asli
print("Data Asli:")
print(df)

# Melakukan winsorizing pada data dengan batas 5% dan 95%
df['Tinggi_Winsorized'] = mstats.winsorize(df['Tinggi'], limits=[0.05, 0.05])

# Menampilkan data setelah winsorizing
print("\nData Setelah Winsorizing:")
print(df)

