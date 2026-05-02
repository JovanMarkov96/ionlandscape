import os
from geopy.geocoders import Nominatim
import re

geolocator = Nominatim(user_agent="ionlandscape_updater")

companies = {
    "c007-quantum-machines.md": "HaMasger Street 35, Tel Aviv-Yafo, Israel",
    "c008-classiq-technologies.md": "Daniel Frisch 3, Tel Aviv, Israel",
    "c004-qedma.md": "Rokach Blvd 101, Tel Aviv, Israel",
    "c005-quantum-source-labs.md": "Ramon Ilan 3, Ness Ziona, Israel",
    "c006-quamcore.md": "Maskit St 10, Herzliya, Israel",
    "c009-quantlr.md": "2 HaMaayan Street, Modi'in, Israel",
    "c010-quantum-transistors.md": "Binyamina, Israel",
    "c011-quancilla.md": "Tel Aviv, Israel",
    "c012-enquantum.md": "23 Harokmim Street, Holon, Israel"
}

dir_path = "content/companies/"

for filename, address in companies.items():
    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(filepath):
        print(f"Skipping {filename}, not found.")
        continue
        
    try:
        location = geolocator.geocode(address)
        if location:
            print(f"Found {filename}: {location.latitude}, {location.longitude} ({address})")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            content = re.sub(r'lat: [0-9.]+', f'lat: {location.latitude:.4f}', content)
            content = re.sub(r'lon: [0-9.]+', f'lon: {location.longitude:.4f}', content)
            
            # Additional logic for Modi'in and Binyamina and Holon
            if "Modi'in" in address:
                content = re.sub(r'city: .*', "city: Modi'in", content)
                content = re.sub(r'region: .*', "region: Central", content)
            elif "Binyamina" in address:
                content = re.sub(r'city: .*', f'city: Binyamina', content)
                content = re.sub(r'region: .*', f'region: Haifa', content)
            elif "Holon" in address:
                content = re.sub(r'city: .*', f'city: Holon', content)
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            print(f"Could not geolocate {address} for {filename}")
    except Exception as e:
        print(f"Error {filename}: {e}")

print("Done.")
