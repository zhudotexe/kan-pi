"""
Usage: python score_travelplanner.py [path/to/results.jsonl,...]

Outputs `results_for_tp_eval.json` files next to each input `results.jsonl` file.
"""

import asyncio
import glob
import json
import sys
from pathlib import Path

from redel.utils import read_jsonl

EXPECTED_RESULTS = 180
ID_TO_IDX_MAP = Path(__file__).parent / "experiments/travelplanner/id_to_idx.json"


async def transform_submission(fp: Path):
    """Read in the answers and generations and transform them all into the correct TP eval format."""
    results = read_jsonl(fp)
    split = fp.parents[1].name
    transformed = []
    try:
        with open(ID_TO_IDX_MAP) as f:
            id_to_idx = json.load(f)
    except FileNotFoundError:
        id_to_idx = {}

    for result in results:
        idx = result.get("idx", id_to_idx[result["id"]])
        query = result["question"]
        plan = result["plan"] or None

        # some stupid fixes for the eval script
        if plan:
            for day in plan:
                # every accommodation needs `, {CITY_NAME}` at the end (just tack on current city if missing)
                if day["accommodation"] and day["accommodation"] != "-" and not "," in day["accommodation"]:
                    *_, current_city = day["current_city"].split("to ")
                    day["accommodation"] += f", {current_city}"

        transformed.append({"idx": idx, "query": query, "plan": plan})

    # ensure there are the right number of results, and they're sorted by idx
    missing_idxs = set(range(EXPECTED_RESULTS)).difference({t["idx"] for t in transformed})
    if missing_idxs:
        print(f"WARN: Submission is missing indices {missing_idxs}")
        for idx in missing_idxs:
            transformed.append({"idx": idx, "query": None, "plan": None})
        transformed.sort(key=lambda t: t["idx"])

    result_fp = fp.parent / "results_for_tp_eval.jsonl"
    with open(result_fp, "w") as f:
        for transformed_result in transformed:
            f.write(json.dumps(transformed_result))
            f.write("\n")
    print(f"Written to {result_fp.resolve()}.")
    print("Use this command in TravelPlanning:")
    print(f"python eval.py --set_type {split} --evaluation_file_path {result_fp.resolve()}")
    return result_fp


async def main():
    paths = sys.argv[1:]
    if len(paths) == 1 and "*" in paths[0]:
        paths = glob.glob(paths[0], recursive=True)
    if not paths:
        print("no paths specified! Usage: python score_travelplanner.py [path/to/results.jsonl ...]")
    print(paths)
    for fp in paths:
        await transform_submission(Path(fp))
    print(
        "Now you should run the evaluation in the TravelPlanner repository (see"
        " https://github.com/OSU-NLP-Group/TravelPlanner#evaluation)."
    )


if __name__ == "__main__":
    asyncio.run(main())
