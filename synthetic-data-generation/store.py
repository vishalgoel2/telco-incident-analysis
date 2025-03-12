import sqlite3
from typing import List

DB_FILE = "telco_incidents.db"


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS INCIDENTS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scenario TEXT NOT NULL,
        dataset TEXT,
        generated BOOLEAN DEFAULT 0
    )
    """
    )
    conn.commit()
    return conn


def insert_scenarios(scenarios: List[str]):
    conn = get_db_connection()
    cursor = conn.cursor()
    for scenario in scenarios:
        cursor.execute(
            f"INSERT INTO INCIDENTS (scenario, generated) VALUES (?, ?)",
            (scenario, False),
        )
    conn.commit()
    conn.close()


def get_scenario_to_generate(order="ASC"):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM INCIDENTS WHERE generated = 0 ORDER BY ID {order} LIMIT 1"
    )
    row = cursor.fetchone()
    conn.close()
    if row:
        scenario = dict(row)
        return scenario
    return None


def update_scenario(scenario, datasets):
    conn = get_db_connection()
    cursor = conn.cursor()
    dataset_json = datasets.model_dump_json()
    cursor.execute(
        f"UPDATE INCIDENTS SET dataset = ?, generated = 1 WHERE id = ?",
        (dataset_json, scenario["id"]),
    )
    conn.commit()
    conn.close()


def get_all_scenario_datasets(limit: int = 200) -> List[str]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT dataset FROM INCIDENTS WHERE dataset IS NOT NULL LIMIT ?", (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    datasets = []
    for row in rows:
        if row["dataset"]:
            datasets.append(row["dataset"])
    return datasets
