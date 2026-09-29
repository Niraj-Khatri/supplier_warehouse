import csv, random, datetime as dt
from pathlib import Path

random.seed(7)
OUT = Path("seeds"); OUT.mkdir(exist_ok=True)

REGIONS = ["North", "South", "Midwest", "West", None]
CATEGORIES = ["Produce", "Dairy", "Frozen", "Dry Goods", "Beverage"]
BASE = ["Harvest Foods", "Cedar Valley Farms", "Northgate Dairy",
        "Blue Ridge Beverage", "Summit Provisions", "Oakline Distributors",
        "Riverbend Organics", "Pinecrest Mills"]

# --- suppliers: duplicate names with different casing and whitespace ---
suppliers = []
for i, name in enumerate(BASE, start=1):
    suppliers.append({
        "supplier_id": f"SUP-{1000+i}",
        "supplier_name": name,
        "region": random.choice(REGIONS),
        "status": random.choice(["Active", "active", "ACTIVE", "Inactive"]),
        "created_at": (dt.date(2023, 1, 1) + dt.timedelta(days=random.randint(0, 900))).isoformat(),
    })
# three near-duplicates that should collapse in staging
suppliers.append({"supplier_id": "SUP-1009", "supplier_name": "  harvest foods ",
                  "region": "North", "status": "Active", "created_at": "2023-04-02"})
suppliers.append({"supplier_id": "SUP-1010", "supplier_name": "CEDAR VALLEY FARMS",
                  "region": None, "status": "active", "created_at": "2024-02-11"})
suppliers.append({"supplier_id": "SUP-1011", "supplier_name": "Northgate Dairy",
                  "region": "Midwest", "status": "Inactive", "created_at": "2023-09-30"})

# --- products: some orphaned supplier_ids, some null costs ---
products = []
for i in range(1, 61):
    sup = random.choice(suppliers)["supplier_id"]
    if i % 17 == 0:
        sup = f"SUP-{random.randint(9000, 9999)}"   # orphan on purpose
    products.append({
        "product_id": f"PRD-{2000+i}",
        "supplier_id": sup,
        "product_name": f"{random.choice(CATEGORIES)} Item {i:03d}",
        "category": random.choice(CATEGORIES),
        "unit_cost": "" if i % 13 == 0 else round(random.uniform(1.2, 48.0), 2),
    })

# --- orders: mixed date formats, negatives, duplicate ids ---
def messy_date(d):
    return random.choice([d.isoformat(), d.strftime("%m/%d/%Y"), d.strftime("%d-%b-%Y")])

orders, oid = [], 5000
for i in range(1, 801):
    oid += 1
    d = dt.date(2025, 1, 1) + dt.timedelta(days=random.randint(0, 600))
    qty = random.randint(1, 40)
    if i % 61 == 0:
        qty = -qty                                   # bad quantity on purpose
    orders.append({
        "order_id": f"ORD-{oid}",
        "product_id": random.choice(products)["product_id"],
        "order_date": messy_date(d),
        "quantity": qty,
        "unit_price": round(random.uniform(2.0, 80.0), 2),
        "order_status": random.choice(["Shipped", "shipped", "Cancelled", "Open", "OPEN"]),
    })
orders.extend(random.sample(orders, 6))              # duplicate order_ids on purpose

# --- returns ---
returns = []
for i, o in enumerate(random.sample(orders, 120), start=1):
    returns.append({
        "return_id": f"RET-{7000+i}",
        "order_id": o["order_id"],
        "return_date": messy_date(dt.date(2025, 6, 1) + dt.timedelta(days=random.randint(0, 400))),
        "return_qty": random.randint(1, max(1, abs(int(o["quantity"])))),
        "reason": random.choice(["Damaged", "Late", "Wrong item", "Quality", ""]),
    })

for name, rows in [("raw_suppliers", suppliers), ("raw_products", products),
                   ("raw_orders", orders), ("raw_returns", returns)]:
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"wrote {name}.csv  ({len(rows)} rows)")