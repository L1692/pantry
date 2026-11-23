# pantry

La dispensa da riga di comando, in Python 3.15 su MariaDB. Unica libreria esterna: PyMySQL, il driver per collegarsi a MariaDB.

| File | Cosa contiene |
|---|---|
| `schema.sql` | La tabella `pantry_item` |
| `db.py` | La connessione a MariaDB (parametri da variabili d'ambiente) |
| `pantry.py` | Le query e i comandi `add`, `list`, `scadenze` |

## Preparazione (una volta)

```sql
-- mariadb -u root -p
CREATE DATABASE pantry CHARACTER SET utf8mb4;
CREATE USER 'pantry'@'localhost' IDENTIFIED BY 'pantry';
GRANT ALL ON pantry.* TO 'pantry'@'localhost';
```

```bash
mariadb -u pantry -p pantry < schema.sql
python3.15 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PANTRY_DB_PASSWORD=pantry   # opzionali: PANTRY_DB_HOST, PANTRY_DB_PORT, PANTRY_DB_USER, PANTRY_DB_NAME
```

## Uso

```bash
python pantry.py add "Riso Carnaroli" 1.5 kg secchi --scade 2027-03-01
python pantry.py add Yogurt 2 pz freschi --scade 2026-11-30
python pantry.py list
python pantry.py scadenze --giorni 7
```
