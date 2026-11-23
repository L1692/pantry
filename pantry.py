"""pantry: la dispensa da riga di comando, su MariaDB.

Esempi:
    python pantry.py add "Riso Carnaroli" 1.5 kg secchi --scade 2027-03-01
    python pantry.py list
    python pantry.py scadenze --giorni 7
"""

import argparse
import sys
from datetime import date, timedelta

import pymysql

from db import connect

# Devono coincidere con gli ENUM di schema.sql. frozendict (Python 3.15): non modificabile.
CATEGORIES = frozendict(
    secchi="Secchi e cereali",
    scatolame="Scatolame",
    freschi="Freschi",
    surgelati="Surgelati",
    spezie="Spezie e condimenti",
)
UNITS = ("g", "kg", "ml", "l", "pz")


def add_item(name, quantity, unit, category, expires_on):
    sql = """
        INSERT INTO pantry_item (name, quantity, unit, category, expires_on)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (name, quantity, unit, category, expires_on))
            new_id = cur.fetchone()["id"]
        conn.commit()
    return new_id


def list_items():
    sql = """
        SELECT name, quantity, unit, category, expires_on
        FROM pantry_item
        ORDER BY expires_on IS NULL, expires_on, name
    """
    with connect() as conn, conn.cursor() as cur:
        cur.execute(sql)
        return cur.fetchall()


def expiring_items(days):
    sql = """
        SELECT name, quantity, unit, category, expires_on
        FROM pantry_item
        WHERE expires_on <= %s
        ORDER BY expires_on, name
    """
    with connect() as conn, conn.cursor() as cur:
        cur.execute(sql, (date.today() + timedelta(days=days),))
        return cur.fetchall()


def print_items(rows):
    today = date.today()
    for row in rows:
        exp = row["expires_on"]
        when = exp.strftime("%d/%m/%Y") if exp else "senza scadenza"
        flag = " SCADUTO" if exp and exp < today else ""
        qty = f"{row['quantity'].normalize():f}"
        category = CATEGORIES[row["category"]]
        print(f"{when:<15}{flag:<9} {row['name']} ({qty} {row['unit']}, {category})")


def main():
    parser = argparse.ArgumentParser(prog="pantry", description="La dispensa su MariaDB.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="aggiunge un prodotto")
    p_add.add_argument("name")
    p_add.add_argument("quantity", type=float)
    p_add.add_argument("unit", choices=UNITS)
    p_add.add_argument("category", choices=list(CATEGORIES))
    p_add.add_argument("--scade", type=date.fromisoformat, help="data AAAA-MM-GG")

    sub.add_parser("list", help="elenca la dispensa")

    p_exp = sub.add_parser("scadenze", help="prodotti scaduti o in scadenza")
    p_exp.add_argument("--giorni", type=int, default=7)

    args = parser.parse_args()
    try:
        run(parser, args)
    except pymysql.err.OperationalError as exc:
        sys.exit(f"Errore MariaDB: {exc.args[1]}")


def run(parser, args):
    if args.command == "add":
        if args.quantity < 0:
            parser.error("la quantità non può essere negativa")
        new_id = add_item(args.name, args.quantity, args.unit, args.category, args.scade)
        print(f"Aggiunto #{new_id}: {args.name}")
    elif args.command == "list":
        rows = list_items()
        if rows:
            print_items(rows)
        else:
            print("La dispensa è vuota.")
    elif args.command == "scadenze":
        rows = expiring_items(args.giorni)
        if rows:
            print_items(rows)
        else:
            print(f"Nessun prodotto in scadenza nei prossimi {args.giorni} giorni.")


if __name__ == "__main__":
    main()
