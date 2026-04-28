import os
import json
import mysql.connector
from tqdm import tqdm  # shows a progress bar

# ── DB connection ──────────────────────────────────────────────
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2301",  # change this
    database="phonepe_pulse"
)
cursor = conn.cursor()

# ── Path to cloned repo ────────────────────────────────────────
DATA_PATH = r"C:\Users\User\pulse\data"  #  actual path

# ══════════════════════════════════════════════════════════════
# 1. AGGREGATED TRANSACTION
# ══════════════════════════════════════════════════════════════
def load_aggregated_transaction():
    path = os.path.join(DATA_PATH, "aggregated", "transaction", "country", "india", "state")
    for state in tqdm(os.listdir(path), desc="Agg Transaction"):
        for year in os.listdir(os.path.join(path, state)):
            for file in os.listdir(os.path.join(path, state, year)):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(path, state, year, file)) as f:
                    data = json.load(f)
                transactions = data["data"]["transactionData"]
                for t in transactions:
                    cursor.execute("""
                        INSERT INTO aggregated_transaction VALUES (%s,%s,%s,%s,%s,%s)
                    """, (state, int(year), quarter,
                          t["name"], t["paymentInstruments"][0]["count"],
                          t["paymentInstruments"][0]["amount"]))
    conn.commit()
    print("✅ aggregated_transaction loaded")

# ══════════════════════════════════════════════════════════════
# 2. AGGREGATED USER
# ══════════════════════════════════════════════════════════════
def load_aggregated_user():
    path = os.path.join(DATA_PATH, "aggregated", "user", "country", "india", "state")
    for state in tqdm(os.listdir(path), desc="Agg User"):
        for year in os.listdir(os.path.join(path, state)):
            for file in os.listdir(os.path.join(path, state, year)):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(path, state, year, file)) as f:
                    data = json.load(f)
                brands = data["data"].get("usersByDevice") or []
                for b in brands:
                    cursor.execute("""
                        INSERT INTO aggregated_user VALUES (%s,%s,%s,%s,%s,%s)
                    """, (state, int(year), quarter,
                          b["brand"], b["count"], b["percentage"]))
    conn.commit()
    print("✅ aggregated_user loaded")

# ══════════════════════════════════════════════════════════════
# 3. AGGREGATED INSURANCE
# ══════════════════════════════════════════════════════════════
def load_aggregated_insurance():
    path = os.path.join(DATA_PATH, "aggregated", "insurance", "country", "india", "state")
    for state in tqdm(os.listdir(path), desc="Agg Insurance"):
        for year in os.listdir(os.path.join(path, state)):
            for file in os.listdir(os.path.join(path, state, year)):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(path, state, year, file)) as f:
                    data = json.load(f)
                transactions = data["data"]["transactionData"]
                for t in transactions:
                    cursor.execute("""
                        INSERT INTO aggregated_insurance VALUES (%s,%s,%s,%s,%s,%s)
                    """, (state, int(year), quarter,
                          t["name"], t["paymentInstruments"][0]["count"],
                          t["paymentInstruments"][0]["amount"]))
    conn.commit()
    print("✅ aggregated_insurance loaded")

# ══════════════════════════════════════════════════════════════
# 4. MAP TRANSACTION
# ══════════════════════════════════════════════════════════════
def load_map_transaction():
    path = os.path.join(DATA_PATH, "map", "transaction", "hover", "country", "india", "state")
    for state in tqdm(os.listdir(path), desc="Map Transaction"):
        for year in os.listdir(os.path.join(path, state)):
            for file in os.listdir(os.path.join(path, state, year)):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(path, state, year, file)) as f:
                    data = json.load(f)
                for d in data["data"]["hoverDataList"]:
                    cursor.execute("""
                        INSERT INTO map_transaction VALUES (%s,%s,%s,%s,%s,%s)
                    """, (state, int(year), quarter,
                          d["name"], d["metric"][0]["count"], d["metric"][0]["amount"]))
    conn.commit()
    print("✅ map_transaction loaded")

# ══════════════════════════════════════════════════════════════
# 5. MAP USER
# ══════════════════════════════════════════════════════════════
def load_map_user():
    path = os.path.join(DATA_PATH, "map", "user", "hover", "country", "india", "state")
    for state in tqdm(os.listdir(path), desc="Map User"):
        for year in os.listdir(os.path.join(path, state)):
            for file in os.listdir(os.path.join(path, state, year)):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(path, state, year, file)) as f:
                    data = json.load(f)
                for d in data["data"]["hoverData"].values():
                    cursor.execute("""
                        INSERT INTO map_user VALUES (%s,%s,%s,%s,%s,%s)
                    """, (state, int(year), quarter,
                          list(data["data"]["hoverData"].keys())[
                              list(data["data"]["hoverData"].values()).index(d)],
                          d["registeredUsers"], d.get("appOpens", 0)))
    conn.commit()
    print("✅ map_user loaded")

# ══════════════════════════════════════════════════════════════
# 6. MAP INSURANCE
# ══════════════════════════════════════════════════════════════
def load_map_insurance():
    path = os.path.join(DATA_PATH, "map", "insurance", "hover", "country", "india", "state")
    for state in tqdm(os.listdir(path), desc="Map Insurance"):
        for year in os.listdir(os.path.join(path, state)):
            for file in os.listdir(os.path.join(path, state, year)):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(path, state, year, file)) as f:
                    data = json.load(f)
                for d in data["data"]["hoverDataList"]:
                    cursor.execute("""
                        INSERT INTO map_insurance VALUES (%s,%s,%s,%s,%s,%s)
                    """, (state, int(year), quarter,
                          d["name"], d["metric"][0]["count"], d["metric"][0]["amount"]))
    conn.commit()
    print("✅ map_insurance loaded")

# ══════════════════════════════════════════════════════════════
# 7. TOP TRANSACTION
# ══════════════════════════════════════════════════════════════
def load_top_transaction():
    path = os.path.join(DATA_PATH, "top", "transaction", "country", "india", "state")
    for state in tqdm(os.listdir(path), desc="Top Transaction"):
        for year in os.listdir(os.path.join(path, state)):
            for file in os.listdir(os.path.join(path, state, year)):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(path, state, year, file)) as f:
                    data = json.load(f)
                for entity_type, items in data["data"].items():
                    if items:
                        for item in items:
                            cursor.execute("""
                                INSERT INTO top_transaction VALUES (%s,%s,%s,%s,%s,%s,%s)
                            """, (state, int(year), quarter,
                                  item["entityName"], entity_type,
                                  item["metric"]["count"], item["metric"]["amount"]))
    conn.commit()
    print("✅ top_transaction loaded")

# ══════════════════════════════════════════════════════════════
# 8. TOP USER
# ══════════════════════════════════════════════════════════════
def load_top_user():
    path = os.path.join(DATA_PATH, "top", "user", "country", "india", "state")
    for state in tqdm(os.listdir(path), desc="Top User"):
        for year in os.listdir(os.path.join(path, state)):
            for file in os.listdir(os.path.join(path, state, year)):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(path, state, year, file)) as f:
                    data = json.load(f)
                for entity_type, items in data["data"].items():
                    if items:
                        for item in items:
                            cursor.execute("""
                                INSERT INTO top_user VALUES (%s,%s,%s,%s,%s,%s)
                            """, (state, int(year), quarter,
                                  item["name"], entity_type,
                                  item["registeredUsers"]))
    conn.commit()
    print("✅ top_user loaded")

# ══════════════════════════════════════════════════════════════
# 9. TOP INSURANCE
# ══════════════════════════════════════════════════════════════
def load_top_insurance():
    path = os.path.join(DATA_PATH, "top", "insurance", "country", "india", "state")
    for state in tqdm(os.listdir(path), desc="Top Insurance"):
        for year in os.listdir(os.path.join(path, state)):
            for file in os.listdir(os.path.join(path, state, year)):
                quarter = int(file.replace(".json", ""))
                with open(os.path.join(path, state, year, file)) as f:
                    data = json.load(f)
                for entity_type, items in data["data"].items():
                    if items:
                        for item in items:
                            cursor.execute("""
                                INSERT INTO top_insurance VALUES (%s,%s,%s,%s,%s,%s,%s)
                            """, (state, int(year), quarter,
                                  item["entityName"], entity_type,
                                  item["metric"]["count"], item["metric"]["amount"]))
    conn.commit()
    print("✅ top_insurance loaded")

# ══════════════════════════════════════════════════════════════
# RUN ALL
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("Starting data load into MySQL...\n")
    load_aggregated_transaction()
    load_aggregated_user()
    load_aggregated_insurance()
    load_map_transaction()
    load_map_user()
    load_map_insurance()
    load_top_transaction()
    load_top_user()
    load_top_insurance()
    cursor.close()
    conn.close()
    print("\n🎉 All 9 tables loaded successfully!")