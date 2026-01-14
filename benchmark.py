import os
import json
import copy
from rapidfuzz import fuzz
import math

class GSJudge:
    
    def __init__(self, *, gs_data_path="Data/gold_standard", comps_data_path="Data/comps"): 
        self.gs = self._load_json(gs_data_path) # List of JSON objects
        self.comps = self._load_json(comps_data_path)
        
    def _load_json(self, data_path: str):
        result = []
        for dirpath, _, filenames in os.walk(data_path):
            for file in filenames:
                if file == 'key.json':
                    filepath = os.path.join(dirpath, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        extraction = json.load(f)
                        result.append(extraction)
        return result
    
    def find_match(self, triplet_idx: int, triplet: dict, search_space: list[dict]) -> tuple[int, float]: # Find a "match"'s index for triplet in search space
        # Find the triplet in search space that most closely corresponds with triplet
        b_score = 0
        b_index = None
        for index, t_comp in enumerate(search_space):
            score = self.compare_triplets(triplet_idx, triplet, index, t_comp, loc=True)
            if score > b_score:
                b_index = index
                b_score = score

        if b_index is None: # this should not happen (fingers crossed)
            return (0, 0)

        b_score = self.compare_triplets(triplet_idx, triplet, b_index, search_space[b_index])
        return (b_index, b_score)  
    
    def compare_triplets(self, t1_idx: int, t1: dict, t2_idx: int, t2: dict, *, loc=False) -> float:
        # on a scale of 0-1, how well does t1 match t2
        # compare target_entity, relation_category, relational_entity

        te_score = max(
            fuzz.ratio(t1["target_entity"], t2["target_entity"]),
            fuzz.partial_ratio(t1["target_entity"], t2["target_entity"]),
            fuzz.token_set_ratio(t1["target_entity"], t2["target_entity"])
        ) / 100
        re_score = max(
            fuzz.ratio(t1["relational_entity"], t2["relational_entity"]),
            fuzz.partial_ratio(t1["relational_entity"], t2["relational_entity"]),
            fuzz.token_set_ratio(t1["relational_entity"], t2["relational_entity"])
        ) / 100
        
        c1 = t1["relation_category"]
        c2 = t2["relation_category"]
        if c1 == c2:
            cat_score = 1
        elif c1 == "DR" or c2 == "DR": # DR vs not DR is important, everything else can be more ambiguous
            cat_score = 0
        else:
            cat_score = 0.8

 
        loc_score = ((abs(t1_idx - t2_idx)) ** (1/4))
        if loc_score == 0:
            loc_score = 1
        else:
            loc_score = 1 / loc_score

        # Target and relational entity classification is very important for matching, category less so
        if loc:
            return (te_score * 0.2) + (re_score * 0.35) + (cat_score * 0.1) + (0.35 * loc_score)
        return (te_score * 0.4) + (re_score * 0.5) + (cat_score * 0.1)
    
    @staticmethod
    def zero_duplicates(map: dict) -> dict:
        best_matches = {}
        for triplet, (index, score) in map.items():
            if index not in best_matches or score > best_matches[index][1]:
                best_matches[index] = (triplet, score)

        unique = {
            triplet: (index, score) for index, (triplet, score) in best_matches.items()
        }

        for triplet in map.keys():
            if triplet not in unique.keys():
                map[triplet] = (0, 0)

        return map

    def pr_score(self, gs_key: list[dict], comp_key: list[dict]) -> tuple[float, float]:
        gs_key = copy.deepcopy(gs_key)
        comp_key = copy.deepcopy(comp_key)

        # Of all things the model predicted, how many were correct? = precision
        # Of all correct answers, how many did the model find? = recall
        
        # make a map of predictions -> (best gs index, score)
        prec_map = {}
        # make a map of prediction -> (best comp index, score)
        rec_map = {}
        for index, triplet in enumerate(comp_key):
            str_key = json.dumps(triplet, sort_keys=True)
            prec_map[str_key] = self.find_match(index, triplet, gs_key)
        for index, triplet in enumerate(gs_key):
            str_key = json.dumps(triplet, sort_keys=True)
            rec_map[str_key] = self.find_match(index, triplet, comp_key)

        prec_map = self.zero_duplicates(prec_map)
        rec_map = self.zero_duplicates(rec_map)

        prec_score = sum([score for (_, score) in prec_map.values()]) / len(prec_map.keys())
        rec_score = sum([score for (_, score) in rec_map.values()]) / len(rec_map.keys())

        return (prec_score, rec_score)
    
    @staticmethod
    def _get_color(num) -> str:
        RED = "\033[31m"
        GREEN = "\033[32m"
        YELLOW = "\033[33m"

        if num >= 0.75:
            return GREEN
        if num < 0.25:
            return RED
        return YELLOW

    def compare(self):
        if len(self.gs) != len(self.comps):
            self.gs = self.gs[:len(self.comps)]

        print(len(self.gs), "gold standard entries vs", len(self.comps), "comp entries")
        precision, recall, avg = 0, 0, 0
        for gs_key, comp_key in zip(self.gs, self.comps):
            p, r = self.pr_score(gs_key["relationship_triplets"], comp_key["relationship_triplets"])
            a = (p + r) / 2

            print(p, r, a)
            # Collect total for precision, recall
            precision += p
            recall += r
            avg += a

        # Average out precision and recall scores
        precision, recall, avg = (x / len(self.comps) for x in (precision, recall, avg))

        RESET = "\033[0m"
        print(f"{self._get_color(precision)}Precision: {precision}")
        print(f"{self._get_color(recall)}Recall: {recall} {RESET}")
        print(f"{self._get_color(avg)}Average: {avg} {RESET}")
        

def main():
    judge = GSJudge(gs_data_path="Data/gold_standard/", comps_data_path="Data/comps/")
    judge.compare()


# if __name__ == "__main__":
#     main()
