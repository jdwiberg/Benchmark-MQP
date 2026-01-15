import os


def make_key(dir_pref: str, start: int, end: int):
    for i in range(start, end+1):
        dir = dir_pref + str(i)
        for name in os.listdir(dir):
            if name == "entities.txt":
                filepath = os.path.join(dir, name)
                with open(filepath, "r") as f:
                    lines = ("").join(f.readlines())
                    index = lines.find("Relationship Triplets:")
                    raw = lines[index + 22 :]
                    clean = raw.split("```")[1].strip()
                    if clean.startswith("json"):
                        clean = clean[4:].strip()
                    with open(dir + "/key.json", "w") as out:
                        out.write(clean)


def remove_entities(dir_pref: str, start: int, end: int):
    for i in range(start, end+1):
        dir = dir_pref + str(i)
        for name in os.listdir(dir):
            if name == "entities.txt":
                filepath = os.path.join(dir, name)
                os.unlink(filepath)





