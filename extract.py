import click
import json
import re
from pathlib import Path
from tqdm import tqdm
from typing import Optional


def extract_json_data(html_content: str) -> Optional[str]:
    """Extracts JSON data from the specified section of the HTML content using regular expressions."""
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        html_content,
        re.DOTALL,
    )
    if match:
        return match.group(1)
    return None


def process_html_files(output_folder: Path, html_files: list[Path]) -> None:
    """Processes each HTML file to extract JSON data and save it as a JSON file."""
    for html_file in tqdm(html_files, desc="Processing HTML files"):
        with open(html_file.as_posix(), "r", encoding="utf-8") as file:
            html_content = file.read()

        json_data = extract_json_data(html_content)
        if json_data:
            output_path = output_folder / (html_file.stem + ".json")
            with open(output_path, "w", encoding="utf-8") as json_file:
                json.dump(json.loads(json_data), json_file, indent=4)
        else:
            print(
                f"Could not find JSON data in {html_file.expanduser().resolve().as_posix()}!"
            )


@click.command()
@click.argument(
    "input_folder", type=click.Path(exists=True, file_okay=False, path_type=Path)
)
@click.argument("output_folder", type=click.Path(file_okay=False, path_type=Path))
def main(input_folder, output_folder):
    """Extracts JSON data from HTML files and saves it as JSON files."""
    html_files = [file for file in input_folder.iterdir() if file.suffix == ".html"]
    output_folder.mkdir(parents=True, exist_ok=True)
    process_html_files(output_folder, html_files)


if __name__ == "__main__":
    main()
