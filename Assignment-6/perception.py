import json

def get_rm_profile():
    while True:
        name = input("Enter your RM name: ").strip()
        with open("data/rm_performance.json", "r") as f:
            data = json.load(f)
        for rm in data:
            if rm['name'].lower() == name.lower():
                return rm
        print("❌ RM not found. Please enter a valid RM name to continue.")