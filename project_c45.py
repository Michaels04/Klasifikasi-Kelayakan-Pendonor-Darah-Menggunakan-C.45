import math
from collections import Counter

import numpy as np
import pandas as pd
from anytree import Node, RenderTree
from sklearn.model_selection import train_test_split
from tabulate import tabulate

# ==============================
# 1. Membaca dataset
# ==============================
df = pd.read_excel("Data Donor Darah.xlsx")

# ==============================
# 2. Preprocessing / Binning
# ==============================
# Binning umur
umur_bins = [0, 25, 45, np.inf]
umur_labels = ["Umur<=25", "25<Umur<=45", "45<Umur"]
df["Umur"] = pd.cut(df["Umur"], bins=umur_bins, labels=umur_labels, right=True)

# Binning HB berdasarkan jenis kelamin
hb_pria = [
    (df["Jenis Kelamin"] == "Pria") & df["HB"].between(13.0, 17.0),
    (df["Jenis Kelamin"] == "Pria") & ~df["HB"].between(13.0, 17.0),
]
hb_wanita = [
    (df["Jenis Kelamin"] == "Wanita") & df["HB"].between(12.0, 15.0),
    (df["Jenis Kelamin"] == "Wanita") & ~df["HB"].between(12.0, 15.0),
]
df["HB"] = np.select(
    hb_pria + hb_wanita,
    ["Normal", "Tidak Normal", "Normal", "Tidak Normal"],
    default="Tidak Diketahui",
)

# Binning tekanan darah
# Catatan: aturan mengikuti implementasi proyek asli.
def bins_tensi(s, d):
    if s < 120 or d < 80:
        return "Rendah"
    elif s > 139 or d > 89:
        return "Tinggi"
    return "Normal"

pos = df.columns.get_loc("Tensi S")
df.insert(pos, "Tensi", df.apply(lambda row: bins_tensi(row["Tensi S"], row["Tensi D"]), axis=1))
df.drop(columns=["Tensi S", "Tensi D"], inplace=True)

# Binning berat badan
berat_bins = [-np.inf, 60, 80, np.inf]
berat_labels = ["BB<=60", "60<BB<=80", "80<BB"]
df["Berat Badan"] = pd.cut(df["Berat Badan"], bins=berat_bins, labels=berat_labels, right=True)

# ==============================
# 3. Membagi data train dan test
# ==============================
x = df.drop(columns=["Status"])
y = df["Status"]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42, stratify=y
)

train_df = x_train.copy()
train_df["Label"] = y_train
test_df = x_test.copy()
test_df["Label"] = y_test

train_data = train_df.to_dict(orient="records")
test_data = test_df.to_dict(orient="records")

full_attr_values = {
    attr: sorted(df[attr].dropna().unique().tolist(), key=str)
    for attr in df.columns
    if attr != "Label"
}

# ==============================
# 4. Perhitungan C4.5
# ==============================
def entropy(data, target_attr):
    total = len(data)
    if total == 0:
        return 0

    counts = Counter(record[target_attr] for record in data)
    ent = 0
    for count in counts.values():
        p = count / total
        ent -= p * math.log2(p)
    return ent


def info_gain(data, attr, target_attr):
    total = len(data)
    subsets = {}
    for record in data:
        subsets.setdefault(record[attr], []).append(record)

    subset_entropy = 0
    for subset in subsets.values():
        p = len(subset) / total
        subset_entropy += p * entropy(subset, target_attr)

    return entropy(data, target_attr) - subset_entropy


def split_info(data, attr):
    total = len(data)
    counts = Counter(record[attr] for record in data)
    si = 0
    for count in counts.values():
        p = count / total
        if p > 0:
            si -= p * math.log2(p)
    return si


def gain_ratio(data, attr, target_attr):
    si = split_info(data, attr)
    if si == 0:
        return 0
    return info_gain(data, attr, target_attr) / si


def choose_best_attribute(data, attributes, target_attr):
    best_attr = None
    best_gr = -1
    total_entropy = entropy(data, target_attr)

    print("\n========================================")
    print(f"Entropy Dataset: {total_entropy:.4f}")
    print("========================================")

    for attr in attributes:
        subsets = {}
        for record in data:
            subsets.setdefault(record[attr], []).append(record)

        weighted_entropy = 0
        details = []
        for value, subset in subsets.items():
            ent = entropy(subset, target_attr)
            weighted_entropy += (len(subset) / len(data)) * ent
            details.append([value, len(subset), round(ent, 4)])

        si = split_info(data, attr)
        gr = (total_entropy - weighted_entropy) / si if si else 0

        print(f"\n[{attr}]")
        print(tabulate(details, headers=["Nilai", "Jumlah", "Entropy"], tablefmt="plain"))
        print(f"Entropy Atribut: {weighted_entropy:.4f}")
        print(f"Gain Ratio     : {gr:.4f}")

        if gr > best_gr:
            best_gr = gr
            best_attr = attr

    print(f"\n=> Atribut terbaik: {best_attr} (Gain Ratio = {best_gr:.4f})")
    return best_attr


def majority_class(data, target_attr):
    counts = Counter(record[target_attr] for record in data)
    return counts.most_common(1)[0][0]


def build_tree(data, attributes, target_attr):
    labels = [record[target_attr] for record in data]

    if len(set(labels)) == 1:
        return labels[0]
    if not attributes:
        return majority_class(data, target_attr)

    best_attr = choose_best_attribute(data, attributes, target_attr)
    tree = {best_attr: {}}

    attr_values = full_attr_values.get(best_attr, [])
    for value in attr_values:
        subset = [record for record in data if record[best_attr] == value]

        if not subset:
            tree[best_attr][value] = majority_class(data, target_attr)
        else:
            new_attributes = [a for a in attributes if a != best_attr]
            tree[best_attr][value] = build_tree(subset, new_attributes, target_attr)

    children = list(tree[best_attr].values())
    if children and all(not isinstance(v, dict) and v == children[0] for v in children):
        return children[0]

    return tree


def predict(tree, record, fallback):
    while isinstance(tree, dict):
        attr = next(iter(tree))
        value = record.get(attr)
        if value not in tree[attr]:
            return fallback
        tree = tree[attr][value]
    return tree


def build_anytree(tree, parent=None):
    if not isinstance(tree, dict):
        return Node(str(tree), parent=parent)

    attr = next(iter(tree))
    node = Node(str(attr), parent=parent)
    for value, subtree in tree[attr].items():
        child = build_anytree(subtree, parent=node)
        child.name = f"{value} : {child.name}"
    return node


# ==============================
# 5. Membentuk decision tree
# ==============================
attributes = list(train_df.columns)
attributes.remove("Label")

decision_tree = build_tree(train_data, attributes, "Label")

print("\n================ DECISION TREE ================")
root = build_anytree(decision_tree)
for pre, _, node in RenderTree(root):
    print(f"{pre}{node.name}")

# ==============================
# 6. Evaluasi
# ==============================
def accuracy_score_manual(tree, data, fallback):
    correct = 0
    for record in data:
        pred = predict(tree, record, fallback)
        if pred == record["Label"]:
            correct += 1
    return correct / len(data)


fallback = majority_class(train_data, "Label")
train_accuracy = accuracy_score_manual(decision_tree, train_data, fallback)
test_accuracy = accuracy_score_manual(decision_tree, test_data, fallback)

print(f"\nAkurasi Data Train: {train_accuracy * 100:.2f}%")
print(f"Akurasi Data Test : {test_accuracy * 100:.2f}%")
