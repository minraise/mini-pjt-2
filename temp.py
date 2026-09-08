from app.repository import load_region_monthly

df = load_region_monthly("종로구", "2026-05", "2026-08")
print(df.shape)
print(df.head())