import requests
import os

save_folder = "static/img" 
os.makedirs(save_folder, exist_ok=True)

n = 50

for i in range(1, n + 1):
    url = "https://avatar.iran.liara.run/public"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = os.path.join(save_folder, f"{i}.png")
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"✅ images {i} saved: {filename}")
        else:
            print(f"error to get image {i}")
    except Exception as e:
        print(f"error: {e}")

print("END")