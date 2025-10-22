import json
from pathlib import Path
from datetime import datetime
from .data import *
from .utils import mix_soup, process_products, filter_new_in_stock, fetch_html

CWD = Path.cwd()


def process_urls():
    pricing_folder = CWD / "pricing"
    html_path = pricing_folder / "html"
    pricing_data_file = pricing_folder / "pricing_data.json"

    if not pricing_folder.exists():
        pricing_folder.mkdir()
    if not html_path.exists():
        html_path.mkdir()
    if not pricing_data_file.exists():
        pricing_data_file.touch()

    # Delete all html files in the html folder
    for html_file in html_path.iterdir():
        html_file.unlink()

    list_of_dict = [
        AMD_MOBO_URLS,
        AMD_CPU_URLS,
        RAM_URLS,
        PSU_URLS,
        GPU_URLS,
        M2_NVME_URLS,
        SATA_SSD_URLS,
    ]

    pricing_data: dict = {
        "__fetched__": datetime.now().isoformat(),
    }

    for d in list_of_dict:
        for k, v in d.items():
            file = html_path / f"{k}.html"

            if file.exists():
                file_data = file.read_text()
            else:
                file_data = fetch_html(v, file)

            soup = mix_soup(file_data)
            products = process_products(soup)
            pricing_data[k] = filter_new_in_stock(products)

    pricing_data_file.write_text(json.dumps(pricing_data, indent=4))


if __name__ == "__main__":
    process_urls()
