"""
Sube la tabla local reporte_ventas (DuckDB) a Supabase.

Variables en .env (raíz del proyecto):
  SUPABASE_URL=https://xxxx.supabase.co
  SUPABASE_KEY=tu_service_role_o_anon_key

Tabla en Supabase (ejemplo):

  create table public.reporte_ventas (
    id_cliente bigint primary key,
    nombre text,
    apellido text,
    region text,
    total_ventas bigint,
    total_unidades bigint
  );
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import duckdb
from dotenv import load_dotenv
from supabase import create_client

BATCH = 500


def main() -> int:
    scripts_dir = Path(__file__).resolve().parent
    project_root = scripts_dir.parent
    load_dotenv(project_root / ".env")

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("Error: define SUPABASE_URL y SUPABASE_KEY en .env", file=sys.stderr)
        return 1

    print("Conectando a Supabase (validando credenciales)...")
    client = create_client(url, key)

    db_path = project_root / "duckdb" / "local_warehouse.db"
    if not db_path.is_file():
        print(f"Error: no existe {db_path}", file=sys.stderr)
        return 1

    print(f"Leyendo DuckDB: {db_path}")
    conn = duckdb.connect(str(db_path))
    result = conn.execute("SELECT * FROM reporte_ventas")
    columns = [c[0] for c in result.description]
    rows = result.fetchall()
    conn.close()

    records = []
    for row in rows:
        d = dict(zip(columns, row))
        records.append(
            {
                "id_cliente": int(d["ID_Cliente"]),
                "nombre": d["Nombre"],
                "apellido": d["Apellido"],
                "region": d["region"],
                "total_ventas": int(d["total_ventas"]),
                "total_unidades": int(d["total_unidades"]),
            }
        )

    print(f"Leídas {len(records)} filas de reporte_ventas.")

    total_inserted = 0
    for i in range(0, len(records), BATCH):
        chunk = records[i : i + BATCH]
        resp = client.table("reporte_ventas").insert(chunk).execute()
        n = len(resp.data) if resp.data else 0
        total_inserted += n
        print(f"  Lote {i // BATCH + 1}: OK, {n} filas en la respuesta.")

    print(f"Listo: {len(records)} filas enviadas; Supabase devolvió {total_inserted} filas en total.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as e:
        print(f"Fallo: {e}", file=sys.stderr)
        raise SystemExit(1) from e
