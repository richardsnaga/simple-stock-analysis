# app/seeds/seed_data.py

import os
import pandas as pd
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app import models  

SEED_FOLDER = os.path.dirname(__file__)

def seed_all():
    db: Session = SessionLocal()
    total_inserted = 0

    try:
        for filename in os.listdir(SEED_FOLDER):
            if not filename.endswith(".csv"):
                continue

            # Gunakan nama file untuk mencari nama model
            model_name = filename.replace(".csv", "").replace("_", " ").title().replace(" ", "")
            print(f"📘 Memproses file: {filename} → model: {model_name}")

            model_class = getattr(models, model_name, None)
            if not model_class:
                print(f"⚠️  Model '{model_name}' tidak ditemukan untuk file {filename}. Lewati.")
                continue

            filepath = os.path.join(SEED_FOLDER, filename)
            if os.stat(filepath).st_size == 0:
                print(f"⚠️  File {filename} kosong, lewati.")
                continue

            # === BACA CSV DENGAN PANDAS ===
            try:
                df = pd.read_csv(filepath, delimiter=';', encoding='utf-8')
            except Exception as e:
                print(f"❌ Gagal membaca {filename}: {e}")
                continue

            # Normalisasi nama kolom
            df.columns = [col.lower().strip().replace('.', '').replace(' ', '_') for col in df.columns]
            print(f"   🔍 Kolom ditemukan: {df.columns.tolist()}")

            if df.empty:
                print(f"⚠️  File {filename} tidak memiliki data.")
                continue

            # Tentukan kolom unik (ubah sesuai kebutuhan)
            unique_field = "date"
            if unique_field not in df.columns:
                print(f"⚠️  Kolom unik '{unique_field}' tidak ditemukan di {filename}. Lewati.")
                continue

            inserted = 0
            for row in df.to_dict(orient="records"):
                # Cek apakah data sudah ada
                existing = db.query(model_class).filter(
                    getattr(model_class, unique_field) == row[unique_field]
                ).first()

                if existing:
                    continue

                # Buat instance baru dari model ORM
                obj = model_class(**row)
                db.add(obj)
                inserted += 1

            db.commit()
            total_inserted += inserted
            print(f"✅ {inserted} record baru ditambahkan dari {filename}\n")

    except Exception as e:
        print(f"❌ Error saat seeding data: {e}")
        db.rollback()
    finally:
        db.close()
        print(f"🎯 Total record baru yang berhasil di-seed: {total_inserted}")


if __name__ == "__main__":
    seed_all()