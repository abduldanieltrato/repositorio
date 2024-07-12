names = []

with open("names.txt") as file:
    for line in sorted(file):
        names.append(line.rstrip())

for name in sorted(names, reverse=False):
    print(f"H, {name}")
