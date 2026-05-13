import json
from pathlib import Path

BUILD_MANIFEST = Path(".build/__local__.json")
OUTPUT_DIR = Path("output")


def _iter_project_contracts(manifest: dict):
    for name, contract in manifest.get("contractTypes", {}).items():
        source_id = contract.get("sourceId", "")
        if source_id.startswith("contracts/"):
            yield name, contract


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    for existing_file in OUTPUT_DIR.glob("*.json"):
        existing_file.unlink()

    with BUILD_MANIFEST.open("r", encoding="utf-8") as file:
        manifest = json.load(file)

    for name, contract_json in _iter_project_contracts(manifest):
        output = {"abi": contract_json["abi"]}

        deployment = contract_json.get("deploymentBytecode", {})
        runtime = contract_json.get("runtimeBytecode", {})
        if "bytecode" in deployment:
            output["bytecode"] = deployment["bytecode"]
        if "bytecode" in runtime:
            output["deployedBytecode"] = runtime["bytecode"]

        with (OUTPUT_DIR / f"{name}.json").open("w", encoding="utf-8") as file:
            json.dump(output, file, indent=2)
            file.write("\n")


if __name__ == "__main__":
    main()
