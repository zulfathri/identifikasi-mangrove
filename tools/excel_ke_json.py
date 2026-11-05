"""
Ubah matriks ciri (Excel) menjadi data web: data/mangrove.json

Pemakaian (dari folder kunci-mangrove):
    python tools/excel_ke_json.py
    python tools/excel_ke_json.py data-sumber/Matriks_Ciri_Mangrove_Sejati.xlsx data/mangrove.json

Yang dibaca:
  - lembar "Ciri"    : kode, organ, nama ciri, tipe, nilai yang boleh dipakai, keterangan
  - lembar "Spesies" : nama ilmiah, author, famili, nama lokal, halaman, status, catatan tata nama
  - lembar "Matriks" : baris 3 = kode ciri, baris 4 dst = satu spesies per baris
                       komentar sel = catatan "perlu verifikasi" yang tampil di web
Perlu: pip install openpyxl
"""
import json, sys, datetime
from pathlib import Path
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data-sumber" / "Matriks_Ciri_Mangrove_Sejati.xlsx"
out = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "data" / "mangrove.json"

wb = load_workbook(src)
txt = lambda v: "" if v is None else str(v).strip()

# Ciri
chars = []
for r in wb["Ciri"].iter_rows(min_row=2, values_only=True):
    if not r[0]: continue
    k, o, n, t, vals, ket = (txt(x) for x in r[:6])
    chars.append(dict(k=k, o=o, n=n, t=t, vals=[v.strip() for v in vals.split(";") if v.strip()], ket=ket))
vocab = {c["k"]: set(c["vals"]) for c in chars if c["vals"]}

# Spesies
meta = {}
for r in wb["Spesies"].iter_rows(min_row=2, values_only=True):
    if not r[1]: continue
    _, nama, auth, fam, lokal, hal, status, cat = r[:8]
    meta[txt(nama)] = dict(a=txt(auth), f=txt(fam), l=txt(lokal), p=hal,
                           st="" if txt(status) in ("", "Mangrove sejati") else txt(status), tn=txt(cat))

# Matriks
ws = wb["Matriks"]
codes = [txt(c.value) for c in ws[3]]
sp, flags, warn = [], {}, []
for row in ws.iter_rows(min_row=4):
    nama = txt(row[1].value)
    if not nama: continue
    if nama not in meta:
        warn.append(f"{nama}: ada di Matriks tetapi tidak ada di lembar Spesies"); continue
    v = {}
    for code, cell in zip(codes, row):
        if not code or code in ("kode",) or cell.column <= 2: continue
        val = txt(cell.value)
        if val:
            v[code] = val
            if code in vocab:
                for x in (s.strip() for s in val.split(";")):
                    if x not in vocab[code]:
                        warn.append(f"{nama} / {code}: nilai '{x}' tidak ada di daftar nilai lembar Ciri")
        if cell.comment:
            flags[f"{nama}|{code}"] = cell.comment.text.strip()
    sp.append(dict(n=nama, v=v, **meta[nama]))

data = dict(
    sumber="Noor, Khazali & Suryadiputra (2006) Panduan Pengenalan Mangrove di Indonesia; daftar dicocokkan dengan Giesen dkk. (FAO, 2007)",
    dibuat=datetime.date.today().isoformat(),
    chars=chars, sp=sp, flags=flags)
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Selesai: {len(sp)} jenis, {len(chars)} ciri, {len(flags)} catatan verifikasi -> {out}")
if warn:
    print("\nPERINGATAN:")
    for w in warn: print(" -", w)
