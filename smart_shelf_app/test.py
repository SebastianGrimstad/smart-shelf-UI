from API import fetch_shelf_data  # Import the function

# Fetch data for a specific shelf
grouped_data = fetch_shelf_data("smart_shelf_1")

# ✅ Use grouped_data inside another script
if grouped_data:
    for shelf_id, shelf_items in grouped_data.items():
        print(f"\n📦 Shelf ID: {shelf_id}")
        print("=" * 40)
        for item in shelf_items:
            print(item)
else:
    print("No data found.")
