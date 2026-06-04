import os
import urllib.request
import frontmatter

# Define domains for logos
companies = {
    "c010-quantum-transistors": {
        "domain": "quantumtransistors.com",
        "founders": [
            {"name": "Shmuel Bachinsky", "role": "CEO & Co-Founder"},
            {"name": "Moshe Tordjman", "role": "CTO & Co-Founder"}
        ],
        "website": "https://quantumtransistors.com",
        "funding": {
            "total_raised_usd": 18500000,
            "rounds": [
                {
                    "date": "2024-01-01",
                    "round": "Grant/Seed",
                    "stage": "seed",
                    "amount_usd": 18500000,
                    "other_investors": ["European Innovation Council", "10D", "Awz Ventures", "Entrée Capital", "Tal Ventures"]
                }
            ]
        },
        "milestones": [
            {"date": "2025-12-01", "claim": "Achieved quantum gate fidelity of 99.9988%", "source_url": "https://techtime.news"}
        ]
    },
    "c011-quancilla": {
        "domain": "quancilla.com",
        "founders": [
            {"name": "Saar Barak", "role": "Co-Founder"},
            {"name": "Uri Almedon", "role": "Co-Founder"}
        ],
        "website": "https://quancilla.com"
    },
    "c012-enquantum": {
        "domain": "enquantum.io",
        "founders": [
            {"name": "Roman Vercetti", "role": "Founder"}
        ],
        "website": "https://enquantum.io",
        "status": {
            "acquired": {
                "is_acquired": True,
                "acquired_by": "Reliance Global Group",
                "acquisition_date": "2026-01-01",
                "deal_value_usd": 2041000
            }
        }
    },
    "c013-qedma": {
        "domain": "qedma.com",
        "founders": [
            {"name": "Asif Sinay", "role": "CEO & Co-Founder"},
            {"name": "Dorit Aharonov", "role": "CSO & Co-Founder"},
            {"name": "Netanel Lindner", "role": "CTO & Co-Founder"}
        ],
        "website": "https://qedma.com",
        "funding": {
            "total_raised_usd": 30700000,
            "rounds": [
                {
                    "date": "2025-07-01",
                    "round": "Series A",
                    "stage": "series_a",
                    "amount_usd": 26000000,
                    "lead_investors": ["Glilot Capital Partners"],
                    "other_investors": ["IBM", "Korea Investment Partners", "TPY Capital"]
                }
            ]
        }
    },
    "c015-quamcore": {
        "domain": "quamcore.com",
        "founders": [
            {"name": "Alon Cohen", "role": "CEO & Co-Founder"},
            {"name": "Shay Hacohen-Gourgy", "role": "CTO & Co-Founder"},
            {"name": "Serge Rosenblum", "role": "Chief Scientist & Co-Founder"}
        ],
        "website": "https://quamcore.com",
        "funding": {
            "total_raised_usd": 35000000,
            "rounds": [
                {
                    "date": "2025-08-01",
                    "round": "Series A",
                    "stage": "series_a",
                    "amount_usd": 26000000,
                    "lead_investors": ["Sentinel Global"],
                    "other_investors": ["Arkin Capital"]
                },
                {
                    "date": "2025-03-01",
                    "round": "Seed",
                    "stage": "seed",
                    "amount_usd": 9000000,
                    "lead_investors": ["Viola Ventures"],
                    "other_investors": ["Earth & Beyond Ventures", "Surround Ventures"]
                }
            ]
        }
    }
}

root = r"d:\OneDrive - weizmann.ac.il\GitHub\quantum-landscape"
logos_dir = os.path.join(root, "website", "static", "logos")
content_dir = os.path.join(root, "content", "companies")

for cid, data in companies.items():
    # 1. Download logo
    logo_path = os.path.join(logos_dir, f"{cid}.png")
    logo_url = f"https://www.google.com/s2/favicons?domain={data['domain']}&sz=128"
    try:
        urllib.request.urlretrieve(logo_url, logo_path)
        print(f"Downloaded logo for {cid}")
    except Exception as e:
        print(f"Failed to download logo for {cid}: {e}")

    # 2. Update markdown
    md_path = os.path.join(content_dir, f"{cid}.md")
    if os.path.exists(md_path):
        post = frontmatter.load(md_path)
        meta = post.metadata
        
        # update logo
        if "media" not in meta or meta["media"] is None:
            meta["media"] = {}
        meta["media"]["logo_path"] = f"/logos/{cid}.png"
        
        # update links
        if "links" not in meta or meta["links"] is None:
            meta["links"] = {}
        meta["links"]["website"] = data["website"]
        
        # update founders
        if "people" not in meta or meta["people"] is None:
            meta["people"] = {}
        if "founders" in data:
            meta["people"]["founders"] = data["founders"]
            
        # update funding
        if "funding" in data:
            meta["funding"] = data["funding"]
            
        # update milestones
        if "milestones" in data:
            if "milestones" not in meta or not meta["milestones"]:
                meta["milestones"] = data["milestones"]
            else:
                meta["milestones"].extend(data["milestones"])
                
        # update status
        if "status" in data:
            if "status" not in meta or meta["status"] is None:
                meta["status"] = data["status"]
            else:
                meta["status"].update(data["status"])
                
        # Write back
        post.metadata = meta
        with open(md_path, "wb") as f:
            frontmatter.dump(post, f)
        print(f"Updated {cid}.md")
        
        # Update evidence map
        evidence_path = os.path.join(content_dir, f"{cid}.evidence.md")
        evidence_content = f"# Evidence Map: {meta.get('name', cid)}\n## Sources\n1. [{data['domain']}]({data['website']})\n"
        with open(evidence_path, "w") as f:
            f.write(evidence_content)
        print(f"Updated {cid}.evidence.md")

print("Done.")
