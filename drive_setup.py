import requests
from tqdm import tqdm
from google.colab import drive
import os

# Mount Google Drive
drive.mount('/content/drive')

# Save files to Google Drive
save_path = "/content/drive/MyDrive/ZenodoFiles/"
os.makedirs(save_path, exist_ok=True)

# Fetch metadata from Zenodo
record_id = "14669616"
url = f"https://zenodo.org/api/records/{record_id}"

response = requests.get(url)
data = response.json()

files = data.get("files", [])

for file_info in files:
    file_url = file_info["links"]["self"]
    file_name = file_info["key"]

    print(f"Downloading {file_name}...")

    # Streaming download to handle large files
    with requests.get(file_url, stream=True) as file_response:
        file_size = int(file_response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB

        # Progress bar setup
        t = tqdm(total=file_size, unit='iB', unit_scale=True, desc=file_name)

        with open(os.path.join(save_path, file_name), "wb") as f:
            for data in file_response.iter_content(block_size):
                t.update(len(data))
                f.write(data)

        t.close()

print("Download complete! Files saved to Google Drive.")
