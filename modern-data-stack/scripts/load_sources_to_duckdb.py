"""
Carga todos los CSV de la carpeta `sources` en una base DuckDB local.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import duckdb

SAFE_TABLE_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def main() -> int:
    root = Path(__file__).resolve().parent
    sources_dir = root / "sources"
    db_path = root / "local_warehouse.db"

    if not sources_dir.is_dir():
        print(f"No existe la carpeta de fuentes: {sources_dir}", file=sys.stderr)
        return 1

    csv_files = sorted(sources_dir.glob("*.csv"))
    if not csv_files:
        print(f"No hay archivos .csv en {sources_dir}", file=sys.stderr)
        return 1

    conn = duckdb.connect(str(db_path))

    for path in csv_files:
        table = path.stem
        if not SAFE_TABLE_NAME.match(table):
            print(f"Nombre de tabla no válido (omitiendo): {path.name}", file=sys.stderr)
            continue

        abs_path = path.resolve().as_posix()
        conn.execute(
            f'CREATE OR REPLACE TABLE "{table}" AS '
            "SELECT * FROM read_csv_auto(?, header=true, auto_detect=true)",
            [abs_path],
        )
        count = conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
        print(f"{table}: {count} filas")

    conn.close()
    print(f"Base actualizada: {db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
