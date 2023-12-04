import click
import requests
from tqdm import tqdm
from typing import Optional


@click.command()
@click.option(
    "--cookie",
    "-c",
    required=True,
    type=str,
    help="The cookie to be used in the request.",
)
@click.option(
    "--max-number",
    "-m",
    default=1000,
    type=int,
    help="The maximum number for the loop variable.",
)
@click.option(
    "--save-to",
    "-s",
    "-o",
    type=click.Path(),
    default=None,
    help="The folder to save the html results to.",
)
def send_requests(cookie: str, max_number: int, save_to: Optional[str]):
    """Sends HTTP requests to a specified URL with a cookie."""
    base_url = "https://os.contrary.com/dashboard/profile/"
    got_count = 0
    for number in tqdm(range(max_number), desc="Sending Requests"):
        url = f"{base_url}{number}"
        headers = {"Cookie": cookie}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            got_count += 1
            if save_to is not None:
                url_as_name = (
                    url.replace("/", "_").replace(".", "_").replace("https:", "")
                )
                with open(f"{save_to}/{url_as_name}.html", "w") as f:
                    f.write(response.text)
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")

    # NOTE: you'll want to confirm that this matches a quick eyeball of how many there were
    # There should be 27*14 + 12 = 390 valid URLs at least
    click.echo(f"Found {got_count} valid URLs in total!")


if __name__ == "__main__":
    send_requests()
