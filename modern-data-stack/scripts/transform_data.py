"""
Transformaciones sobre el almacén DuckDB local.
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb


def main() -> int:
    scripts_dir = Path(__file__).resolve().parent
    db_path = (scripts_dir / ".." / "duckdb" / "local_warehouse.db").resolve()

    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = duckdb.connect(str(db_path))

    conn.execute("""
        CREATE OR REPLACE TABLE reporte_ventas AS
        SELECT
            c.ID_Cliente,
            c.Nombre,
            c.Apellido,
            c."Región" AS region,
            COUNT(v.ID_Venta) AS total_ventas,
            COALESCE(SUM(v.Cantidad), 0)::BIGINT AS total_unidades
        FROM clientes c
        LEFT JOIN ventas v ON v.ID_Cliente = c.ID_Cliente
        GROUP BY
            c.ID_Cliente,
            c.Nombre,
            c.Apellido,
            c."Región"
    """)

    n = conn.execute("SELECT COUNT(*) FROM reporte_ventas").fetchone()[0]
    conn.close()

    print(f"Tabla reporte_ventas creada en {db_path} ({n} filas, una por cliente).")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except duckdb.CatalogException as e:
        print(
            "Faltan tablas en la base (¿ejecutaste la carga de CSV?). Detalle:",
            e,
            file=sys.stderr,
        )
        raise SystemExit(1) from e
