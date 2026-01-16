import os
import json
from datasets import load_dataset

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


def make_list(start: int, end: int):
    dir_pref = "gold_standard/"
    for i in range(start, end+1):
        dir = dir_pref + str(i)
        for file in os.listdir(dir):
            if file == 'key.json':
                with open(os.path.join(dir, file), 'r') as f:
                    lines = f.readlines()

                    for idx, line in enumerate(lines):
                        if 'target_entity' in line and '[' not in line:
                            lines[idx] = line[:23] + '[' + line[23:-2] + ']' + line[-2:]

                    with open(os.path.join(dir, "key2.json"), 'w') as f:
                        f.writelines(lines)

def make_full_json(start: int, end: int):
    dir_pref = "gold_standard/"
    for i in range(start, end+1):
        dir = dir_pref + str(i)
        for file in os.listdir(dir):
            pth = os.path.join(dir, file)
            text = []

            pth_key = os.path.join(dir, "key.json")
            pth_text = os.path.join(dir, f"{i}gs.txt")
            with open(pth_key, "r") as k:
                key = json.load(k)
                with open(pth_text, "r") as t:
                    text = "".join(t.readlines())
                    with open(os.path.join(dir, "data.json"), 'w') as out:
                        full = {
                            "text": text,
                            "key": key
                        }
                        json.dump(full, out, indent=4)
                        out.close()
                        t.close()
                        k.close()

def rename_all():
    for i in range(0, 100):
        dir = "gold_standard/" + str(i)
        new_dir = "gs_jsons/"
        for name in os.listdir(dir):
            pth = os.path.join(dir, name)
            if name == f"{i}_gs_data.json":
                os.rename(pth, os.path.join(new_dir, f"{i}_gs_data.json"))

def debug():
    dir = "gs_jsons/"
    for name in os.listdir(dir):
        with open(os.path.join(dir, name), "r") as f:
            lines = f.readlines()
            for line in lines:
                if "relational_category" in line:
                    print(name)
            f.close()

def hf_pipeline():
    ds = load_dataset("json", data_files={"test": "gs_jsons/*.json"})
    ds.push_to_hub("jdwiberg/benchmark-mqp-gs")
    return ds

def main():
    pass


if __name__ == "__main__":
    # make_key("gold_standard/", 0, 99)
    # remove_entities("gold_standard/", 0, 99)
    # make_list(0, 99)
    # make_full_json(0, 99)
    # rename_all()
    # debug()
    # hf_pipeline()
    main()
