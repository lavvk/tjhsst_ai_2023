import math
import sys

def parse_line(line, cat):
    temp = line.split(",")
    row = {}
    for i in range(len(cat)):
        row[cat[i]] = temp[i]
    return row

def entropy(data, cat):
    outcomes = {}
    outcome_cat = cat[-1]
    for row in data:
        outcome = row[outcome_cat]
        outcomes[outcome] = outcomes.get(outcome, 0) + 1
    ent = 0
    for count in outcomes.values():
        prob = count / len(data)
        ent -= prob * math.log(prob, 2)
    return ent

def info(feature, data, cat):
    vals = {}
    for row in data:
        val = row[feature]
        if val not in vals:
            vals[val] = [row]
        else:
            vals[val].append(row)
    ent = 0
    for subset in vals.values():
        prob = len(subset) / len(data)
        ent += prob * entropy(subset, cat)
    gain = entropy(data, cat) - ent
    return gain

def gen_subtree(subtree, data, cat, best_feat):
    vals = {}
    for row in data:
        val = row[best_feat]
        if val not in vals:
            vals[val] = [row]
        else:
            vals[val].append(row)
    for value, subset in vals.items():
        subtree[best_feat][value] = {}
        if entropy(subset, cat) == 0:
            subtree[best_feat][value] = subset[0][cat[-1]]
        else:
            gen_tree(subtree[best_feat][value], subset, cat)

def gen_tree(tree, data, cat):
    best_feat = ""
    highest_gain = 0
    for feat in cat[:-1]:
        gain = info(feat, data, cat)
        if gain > highest_gain:
            highest_gain = gain
            best_feat = feat
    tree[best_feat] = {}
    gen_subtree(tree, data, cat, best_feat)
    return tree

def format(tree, f, indent=0):
    for key, value in tree.items():
        print("\t" * indent + "* " + str(key), end="", file=f)
        if isinstance(value, dict):
            print("", file=f)
            format(value, f, indent + 1)
        else:
            print(" --> " + str(value), file=f)

def read_csv(file_path):
    cat = []
    data = []

    with open(file_path) as f:
        count = 0
        for line in f:
            line = line.strip()
            if count == 0:
                cat = line.split(",")
                count += 1
            else:
                data.append(parse_line(line, cat))
    return cat, data

cat, data = read_csv(sys.argv[1])
tree = gen_tree({}, data, cat)

with open("treeout.txt", "w") as f:
    format(tree, f)
