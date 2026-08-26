from pathlib import Path
from datetime import datetime, timedelta
import random
import numpy as np
import pandas as pd

SEED = 42
OUTPUT_DIR = Path("data")
rng = np.random.default_rng(SEED)
random.seed(SEED)

CITIES = ["Jaipur","Mumbai","Delhi","Bengaluru","Ahmedabad","Pune","Hyderabad","Chennai","Kolkata","Udaipur"]
OCCUPATIONS = ["Engineer","Accountant","Doctor","Student","Business Owner","Consultant","Teacher","Designer","Trader","Analyst"]


def build():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    customers = []
    for i in range(1, 201):
        customers.append({
            "customer_id": f"C{i:04d}",
            "name": f"Customer_{i:04d}",
            "city": random.choice(CITIES),
            "occupation": random.choice(OCCUPATIONS),
            "account_open_date": (datetime(2023, 1, 1) + timedelta(days=int(rng.integers(0, 900)))).date().isoformat(),
        })
    customers_df = pd.DataFrame(customers)

    accounts_df = pd.DataFrame([
        {
            "account_id": f"A{i:05d}",
            "customer_id": f"C{i:04d}",
            "balance": round(float(rng.uniform(5000, 500000)), 2),
            "status": "ACTIVE",
        }
        for i in range(1, 201)
    ])

    devices = []
    for i in range(1, 201):
        cid = f"C{i:04d}"
        for j in (1, 2):
            devices.append({
                "customer_id": cid,
                "device_id": f"D{i:04d}_{j}",
                "ip_address": f"10.{(i % 250) + 1}.{j}.{(i * 7) % 250 + 1}",
                "device_type": random.choice(["Android", "iPhone", "Web"]),
                "login_city": customers_df.loc[i - 1, "city"],
                "first_seen": (datetime(2024, 1, 1) + timedelta(days=int(rng.integers(0, 500)))).isoformat(sep=" "),
            })
    devices_df = pd.DataFrame(devices)

    special = {
        "C0001": ("B0001_FRAUD", datetime(2026, 8, 10, 2, 0)),
        "C0002": ("B0002_SLOW", datetime(2026, 8, 10, 10, 0)),
        "C0003": ("B0003_BURST", datetime(2026, 8, 10, 23, 58)),
        "C0004": ("B0004_FP", datetime(2026, 8, 11, 14, 0)),
        "C0005": ("B0005_IDENT", datetime(2026, 8, 11, 1, 0)),
        "C0006": ("B0006_MIDNIGHT", datetime(2026, 8, 11, 23, 55)),
        "C0007": ("B0007_BOUNDARY", datetime(2026, 8, 12, 9, 0)),
        "C0008": ("B0008_BEFORE", datetime(2026, 8, 12, 11, 0)),
        "C0009": ("B0009_RAPID", datetime(2026, 8, 12, 2, 30)),
        "C0010": ("B0010_ONLY2", datetime(2026, 8, 12, 3, 0)),
    }

    beneficiaries = []
    for i in range(1, 201):
        cid = f"C{i:04d}"
        for j in (1, 2):
            added = datetime(2025, 1, 1) + timedelta(days=int(rng.integers(0, 500)), hours=int(rng.integers(0, 24)))
            beneficiaries.append({
                "customer_id": cid,
                "beneficiary_account": f"B{i:04d}_{j}",
                "added_on": added.isoformat(sep=" "),
                "verified": True,
                "bank_name": random.choice(["Bank_A", "Bank_B", "Bank_C", "Bank_D"]),
            })
    for cid, (bid, added) in special.items():
        beneficiaries.append({
            "customer_id": cid,
            "beneficiary_account": bid,
            "added_on": added.isoformat(sep=" "),
            "verified": False,
            "bank_name": "Bank_Z",
        })
    beneficiaries.append({
        "customer_id": "C0009",
        "beneficiary_account": "B0010_OTHER",
        "added_on": "2026-08-12 04:00:00",
        "verified": True,
        "bank_name": "Bank_B",
    })
    beneficiaries_df = pd.DataFrame(beneficiaries).drop_duplicates(["customer_id", "beneficiary_account"])

    transactions = []
    txn_id = 1

    def add_txn(customer_id, beneficiary, when, amount):
        nonlocal txn_id
        transactions.append({
            "txn_id": f"T{txn_id:07d}",
            "customer_id": customer_id,
            "from_account": f"A{int(customer_id[1:]):05d}",
            "to_account": beneficiary,
            "amount": float(amount),
            "txn_time": when.isoformat(sep=" "),
            "channel": "UPI",
            "status": "SUCCESS",
        })
        txn_id += 1

    for i in range(1, 201):
        cid = f"C{i:04d}"
        bids = list(beneficiaries_df.loc[beneficiaries_df.customer_id == cid, "beneficiary_account"])
        for _ in range(int(rng.integers(8, 16))):
            bid = random.choice(bids)
            day = datetime(2026, 7, 1) + timedelta(days=int(rng.integers(0, 45)))
            when = day.replace(hour=int(rng.integers(8, 21)), minute=int(rng.integers(60)), second=int(rng.integers(60)))
            amount = max(100, round(float(rng.lognormal(7, 0.55)), 2))
            add_txn(cid, bid, when, amount)

    cases = []

    cid, bid = "C0001", special["C0001"][0]
    a = special["C0001"][1]
    for off, amount in [(5, 95000), (7, 98000), (9, 97000), (12, 100000)]:
        add_txn(cid, bid, a + timedelta(minutes=off), amount)
    cases.append(("TC01", cid, bid, "ALERT", "3+ transactions with rapid gaps <=3 minutes"))

    cid, bid = "C0002", special["C0002"][0]
    a = special["C0002"][1]
    for off in (2, 21, 30):
        add_txn(cid, bid, a + timedelta(minutes=off), 5000)
    cases.append(("TC02", cid, bid, "NO_ALERT", "Gaps are 19 and 9 minutes"))

    cid, bid = "C0003", special["C0003"][0]
    a = special["C0003"][1]
    for off, amount in [(3, 12000), (5, 12500), (7, 13000), (25, 9000)]:
        add_txn(cid, bid, a + timedelta(minutes=off), amount)
    cases.append(("TC03", cid, bid, "ALERT", "3-transaction rapid burst followed by later non-rapid transaction"))

    cid, bid = "C0004", special["C0004"][0]
    a = special["C0004"][1]
    for off in (2, 4, 6, 8):
        add_txn(cid, bid, a + timedelta(minutes=off), 15000)
    cases.append(("TC04", cid, bid, "ALERT", "High-velocity pattern; may be legitimate business activity"))

    cid, bid = "C0005", special["C0005"][0]
    a = special["C0005"][1]
    for off in (3, 6, 9):
        add_txn(cid, bid, a + timedelta(minutes=off), 25000)
    cases.append(("TC05", cid, bid, "ALERT", "3 identical-value transactions with 3-minute gaps"))

    cid, bid = "C0006", special["C0006"][0]
    a = special["C0006"][1]
    for off, amount in [(2, 7000), (4, 7500), (6, 7200)]:
        add_txn(cid, bid, a + timedelta(minutes=off), amount)
    cases.append(("TC06", cid, bid, "ALERT", "3 rapid transactions crossing midnight"))

    cid, bid = "C0007", special["C0007"][0]
    a = special["C0007"][1]
    for off in (30, 32, 35):
        add_txn(cid, bid, a + timedelta(minutes=off), 50000)
    cases.append(("TC07", cid, bid, "NO_ALERT", "Only first transaction is exactly at 30-minute boundary"))

    cid, bid = "C0008", special["C0008"][0]
    a = special["C0008"][1]
    add_txn(cid, bid, a - timedelta(minutes=5), 20000)
    for off in (4, 19, 29):
        add_txn(cid, bid, a + timedelta(minutes=off), 20000)
    cases.append(("TC08", cid, bid, "NO_ALERT", "Pre-add transaction excluded; post-add gaps are not rapid"))

    cid, bid = "C0009", special["C0009"][0]
    a = special["C0009"][1]
    for off, amount in [(1, 8000), (3, 8200), (5, 8100)]:
        add_txn(cid, bid, a + timedelta(minutes=off), amount)
    cases.append(("TC09", cid, bid, "ALERT", "3 rapid transactions to B0009_RAPID"))

    bid2 = "B0010_OTHER"
    a2 = datetime(2026, 8, 12, 4, 0)
    for off, amount in [(5, 10000), (20, 11000)]:
        add_txn(cid, bid2, a2 + timedelta(minutes=off), amount)
    cases.append(("TC10", cid, bid2, "NO_ALERT", "Only 2 transactions; tests customer-beneficiary partitioning"))

    cid, bid = "C0010", special["C0010"][0]
    a = special["C0010"][1]
    for off, amount in [(1, 9000), (16, 9500), (25, 9200)]:
        add_txn(cid, bid, a + timedelta(minutes=off), amount)
    cases.append(("TC11", cid, bid, "NO_ALERT", "3 transactions but gaps are 15 and 9 minutes"))

    transactions_df = pd.DataFrame(transactions)

    login_events = []
    login_id = 1
    for i in range(1, 201):
        cid = f"C{i:04d}"
        for _ in range(5):
            when = datetime(2026, 7, 15) + timedelta(days=int(rng.integers(0, 30)), hours=int(rng.integers(0, 14)))
            login_events.append({
                "login_id": f"L{login_id:07d}",
                "customer_id": cid,
                "device_id": f"D{i:04d}_1",
                "ip_address": f"10.{(i % 250) + 1}.1.{(i * 7) % 250 + 1}",
                "login_time": when.isoformat(sep=" "),
                "login_city": customers_df.loc[i - 1, "city"],
            })
            login_id += 1
    login_events += [
        {"login_id": "L900001", "customer_id": "C0001", "device_id": "D0001_NEW", "ip_address": "172.16.99.10", "login_time": "2026-08-10 01:58:00", "login_city": "Mumbai"},
        {"login_id": "L900002", "customer_id": "C0003", "device_id": "D0003_NEW", "ip_address": "172.16.99.11", "login_time": "2026-08-10 23:56:00", "login_city": "Delhi"},
        {"login_id": "L900003", "customer_id": "C0005", "device_id": "D0005_NEW", "ip_address": "172.16.99.12", "login_time": "2026-08-11 00:58:00", "login_city": "Bengaluru"},
        {"login_id": "L900004", "customer_id": "C0009", "device_id": "D0009_NEW", "ip_address": "172.16.99.13", "login_time": "2026-08-12 02:29:00", "login_city": "Pune"},
    ]
    login_df = pd.DataFrame(login_events)

    for name, df in [("customers", customers_df), ("accounts", accounts_df), ("beneficiaries", beneficiaries_df), ("transactions", transactions_df), ("devices", devices_df), ("login_events", login_df)]:
        df.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)
    pd.DataFrame(cases, columns=["case_id", "customer_id", "beneficiary_account", "expected_outcome", "reason"]).to_csv("test_cases.csv", index=False)


if __name__ == "__main__":
    build()
    print("Synthetic fraud dataset generated in ./data and ./test_cases.csv")
