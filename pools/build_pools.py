from pathlib import Path
from faker import Faker
import random
import pandas as pd 


SEED=42
OUTPUT_DIR=Path(__file__).parent/"Output" #creating the output folder inside the parent folder

#setting up the customer size and the pool size 

N_CUSTOMER_NAMES=100000
N_DRIVER_NAME=15000
N_RESTAURANT_NAME=25000
N_ADDRESSES=35000
N_REVIEWS_PER_RATING=1000

fake=Faker("en_IN")
Faker.seed(SEED)
random.seed(SEED)


#CITIES AND LOCATIONS

CITIES=[
    ("Mumbai", "Maharashtra", 19.0760, 72.8777),
    ("Delhi", "Delhi", 28.6139, 77.2090),
    ("Bengaluru", "Karnataka", 12.9716, 77.5946),
    ("Hyderabad", "Telangana", 17.3850, 78.4867),
    ("Chennai", "Tamil Nadu", 13.0827, 80.2707),
    ("Pune", "Maharashtra", 18.5204, 73.8567),
    ("Kolkata", "West Bengal", 22.5726, 88.3639),
    ("Jaipur", "Rajasthan", 26.9124, 75.7873),
    ("Lucknow", "Uttar Pradesh", 26.8467, 80.9462),
    ("Ahmedabad", "Gujarat", 23.0225, 72.5714),
    ("Mathura", "Uttar Pradesh", 27.4924, 77.6737),
    ("Agra", "Uttar Pradesh", 27.1767, 78.0081),
    ("Surat", "Gujarat", 21.1702, 72.8311),
    ("Kanpur", "Uttar Pradesh", 26.4499, 80.3319),
    ("Nagpur", "Maharashtra", 21.1458, 79.0882),
    ("Indore", "Madhya Pradesh", 22.7196, 75.8577),
    ("Bhopal", "Madhya Pradesh", 23.2599, 77.4126),
    ("Patna", "Bihar", 25.5941, 85.1376),
    ("Vadodara", "Gujarat", 22.3072, 73.1812),
    ("Coimbatore", "Tamil Nadu", 11.0056, 76.9661),
    ("Ludhiana", "Punjab", 30.9010, 75.8573),
    ("Chandigarh", "Chandigarh", 30.7333, 76.7794),
    ("Kochi", "Kerala", 9.9312, 76.2673),
    ("Visakhapatnam", "Andhra Pradesh", 17.6868, 83.2185),
    ("Bhubaneswar", "Odisha", 20.2961, 85.8245),
    ("Guwahati", "Assam", 26.1445, 91.7362),
    ("Dehradun", "Uttarakhand", 30.3165, 78.0322),
    ("Ranchi", "Jharkhand", 23.3441, 85.3096),
]

ZONE_DIRECTIONS=["Central","North","South","East","West"]

CUISINES = ["North Indian", "South Indian", "Chinese", "Italian", "Fast Food","Biryani", "Desserts", "Street Food", "Healthy", "Mughlai"]

def add_pool_id(df: pd.DataFrame) ->pd.DataFrame:
    """pool_id runs 1..N so DuckDB can pick a row with a random number."""
    df.insert(0,"pool_id",range(1,len(df)+1))
    return df

##adding builder person pool 

def build_person_pool(n: int) ->pd.DataFrame:
    rows=[{"first_name":fake.first_name(),"Last_name":fake.last_name()}
          for _ in range(n)]
    return add_pool_id(pd.DataFrame(rows))

#adding the restraunt pools 

def build_restaurant_pool(n: int) ->pd.DataFrame:

    prefixes=["Spice", "Royal", "Tasty", "Golden", "Urban", "Desi", "Little",
                "Grand", "Fresh", "Hungry", "Punjabi", "Madras", "Bombay",
                "Delhi", "Chennai", "Tandoor", "Biryani", "Chai", "Curry"]

    suffixes=["Kitchen", "Dhaba", "Bistro", "Cafe", "Express", "House",
                "Corner", "Palace", "Junction", "Point", "Treats", "Darbar","Hotel"]

    rows=[]

    for _ in range(n):
        name=f"{random.choice(prefixes)} {random.choice(suffixes)}"
        if random.random()<0.5:
            name=f"{fake.last_name()}'s {name.split()[-1]}"
        rows.append({"restaurant_name":name,"cuisine_type":random.choice(CUISINES)})
    return add_pool_id(pd.DataFrame(rows))

#building the city pool 

def build_city_pool() ->pd.DataFrame:
    rows=[{"city":c,"state":s,"center_lat":lat,"center_lng":lng}
          for c,s,lat,lng in CITIES]
    return add_pool_id(pd.DataFrame(rows))

#building the zones

def build_zone_pool() -> pd.DataFrame:
    rows = [{"city": c, "delivery_zone": f"{c}-{d}"}
            for c, _, _, _ in CITIES for d in ZONE_DIRECTIONS]
    return add_pool_id(pd.DataFrame(rows))


#BUILDING THE ADDRESS 


def build_address_pool(n: int) -> pd.DataFrame:
    rows = []
    for _ in range(n):
        city, state, _, _ = random.choice(CITIES)
        rows.append({
            "street": fake.street_name(),
            "area": fake.city_suffix().title() + " Nagar",
            "city": city,
            "pincode": fake.postcode(),
        })
    return add_pool_id(pd.DataFrame(rows))

#building the menu

def build_menu_catalog() -> pd.DataFrame:
    # (item_name, category, base_price, is_veg)
    catalog = {
        "North Indian": [("Paneer Butter Masala", "Main Course", 260, True),
                         ("Dal Makhani", "Main Course", 220, True),
                         ("Butter Chicken", "Main Course", 320, False),
                         ("Butter Naan", "Breads", 50, True),
                         ("Chole Bhature", "Main Course", 180, True),
                         ("Tandoori Roti", "Breads", 25, True),
                         ("Jeera Rice", "Rice", 120, True),
                         ("Lassi", "Beverages", 70, True)],
        "South Indian": [("Masala Dosa", "Main Course", 120, True),
                         ("Idli Sambar", "Breakfast", 90, True),
                         ("Medu Vada", "Starters", 80, True),
                         ("Uttapam", "Main Course", 130, True),
                         ("Filter Coffee", "Beverages", 60, True),
                         ("Curd Rice", "Rice", 100, True),
                         ("Rava Dosa", "Main Course", 140, True),
                         ("Chicken Chettinad", "Main Course", 290, False)],
        "Chinese": [("Veg Hakka Noodles", "Main Course", 170, True),
                    ("Chicken Manchurian", "Starters", 240, False),
                    ("Veg Fried Rice", "Rice", 160, True),
                    ("Spring Roll", "Starters", 140, True),
                    ("Chilli Paneer", "Starters", 230, True),
                    ("Hot and Sour Soup", "Soups", 110, True),
                    ("Chicken Fried Rice", "Rice", 200, False),
                    ("Schezwan Noodles", "Main Course", 190, True)],
        "Italian": [("Margherita Pizza", "Pizza", 280, True),
                    ("Penne Arrabbiata", "Pasta", 260, True),
                    ("Garlic Bread", "Starters", 120, True),
                    ("Farmhouse Pizza", "Pizza", 340, True),
                    ("Pasta Alfredo", "Pasta", 290, True),
                    ("Chicken Pepperoni Pizza", "Pizza", 380, False),
                    ("Lasagna", "Main Course", 350, False),
                    ("Tiramisu", "Desserts", 190, True)],
        "Fast Food": [("Veg Burger", "Burgers", 110, True),
                      ("Chicken Burger", "Burgers", 160, False),
                      ("French Fries", "Sides", 90, True),
                      ("Veg Sandwich", "Sandwiches", 100, True),
                      ("Chicken Wrap", "Wraps", 170, False),
                      ("Cold Coffee", "Beverages", 120, True),
                      ("Onion Rings", "Sides", 100, True),
                      ("Chicken Nuggets", "Sides", 150, False)],
        "Biryani": [("Chicken Biryani", "Biryani", 280, False),
                    ("Veg Biryani", "Biryani", 220, True),
                    ("Mutton Biryani", "Biryani", 380, False),
                    ("Egg Biryani", "Biryani", 210, False),
                    ("Raita", "Sides", 40, True),
                    ("Paneer Biryani", "Biryani", 250, True),
                    ("Mirchi Ka Salan", "Sides", 80, True),
                    ("Phirni", "Desserts", 90, True)],
        "Desserts": [("Gulab Jamun", "Desserts", 80, True),
                     ("Chocolate Brownie", "Desserts", 120, True),
                     ("Rasmalai", "Desserts", 110, True),
                     ("Ice Cream Sundae", "Desserts", 140, True),
                     ("Jalebi", "Desserts", 70, True),
                     ("Kulfi", "Desserts", 90, True),
                     ("Cheesecake", "Desserts", 180, True),
                     ("Gajar Halwa", "Desserts", 100, True)],
        "Street Food": [("Pav Bhaji", "Main Course", 130, True),
                        ("Vada Pav", "Snacks", 40, True),
                        ("Pani Puri", "Snacks", 60, True),
                        ("Aloo Tikki", "Snacks", 70, True),
                        ("Samosa", "Snacks", 30, True),
                        ("Dahi Puri", "Snacks", 80, True),
                        ("Egg Roll", "Snacks", 90, False),
                        ("Kathi Roll", "Snacks", 120, False)],
        "Healthy": [("Greek Salad", "Salads", 180, True),
                    ("Quinoa Bowl", "Bowls", 250, True),
                    ("Fruit Bowl", "Bowls", 150, True),
                    ("Sprouts Chaat", "Snacks", 120, True),
                    ("Grilled Paneer Salad", "Salads", 230, True),
                    ("Grilled Chicken Bowl", "Bowls", 280, False),
                    ("Green Smoothie", "Beverages", 140, True),
                    ("Oats Porridge", "Breakfast", 110, True)],
        "Mughlai": [("Chicken Korma", "Main Course", 330, False),
                    ("Seekh Kebab", "Starters", 260, False),
                    ("Mutton Rogan Josh", "Main Course", 400, False),
                    ("Shahi Paneer", "Main Course", 270, True),
                    ("Rumali Roti", "Breads", 35, True),
                    ("Malai Kofta", "Main Course", 250, True),
                    ("Chicken Tikka", "Starters", 280, False),
                    ("Shahi Tukda", "Desserts", 120, True)],
    }
    styles = ["freshly prepared", "chef's special", "made with authentic spices",
              "a customer favourite", "served hot", "made to order"]
    rows = []
    for cuisine, items in catalog.items():
        for name, category, price, is_veg in items:
            kind = "vegetarian" if is_veg else "non-vegetarian"
            rows.append({
                "item_name": name,
                "cuisine_type": cuisine,
                "category": category,
                "base_price": price,
                "is_veg": is_veg,
                "description": f"{name}, {random.choice(styles)}. A {kind} {cuisine} dish.",
            })
    return add_pool_id(pd.DataFrame(rows))


#building the review 

def build_review_pool(n_per_rating: int) -> pd.DataFrame:
    openers = {
        5: ["Absolutely loved it.", "Outstanding meal!", "Best order in a long time.", "Superb quality.","Highly Recommended","Best decision ever"],
        4: ["Really good food.", "Quite satisfied.", "Pretty great overall.", "Tasty and fresh."],
        3: ["It was okay.", "Average experience.", "Decent but nothing special.", "Mixed feelings.","Can improve!!"],
        2: ["Not very happy.", "Below expectations.", "Disappointing meal.", "Could be much better."],
        1: ["Terrible experience.", "Worst order ever.", "Very poor quality.", "Completely unsatisfied."],
    }
    middles = {
        5: ["The food arrived hot and fresh.", "Portion size was generous.", "Flavours were perfectly balanced.", "Packaging was neat."],
        4: ["Delivery was quick.", "Taste was good, portion was fair.", "Food was warm on arrival.", "Good value for money."],
        3: ["Taste was average.", "Delivery took a bit long.", "Portion was small for the price.", "Food was lukewarm."],
        2: ["Food was cold on arrival.", "Delivery was very late.", "Some items were missing.", "Too oily and bland."],
        1: ["Food was stale and cold.", "Order arrived extremely late.", "Wrong items delivered.", "Packaging was spilled and messy."],
    }
    closers = {
        5: ["Will order again!", "Highly recommended.", "Five stars from me.", "Never disappoints."],
        4: ["Will order again.", "Recommended.", "Worth trying.", "Good job."],
        3: ["Might try again.", "Needs improvement.", "Fine for a quick meal.", "Hit or miss."],
        2: ["Will not repeat soon.", "Please improve quality.", "Expected more.", "Not worth the price."],
        1: ["Will never order again.", "Requesting a refund.", "Avoid this place.", "Very disappointed."],
    }
    rows = []
    for rating in range(1, 6):
        for _ in range(n_per_rating):
            text = " ".join([random.choice(openers[rating]),
                             random.choice(middles[rating]),
                             random.choice(closers[rating])])
            rows.append({"rating": rating, "review_text": text})
    return add_pool_id(pd.DataFrame(rows))


def save(df: pd.DataFrame, filename: str) -> None:
    path = OUTPUT_DIR / filename
    df.to_parquet(path, index=False)
    size_kb = path.stat().st_size / 1024
    print(f"  {filename:<28} {len(df):>7,} rows   {size_kb:>8.1f} KB")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Building pools into: {OUTPUT_DIR}\n")

    save(build_person_pool(N_CUSTOMER_NAMES), "customer_names.parquet")
    save(build_person_pool(N_DRIVER_NAME), "driver_names.parquet")
    save(build_restaurant_pool(N_RESTAURANT_NAME), "restaurant_names.parquet")
    save(build_city_pool(), "cities.parquet")
    save(build_zone_pool(), "city_zones.parquet")
    save(build_address_pool(N_ADDRESSES), "street_addresses.parquet")
    save(build_menu_catalog(), "menu_catalog.parquet")
    save(build_review_pool(N_REVIEWS_PER_RATING), "review_texts.parquet")

    print("\nDone. Pools are ready for DuckDB.")


if __name__ == "__main__":
    main()







