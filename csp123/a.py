# -*- coding: utf-8 -*-
"""
TripGenie – Smart Gateway to Your Destination
AI-Assisted, Mood-Based Tourism and Local Heritage Trip Planning Web Application
B.Tech Artificial Intelligence and Data Science | Community Service Project (CSP)
"""

import streamlit as st
import pandas as pd
import random
import string
import requests
import math
import datetime

# ============================================================================
# 1. PAGE CONFIGURATION & THEME
# ============================================================================
st.set_page_config(
    page_title="TripGenie – Smart Gateway to Your Destination",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# University Project Styling: Professional Slate, Deep Navy, and Amber Accents
st.markdown("""
<style>
/* Main Container Styling */
.stApp {
    background-color: #f8fafc !important;
    color: #0f172a !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* Hero Banner */
.hero-block {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 60%, #38bdf8 100%);
    border-radius: 14px;
    padding: 32px 36px;
    color: white !important;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.15);
}

.hero-title {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
    color: #ffffff !important;
}

.hero-subtitle {
    font-size: 16px;
    opacity: 0.95;
    margin-bottom: 12px;
    font-weight: 400;
    color: #e0f2fe !important;
}

.hero-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(6px);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    color: #ffffff !important;
}

/* Clean Elevated Cards */
.card {
    background: #ffffff;
    border-radius: 12px;
    padding: 22px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
    border: 1px solid #e2e8f0;
    margin-bottom: 20px;
}

/* Day Itinerary Box */
.day-card {
    background: #ffffff;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 14px;
    border-left: 4px solid #2563eb;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    border-top: 1px solid #f1f5f9;
    border-right: 1px solid #f1f5f9;
    border-bottom: 1px solid #f1f5f9;
}

.day-header {
    font-size: 18px;
    font-weight: 700;
    color: #1e3a8a;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Activity Row */
.activity-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 6px 0;
    font-size: 14.5px;
    color: #334155;
    border-bottom: 1px dashed #f1f5f9;
}

.activity-row:last-child {
    border-bottom: none;
}

.activity-time {
    font-weight: 700;
    color: #2563eb;
    min-width: 60px;
    font-family: monospace;
    font-size: 13.5px;
}

/* Heritage Highlight Box */
.heritage-box {
    background: #fffbeb;
    border: 1px solid #fef3c7;
    border-left: 4px solid #f59e0b;
    border-radius: 10px;
    padding: 16px;
    margin-top: 16px;
    color: #78350f;
}

/* Budget Metric Pill */
.budget-pill {
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 8px;
    padding: 12px;
    text-align: center;
}

.budget-val {
    font-size: 20px;
    font-weight: 800;
    color: #1e3a8a;
}

.budget-lbl {
    font-size: 12px;
    color: #64748b;
    text-transform: uppercase;
    font-weight: 600;
}

/* Assistant Chat Bubbles */
.chat-genie {
    background: #f1f5f9;
    color: #0f172a;
    padding: 10px 14px;
    border-radius: 10px 10px 10px 2px;
    margin-bottom: 10px;
    font-size: 14px;
    border: 1px solid #e2e8f0;
}

.chat-user {
    background: #2563eb;
    color: #ffffff !important;
    padding: 10px 14px;
    border-radius: 10px 10px 2px 10px;
    margin-bottom: 10px;
    text-align: right;
    font-size: 14px;
    margin-left: 20px;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%) !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    box-shadow: 0 6px 18px rgba(37, 99, 235, 0.35) !important;
    transform: translateY(-1px) !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# 2. DOMAIN KNOWLEDGE BASE: TERRAINS, HERITAGE & DESTINATION CLASSIFICATION
# ============================================================================

DESTINATION_CATALOG = {
    # Coastal / Beach Destinations
    "goa": {
        "terrain": "coastal",
        "state": "Goa",
        "heritage": "Basilica of Bom Jesus (UNESCO Site), Aguada Fort, Chapora Fort, Mangueshi Temple",
        "food": "Goan Fish Curry, Prawn Balchão, Bebinca, Poi bread",
        "best_time": "Mid-November to mid-February (pleasant breezy climate)",
        "lat": 15.2993, "lon": 74.1240
    },
    "visakhapatnam": {
        "terrain": "coastal",
        "state": "Andhra Pradesh",
        "heritage": "Submarine Museum, Thotlakonda Buddhist Complex, Simhachalam Temple, Borra Caves",
        "food": "Bongu Chicken, Andhra Royyala Vepudu (Prawn Fry), Pootharekulu",
        "best_time": "October to March (cool sea breeze)",
        "lat": 17.6868, "lon": 83.2185
    },
    "vizag": {
        "terrain": "coastal",
        "state": "Andhra Pradesh",
        "heritage": "Submarine Museum, Thotlakonda Buddhist Complex, Simhachalam Temple, Borra Caves",
        "food": "Bongu Chicken, Andhra Royyala Vepudu, Pootharekulu",
        "best_time": "October to March",
        "lat": 17.6868, "lon": 83.2185
    },
    "pondicherry": {
        "terrain": "coastal",
        "state": "Puducherry",
        "heritage": "Auroville, Sri Aurobindo Ashram, French War Memorial, Promenade Heritage Walk",
        "food": "French Baguettes, Crepes, Seafood Medley, Kothu Parotta",
        "best_time": "October to March",
        "lat": 11.9416, "lon": 79.8083
    },

    # Hill Stations / Mountain Valleys
    "manali": {
        "terrain": "hill_station",
        "state": "Himachal Pradesh",
        "heritage": "Hadimba Temple (1553 AD wooden architecture), Naggar Castle, Manu Temple, Vashisht Hot Springs",
        "food": "Siddu with ghee, Trout fish, Babru, Chha Gosht, local apple cider",
        "best_time": "October to February for snow; March to June for pleasant weather",
        "lat": 32.2432, "lon": 77.1892
    },
    "shimla": {
        "terrain": "hill_station",
        "state": "Himachal Pradesh",
        "heritage": "Viceregal Lodge (British Colonial Era), Gaiety Theatre, Jakhu Temple, Christ Church",
        "food": "Madra, Dhaam, Thukpa, Himachali Sidu",
        "best_time": "March to June and November to February",
        "lat": 31.1048, "lon": 77.1734
    },
    "ooty": {
        "terrain": "hill_station",
        "state": "Tamil Nadu",
        "heritage": "Nilgiri Mountain Railway (UNESCO Heritage Toy Train), Toda Tribal Huts, Stone House",
        "food": "Homemade chocolates, Nilgiri Tea, Varkey pastry, South Indian Filter Coffee",
        "best_time": "October to June",
        "lat": 11.4102, "lon": 76.6950
    },
    "araku": {
        "terrain": "hill_station",
        "state": "Andhra Pradesh",
        "heritage": "Padmapuram Botanical Gardens, Tribal Museum, Borra Caves (Million-year-old stalactites)",
        "food": "Organic Araku Coffee, Bamboo Chicken, Madugula Halwa",
        "best_time": "September to February",
        "lat": 18.3273, "lon": 82.8775
    },
    "munnar": {
        "terrain": "hill_station",
        "state": "Kerala",
        "heritage": "Tea Museum & Heritage Factory, CSI Christ Church (1910 AD), Punarjani Traditional Village",
        "food": "Appam with Ishtu, Kerala Puttu, Cardamom Spiced Tea",
        "best_time": "September to March",
        "lat": 10.0889, "lon": 77.0595
    },

    # Heritage & Cultural Capitals
    "jaipur": {
        "terrain": "heritage",
        "state": "Rajasthan",
        "heritage": "Amber Fort (UNESCO), Hawa Mahal, City Palace, Jantar Mantar, Nahargarh Fort",
        "food": "Dal Baati Churma, Pyaaz Kachori, Ghevar, Laal Maas",
        "best_time": "November to February",
        "lat": 26.9124, "lon": 75.7873
    },
    "varanasi": {
        "terrain": "heritage",
        "state": "Uttar Pradesh",
        "heritage": "Kashi Vishwanath Corridor, Dashashwamedh Ghat Aarti, Sarnath Buddhist Stupa, Ramnagar Fort",
        "food": "Banarasi Paan, Kachori Jalebi, Malaiyyo, Thandai",
        "best_time": "October to March",
        "lat": 25.3176, "lon": 82.9739
    },
    "hampi": {
        "terrain": "heritage",
        "state": "Karnataka",
        "heritage": "Virupaksha Temple, Stone Chariot at Vijaya Vittala Complex (UNESCO), Lotus Mahal, Elephant Stables",
        "food": "Traditional South Indian Banana Leaf Thali, Jolada Rotti, Filter Kaapi",
        "best_time": "October to March",
        "lat": 15.3350, "lon": 76.4600
    },
    "agra": {
        "terrain": "heritage",
        "state": "Uttar Pradesh",
        "heritage": "Taj Mahal (UNESCO World Wonder), Agra Fort, Fatehpur Sikri, Mehtab Bagh",
        "food": "Agra Petha, Bedai with Aloo Sabzi, Mughlai Biryani",
        "best_time": "October to March",
        "lat": 27.1767, "lon": 78.0081
    },

    # Metropolitan & Urban Hubs
    "hyderabad": {
        "terrain": "metro",
        "state": "Telangana",
        "heritage": "Charminar (1591 AD), Golconda Fort Sound & Light, Qutb Shahi Tombs, Chowmahalla Palace",
        "food": "Hyderabadi Dum Biryani, Irani Chai with Osmania Biscuits, Double Ka Meetha, Haleem",
        "best_time": "October to March",
        "lat": 17.3850, "lon": 78.4867
    },
    "bengaluru": {
        "terrain": "metro",
        "state": "Karnataka",
        "heritage": "Bangalore Palace, Tipu Sultan's Summer Palace, Lalbagh Glass House, Bull Temple",
        "food": "Benne Masala Dosa, Filter Coffee, Mangalore Buns, Mysore Pak",
        "best_time": "Year-round pleasant climate",
        "lat": 12.9716, "lon": 77.5946
    },
    "bangalore": {
        "terrain": "metro",
        "state": "Karnataka",
        "heritage": "Bangalore Palace, Tipu Sultan's Summer Palace, Lalbagh Glass House, Bull Temple",
        "food": "Benne Masala Dosa, Filter Coffee, Mangalore Buns, Mysore Pak",
        "best_time": "Year-round pleasant climate",
        "lat": 12.9716, "lon": 77.5946
    },
    "delhi": {
        "terrain": "metro",
        "state": "Delhi NCR",
        "heritage": "Red Fort (UNESCO), Qutub Minar, Humayun's Tomb, India Gate, Jama Masjid",
        "food": "Chole Bhature, Paranthe Wali Gali parathas, Butter Chicken, Dahi Bhalla",
        "best_time": "October to March",
        "lat": 28.6139, "lon": 77.2090
    }
}

CITY_COORDINATES = {
    "hyderabad": (17.3850, 78.4867),
    "vijayawada": (16.5062, 80.6480),
    "guntur": (16.3067, 80.4365),
    "visakhapatnam": (17.6868, 83.2185),
    "vizag": (17.6868, 83.2185),
    "chennai": (13.0827, 80.2707),
    "bengaluru": (12.9716, 77.5946),
    "bangalore": (12.9716, 77.5946),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "kolkata": (22.5726, 88.3639),
    "pune": (18.5204, 73.8567),
    "goa": (15.2993, 74.1240),
    "manali": (32.2432, 77.1892),
    "jaipur": (26.9124, 75.7873),
    "ooty": (11.4102, 76.6950),
    "araku": (18.3273, 82.8775),
    "varanasi": (25.3176, 82.9739),
    "hampi": (15.3350, 76.4600),
    "agra": (27.1767, 78.0081)
}


# ============================================================================
# 3. CORE ALGORITHMIC ENGINE: MOOD × TERRAIN SEMANTIC ITINERARY GENERATOR
# ============================================================================

def classify_destination(dest_name: str) -> dict:
    clean = dest_name.lower().strip()
    if clean in DESTINATION_CATALOG:
        return DESTINATION_CATALOG[clean]
    
    if any(k in clean for k in ["beach", "sea", "island", "coast", "port", "bay"]):
        terrain = "coastal"
    elif any(k in clean for k in ["hill", "mountain", "valley", "peak", "ghat", "ridge"]):
        terrain = "hill_station"
    elif any(k in clean for k in ["fort", "palace", "temple", "monument", "heritage", "mandir"]):
        terrain = "heritage"
    else:
        terrain = "metro"
        
    return {
        "terrain": terrain,
        "state": "India",
        "heritage": f"Historic monuments, local temples, and heritage bazaars in and around {dest_name.title()}",
        "food": f"Regional specialities, popular street food, and authentic local snacks of {dest_name.title()}",
        "best_time": "October to March (Ideal touring climate)",
        "lat": 20.5937, "lon": 78.9629
    }


def generate_itinerary(mood: str, days: int, destination: str) -> list:
    dest_info = classify_destination(destination)
    terrain = dest_info["terrain"]
    dest_title = destination.strip().title() or "Your Destination"
    
    itinerary = []
    
    for d in range(1, days + 1):
        day_plan = []
        
        if d == 1:
            day_plan.append(("09:00", f"Arrive at {dest_title}, hotel check-in, unpack and freshen up"))
            day_plan.append(("11:30", f"Welcome orientation & sample traditional {dest_info['food'].split(',')[0]} at a local eatery"))
        
        if mood == "Relaxed":
            if terrain == "coastal":
                day_plan.append(("14:00", f"Leisurely seaside stroll along the calm shores of {dest_title}"))
                day_plan.append(("16:30", "Visit a beachside café, sip fresh coconut water or local beverage"))
                day_plan.append(("18:30", "Golden hour sunset photography and gentle shoreline walk"))
                day_plan.append(("20:30", f"Relaxed coastal dinner with live acoustic music"))
            elif terrain == "hill_station":
                day_plan.append(("14:00", f"Scenic valley walk through pine and cedar trails in {dest_title}"))
                day_plan.append(("16:30", "Visit a cozy local bakery or tea room with mountain viewpoints"))
                day_plan.append(("18:30", "Warm campfire / balcony sunset view overlooking the mountains"))
                day_plan.append(("20:30", f"Traditional mountain dinner featuring {dest_info['food'].split(',')[0]}"))
            elif terrain == "heritage":
                day_plan.append(("14:00", f"Peaceful courtyard walk inside {dest_info['heritage'].split(',')[0]}"))
                day_plan.append(("16:30", "Explore traditional artisan workshops and local craft bazaar"))
                day_plan.append(("18:30", "Attend the serene evening musical aarti or heritage monument illumination"))
                day_plan.append(("20:30", "Rooftop dinner overlooking illuminated historic monuments"))
            else:
                day_plan.append(("14:00", f"Relaxing stroll in {dest_title}'s premier botanical garden or lake park"))
                day_plan.append(("16:30", "Café hopping and regional sweet tasting"))
                day_plan.append(("18:30", "Lakeside promenade or scenic city skyline viewpoint"))
                day_plan.append(("20:30", f"Fine dining experience sampling authentic regional delicacies"))

        elif mood == "Adventurous":
            if terrain == "coastal":
                day_plan.append(("07:30", f"Early morning water sports: Jet ski, parasailing or scuba session"))
                day_plan.append(("12:00", "Quick hearty lunch at a local shack"))
                day_plan.append(("14:00", f"Costal cliff trek to historic fortress ruins or hidden sea caves"))
                day_plan.append(("17:30", "Beach volleyball or coastal cycling tour along rugged backwaters"))
                day_plan.append(("20:30", "Barbecue dinner with fellow travellers; rest early for next trek"))
            elif terrain == "hill_station":
                day_plan.append(("07:00", f"High-altitude nature trek along scenic mountain ridges of {dest_title}"))
                day_plan.append(("12:30", "Packed trail lunch by a natural waterfall or glacial river bank"))
                day_plan.append(("14:30", "River rafting, paragliding or mountain biking expedition"))
                day_plan.append(("18:00", "Return to base, campfire gathering and trail debrief"))
                day_plan.append(("20:30", "Hearty high-energy dinner; stargazing in clear mountain skies"))
            elif terrain == "heritage":
                day_plan.append(("07:30", f"Expedition to the outer battlements and secret tunnels of {dest_info['heritage'].split(',')[0]}"))
                day_plan.append(("12:30", "Street food challenge trying fiery local delicacies"))
                day_plan.append(("14:30", "Guided heritage scavenger walk exploring hidden architectural ruins"))
                day_plan.append(("18:00", "Sunset climb to high fort viewpoint for panoramic landscape photography"))
                day_plan.append(("20:30", "Local dhaba dining with authentic regional flavors"))
            else:
                day_plan.append(("08:00", f"Urban exploration: Heritage cycling tour across historic quarters of {dest_title}"))
                day_plan.append(("12:30", "Famous street food lane food walk"))
                day_plan.append(("14:30", "Adventure gaming / rock climbing or offbeat museum exploration"))
                day_plan.append(("18:00", "Vibrant evening night market exploration"))
                day_plan.append(("20:30", "Dinner at an iconic food institution"))

        elif mood == "Romantic":
            day_plan.append(("09:30", f"Slow morning breakfast with scenic landscape view of {dest_title}"))
            day_plan.append(("11:30", f"Private couple's tour to {dest_info['heritage'].split(',')[0]}"))
            day_plan.append(("14:00", "Intimate lunch at a scenic boutique restaurant"))
            day_plan.append(("17:00", "Private boat ride or sunset cruise with photo session"))
            day_plan.append(("20:30", "Candlelight dinner under the stars with special local desserts"))

        else: # Peaceful
            day_plan.append(("07:00", f"Morning yoga / meditation session in a quiet garden in {dest_title}"))
            day_plan.append(("09:30", "Wholesome organic breakfast and herbal tea tasting"))
            day_plan.append(("11:30", f"Quiet spiritual visit to {dest_info['heritage'].split(',')[0]}"))
            day_plan.append(("14:00", "Light vegetarian lunch and quiet reading time"))
            day_plan.append(("17:00", "Slow sunset walk beside a peaceful lake or viewpoint"))
            day_plan.append(("20:00", "Wholesome early dinner followed by restful evening"))

        if d == days and days > 1:
            day_plan.append(("16:00", f"Souvenir shopping for local handicrafts ({dest_info['food'].split(',')[-1].strip()})"))
            day_plan.append(("18:00", f"Check-out, packing, and onward departure from {dest_title}"))

        formatted_lines = [f"{t} — {act}" for t, act in day_plan]
        itinerary.append((d, formatted_lines))
        
    return itinerary


# ============================================================================
# 4. BUDGET ESTIMATOR & TRAVEL DISTANCE MODULE
# ============================================================================

def calculate_haversine_distance(source: str, dest: str) -> int:
    s_key = source.lower().strip()
    d_key = dest.lower().strip()
    
    if s_key in CITY_COORDINATES and d_key in CITY_COORDINATES:
        lat1, lon1 = CITY_COORDINATES[s_key]
        lat2, lon2 = CITY_COORDINATES[d_key]
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        road_distance = int(R * c * 1.25)
        return max(50, road_distance)
    
    return 650


def estimate_trip_budget(source: str, destination: str, mode: str, days: int) -> dict:
    distance_km = calculate_haversine_distance(source, destination)
    
    if mode == "Train":
        if distance_km <= 400:
            one_way_transport = 280
            transport_class = "Train (Sleeper Class)"
        elif distance_km <= 900:
            one_way_transport = 520
            transport_class = "Train (Sleeper / 3AC)"
        else:
            one_way_transport = 980
            transport_class = "Train (3AC Class)"
    elif mode == "Bus":
        one_way_transport = max(350, int(distance_km * 1.45))
        transport_class = "Express / Semi-Sleeper Bus"
    else:
        one_way_transport = max(3200, int(distance_km * 3.8))
        transport_class = "Domestic Economy Airfare"
        
    return_transport = one_way_transport * 2
    stay_per_night = 850
    total_stay = stay_per_night * max(1, days - 1)
    food_per_day = 450
    total_food = food_per_day * days
    local_transport = 300 * days
    
    subtotal = return_transport + total_stay + total_food + local_transport
    buffer = int(subtotal * 0.10)
    grand_total = subtotal + buffer
    
    return {
        "distance_km": distance_km,
        "transport_class": transport_class,
        "return_transport": return_transport,
        "total_stay": total_stay,
        "total_food": total_food,
        "local_transport": local_transport,
        "emergency_buffer": buffer,
        "grand_total": grand_total,
        "per_day_cost": int(grand_total / days)
    }


# ============================================================================
# 5. ROBUST IMAGE GALLERY WITH UNSPLASH & VERIFIED TRAVEL FALLBACKS
# ============================================================================

UNSPLASH_KEY = "M9iePqlVZSmJIhZUEIa7hjUA0Os-a1gEq6096S7qNI0"
UNSPLASH_HEADERS = {"Authorization": f"Client-ID {UNSPLASH_KEY}"}

CURATED_FALLBACK_IMAGES = {
    "goa": [
        "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop"
    ],
    "manali": [
        "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1593181824359-57e0569a9442?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=800&auto=format&fit=crop"
    ],
    "jaipur": [
        "https://images.unsplash.com/photo-1603288940300-474070a2fef9?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=800&auto=format&fit=crop"
    ],
    "hyderabad": [
        "https://images.unsplash.com/photo-1605379399642-870262d3d051?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1572947650440-e8a97ef053b2?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1548013146-72479768bada?w=800&auto=format&fit=crop"
    ],
    "default": [
        "https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1503220317375-aaad61436b1b?w=800&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=800&auto=format&fit=crop"
    ]
}

def fetch_destination_images(destination: str, per_page: int = 3) -> list:
    dest_clean = destination.lower().strip()
    try:
        url = "https://api.unsplash.com/search/photos"
        params = {"query": f"{destination} India tourism landmark", "per_page": per_page, "orientation": "landscape"}
        r = requests.get(url, headers=UNSPLASH_HEADERS, params=params, timeout=4)
        if r.status_code == 200:
            data = r.json()
            urls = [item["urls"]["regular"] for item in data.get("results", []) if "urls" in item]
            if len(urls) >= 2:
                return urls[:per_page]
    except Exception:
        pass
        
    if dest_clean in CURATED_FALLBACK_IMAGES:
        return CURATED_FALLBACK_IMAGES[dest_clean][:per_page]
        
    return CURATED_FALLBACK_IMAGES["default"][:per_page]


def fetch_wikipedia_heritage_summary(destination: str) -> str:
    dest_clean = destination.lower().strip()
    dest_info = classify_destination(destination)
    
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{destination.strip().title()}"
        headers = {"User-Agent": "TripGenie-Student-Project/1.0 (academic review)"}
        r = requests.get(url, headers=headers, timeout=3)
        if r.status_code == 200:
            extract = r.json().get("extract")
            if extract and len(extract) > 40:
                return extract
    except Exception:
        pass
        
    return (
        f"{destination.title()} is a celebrated cultural destination in {dest_info['state']}, renowned for its "
        f"living traditions, architecture, and scenic significance. Prominent heritage landmarks include {dest_info['heritage']}. "
        f"Travellers are encouraged to support local artisans, preserve cultural monuments, and explore authentic culinary heritage."
    )


# ============================================================================
# 6. TRIPGENIE AI CONVERSATIONAL ENGINE (NLP INTENT CLASSIFICATION)
# ============================================================================

def process_genie_query(user_query: str, active_dest: str, active_mood: str, active_days: int, active_budget: dict) -> str:
    q = user_query.lower().strip()
    dest = active_dest.strip().title() or "Your Destination"
    dest_info = classify_destination(active_dest)
    
    if any(k in q for k in ["photo", "image", "pic", "look like"]):
        return f"📸 I have loaded visual destination galleries for **{dest}** on the main dashboard! Scroll to the Destination Gallery card to inspect."

    elif any(k in q for k in ["budget", "cost", "how much", "price", "expense", "fare", "cheap"]):
        return (
            f"💰 **Estimated Budget for {dest} ({active_days} Days):**\n\n"
            f"- **Transport ({active_budget['transport_class']}):** ₹{active_budget['return_transport']:,} (Return)\n"
            f"- **Accommodation (Lodging):** ₹{active_budget['total_stay']:,} (Total)\n"
            f"- **Food & Regional Dining:** ₹{active_budget['total_food']:,}\n"
            f"- **Local Sightseeing & Auto:** ₹{active_budget['local_transport']:,}\n"
            f"- **Recommended Total:** **₹{active_budget['grand_total']:,} per person** (includes 10% emergency buffer)."
        )

    elif any(k in q for k in ["heritage", "history", "monument", "temple", "fort", "palace", "culture", "historical"]):
        return (
            f"🏛️ **Local Heritage & Cultural Landmarks in {dest}:**\n\n"
            f"- **Key Heritage Sites:** {dest_info['heritage']}\n"
            f"- **State / Region:** {dest_info['state']}\n"
            f"- **Heritage Preservation Tip:** Support local community guides and visit state archaeology sites during morning hours for fewer crowds."
        )

    elif any(k in q for k in ["food", "eat", "dish", "cuisine", "restaurant", "snack", "dinner"]):
        return (
            f"🍲 **Must-Try Local Food in {dest}:**\n\n"
            f"Don't miss authentic regional specialties: **{dest_info['food']}**.\n"
            f"💡 *Pro-tip for budget travellers:* Eat at bustling local eateries and historic market lanes rather than hotel buffets for genuine flavor at 1/3rd the cost."
        )

    elif any(k in q for k in ["best time", "weather", "season", "when to visit", "climate", "month"]):
        return (
            f"🌤️ **Best Season for {dest}:**\n\n"
            f"The ideal travel window is **{dest_info['best_time']}**.\n"
            f"This window offers comfortable daytime temperatures for outdoor sightseeing and active photography."
        )

    elif any(k in q for k in ["safe", "safety", "solo", "night", "precaution", "emergency"]):
        return (
            f"🛡️ **Safety & Solo Travel Guidelines for {dest}:**\n\n"
            f"1. Keep offline copies of your government ID and TripGenie itinerary.\n"
            f"2. Use prepaid government auto/taxi booths at railway stations.\n"
            f"3. Note down the national tourist helpline number: **1363**.\n"
            f"4. Stay in verified homestays or hostels close to central transit nodes."
        )

    elif any(k in q for k in ["itinerary", "plan", "schedule", "day 1", "day 2", "morning"]):
        return (
            f"🗺️ A personalized **{active_days}-Day ({active_mood} Mood)** plan has been dynamically generated for {dest}! "
            f"You can review each day's morning, afternoon, and evening schedule in the main workspace and click 'Download Itinerary' for offline access."
        )

    else:
        return (
            f"👋 I'm your **TripGenie AI Assistant** for **{dest}**! Ask me anything about:\n"
            f"• 💰 *'What is the estimated budget?'*\n"
            f"• 🏛️ *'Tell me about heritage monuments'*\n"
            f"• 🍲 *'What local food should I try?'*\n"
            f"• 🌤️ *'When is the best time to visit?'*"
        )


# ============================================================================
# 7. UI PRESENTATION: HERO BANNER & SEARCH INPUTS
# ============================================================================

st.markdown("""
<div class="hero-block">
  <div class="hero-badge">AI-ASSISTED TOURISM & LOCAL HERITAGE GATEWAY</div>
  <div class="hero-title">TripGenie – Smart Gateway to Your Destination</div>
  <div class="hero-subtitle">
    Personalized mood-based day-wise itineraries, transparent student travel budgets, and verified heritage discovery.
  </div>
  <div style="font-size: 13px; opacity: 0.85;">
    🌱 Community Service Project • Department of Artificial Intelligence & Data Science
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("#### 🧳 Plan Your Journey")

col1, col2, col3 = st.columns([1.2, 1.2, 1])
with col1:
    source_city = st.text_input("Origin (From)", value="Hyderabad", key="origin_input", help="Starting city or railway hub")
with col2:
    destination_city = st.text_input("Destination (To)", value="Goa", key="destination_input", help="City, hill station, or heritage town")
with col3:
    travel_mode = st.selectbox("Preferred Mode", ["Train", "Bus", "Flight"], key="mode_select")

col_a, col_b = st.columns([1.2, 1.2])
with col_a:
    travel_mood = st.selectbox(
        "Travel Mood (Personalization Parameter)",
        ["Relaxed 🏖️", "Adventurous 🧗", "Romantic 🌅", "Peaceful 🧘"],
        key="mood_select"
    )
    clean_mood = travel_mood.split()[0]
with col_b:
    trip_days = st.slider("Trip Duration (Days)", min_value=1, max_value=7, value=3, key="days_slider")

st.session_state["active_dest"] = destination_city.strip()
st.session_state["active_source"] = source_city.strip()
st.session_state["active_mood"] = clean_mood
st.session_state["active_days"] = trip_days
st.session_state["active_mode"] = travel_mode

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================================
# 8. SIDEBAR: TRIPGENIE CONVERSATIONAL ASSISTANT
# ============================================================================

if "genie_chat_history" not in st.session_state:
    st.session_state.genie_chat_history = [
        {"role": "genie", "text": "Hello! I am TripGenie, your AI travel companion. Ask me about travel budgets, heritage sites, local cuisines, or best visiting times!"}
    ]

with st.sidebar:
    st.markdown("### 🤖 TripGenie Assistant")
    st.caption(f"Context: {destination_city.title()} • {clean_mood} Mood")
    
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.genie_chat_history[-6:]:
            if msg["role"] == "genie":
                st.markdown(f"<div class='chat-genie'><b>TripGenie:</b><br>{msg['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-user'>{msg['text']}</div>", unsafe_allow_html=True)
                
    st.markdown("**Quick Prompts:**")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        if st.button("💰 Budget Tips", use_container_width=True):
            budget_data = estimate_trip_budget(source_city, destination_city, travel_mode, trip_days)
            resp = process_genie_query("estimated budget", destination_city, clean_mood, trip_days, budget_data)
            st.session_state.genie_chat_history.append({"role": "user", "text": "What is the estimated budget?"})
            st.session_state.genie_chat_history.append({"role": "genie", "text": resp})
            st.rerun()
    with col_q2:
        if st.button("🏛️ Heritage Info", use_container_width=True):
            budget_data = estimate_trip_budget(source_city, destination_city, travel_mode, trip_days)
            resp = process_genie_query("heritage monuments", destination_city, clean_mood, trip_days, budget_data)
            st.session_state.genie_chat_history.append({"role": "user", "text": "Tell me about local heritage"})
            st.session_state.genie_chat_history.append({"role": "genie", "text": resp})
            st.rerun()

    with st.form("genie_chat_form", clear_on_submit=True):
        user_query = st.text_input("Ask TripGenie...", placeholder="e.g. Best street food? Or is it safe?")
        submitted = st.form_submit_button("Send Query")
        if submitted and user_query.strip():
            budget_data = estimate_trip_budget(source_city, destination_city, travel_mode, trip_days)
            reply = process_genie_query(user_query.strip(), destination_city, clean_mood, trip_days, budget_data)
            st.session_state.genie_chat_history.append({"role": "user", "text": user_query.strip()})
            st.session_state.genie_chat_history.append({"role": "genie", "text": reply})
            st.rerun()

    st.markdown("---")
    st.caption("TripGenie v2.4 • Academic Edition • Batch B13")


# ============================================================================
# 9. MAIN CONTENT: ITINERARY, GALLERY, BUDGET & HERITAGE
# ============================================================================

budget_data = estimate_trip_budget(source_city, destination_city, travel_mode, trip_days)
dest_meta = classify_destination(destination_city)

# --- SECTION A: DESTINATION GALLERY ---
st.markdown("#### 📸 Destination Visual Discovery")
images = fetch_destination_images(destination_city, per_page=3)

img_cols = st.columns(3)
for idx, col in enumerate(img_cols):
    if idx < len(images):
        with col:
            st.image(images[idx], use_container_width=True, caption=f"{destination_city.title()} — Landmark {idx + 1}")

# --- SECTION B: BUDGET BREAKDOWN METRICS ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(f"#### 💰 Student & Budget Travel Breakdown: {source_city.title()} ➔ {destination_city.title()}")

b_col1, b_col2, b_col3, b_col4 = st.columns(4)
with b_col1:
    st.markdown(f"""
    <div class="budget-pill">
      <div class="budget-val">{budget_data['distance_km']} km</div>
      <div class="budget-lbl">Approx. Distance</div>
    </div>
    """, unsafe_allow_html=True)
with b_col2:
    st.markdown(f"""
    <div class="budget-pill">
      <div class="budget-val">₹{budget_data['return_transport']:,}</div>
      <div class="budget-lbl">Return Transport ({travel_mode})</div>
    </div>
    """, unsafe_allow_html=True)
with b_col3:
    st.markdown(f"""
    <div class="budget-pill">
      <div class="budget-val">₹{budget_data['total_stay']:,}</div>
      <div class="budget-lbl">Lodging ({trip_days - 1} Nights)</div>
    </div>
    """, unsafe_allow_html=True)
with b_col4:
    st.markdown(f"""
    <div class="budget-pill" style="border-color:#86efac; background:#f0fdf4;">
      <div class="budget-val" style="color:#15803d;">₹{budget_data['grand_total']:,}</div>
      <div class="budget-lbl" style="color:#166534;">Est. Total Per Person</div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("🔍 View Itemized Cost Calculations & Expense Split"):
    st.write(f"- **Transport ({budget_data['transport_class']}):** ₹{budget_data['return_transport']:,} return")
    st.write(f"- **Accommodation (Budget student stay @ ₹850/night):** ₹{budget_data['total_stay']:,}")
    st.write(f"- **Food & Regional Dining (@ ₹450/day):** ₹{budget_data['total_food']:,}")
    st.write(f"- **Local Commute & Entry Tickets (@ ₹300/day):** ₹{budget_data['local_transport']:,}")
    st.write(f"- **Emergency & Miscellaneous Buffer (10%):** ₹{budget_data['emergency_buffer']:,}")
    st.info("💡 **Budget Traveler Tip:** Travelling in groups of 3-4 reduces individual accommodation costs by up to 35% through room sharing.")

st.markdown('</div>', unsafe_allow_html=True)


# --- SECTION C: LOCAL HERITAGE & CULTURE AWARENESS ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(f"#### 🏛️ Local Heritage & Cultural Discovery: {destination_city.title()}")

heritage_summary = fetch_wikipedia_heritage_summary(destination_city)
st.write(heritage_summary)

h_col1, h_col2 = st.columns(2)
with h_col1:
    st.markdown(f"""
    <div class="heritage-box">
      <b>🏺 Key Heritage Monuments & Sites:</b><br>
      {dest_meta['heritage']}
    </div>
    """, unsafe_allow_html=True)
with h_col2:
    st.markdown(f"""
    <div class="heritage-box" style="background:#f0fdf4; border-color:#bbf7d0; border-left-color:#22c55e; color:#14532d;">
      <b>🍲 Culinary & Artisan Heritage:</b><br>
      {dest_meta['food']}
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --- SECTION D: PERSONALIZED DAY-WISE ITINERARY ---
st.markdown("#### 📅 Personalized Day-Wise Itinerary")
st.caption(f"Tailored for {clean_mood} Mood • Destination Terrain: {dest_meta['terrain'].replace('_', ' ').title()}")

itinerary_plan = generate_itinerary(clean_mood, trip_days, destination_city)

for day_num, activities in itinerary_plan:
    st.markdown(f"""
    <div class="day-card">
      <div class="day-header">
        <span>📍 Day {day_num}</span>
      </div>
    """, unsafe_allow_html=True)
    
    for act in activities:
        parts = act.split(" — ")
        time_slot = parts[0] if len(parts) > 1 else "Activity"
        desc = parts[1] if len(parts) > 1 else act
        st.markdown(f"""
        <div class="activity-row">
          <div class="activity-time">{time_slot}</div>
          <div>{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)


# --- SECTION E: EXPORT FOR OFFLINE TRAVEL ---
st.markdown('<div class="card" style="text-align: center;">', unsafe_allow_html=True)
st.markdown("#### 📥 Offline Travel Pass")
st.write("Download your complete day-wise travel itinerary and budget estimate for offline access during travel.")

export_lines = [
    "===========================================================",
    f" TRIPGENIE — PERSONALIZED TRAVEL ITINERARY & BUDGET PASS",
    "===========================================================",
    f" Destination: {destination_city.title()}, {dest_meta['state']}",
    f" Origin Hub:   {source_city.title()}",
    f" Trip Length:  {trip_days} Days",
    f" Travel Mood:  {clean_mood}",
    f" Travel Mode:  {travel_mode}",
    f" Generated:    {datetime.datetime.now().strftime('%d %B %Y, %I:%M %p')}",
    "-----------------------------------------------------------",
    f" APPROXIMATE DISTANCE & BUDGET ESTIMATE (PER PERSON):",
    f" Distance:            {budget_data['distance_km']} km",
    f" Return Transit:      Rs. {budget_data['return_transport']:,} ({travel_mode})",
    f" Accommodation:       Rs. {budget_data['total_stay']:,} ({trip_days - 1} Nights)",
    f" Food & Dining:       Rs. {budget_data['total_food']:,}",
    f" Sightseeing/Local:   Rs. {budget_data['local_transport']:,}",
    f" Emergency Reserve:   Rs. {budget_data['emergency_buffer']:,}",
    f" TOTAL ESTIMATE:      Rs. {budget_data['grand_total']:,} per person",
    "-----------------------------------------------------------",
    " HERITAGE & CULTURAL GUIDANCE:",
    f" Key Monuments: {dest_meta['heritage']}",
    f" Local Foods:   {dest_meta['food']}",
    "===========================================================",
    " DAY-WISE ITINERARY:",
    "==========================================================="
]

for d, acts in itinerary_plan:
    export_lines.append(f"\nDAY {d}:")
    for a in acts:
        export_lines.append(f"  * {a}")

export_lines.append("\n===========================================================")
export_lines.append(" TripGenie: Promoting Responsible Tourism & Local Heritage")
export_lines.append(" Department of AI & Data Science | Community Service Project")
export_lines.append("===========================================================")

final_export_text = "\n".join(export_lines)

st.download_button(
    label="📥 Download Travel Itinerary (TXT Pass)",
    data=final_export_text,
    file_name=f"TripGenie_Itinerary_{destination_city.title()}.txt",
    mime="text/plain",
    use_container_width=True
)
st.markdown('</div>', unsafe_allow_html=True)


# --- FOOTER ---
st.markdown("""
<div style="text-align: center; margin-top: 32px; padding: 16px; color: #64748b; font-size: 13px;">
  <b>TripGenie – Smart Gateway to Your Destination</b> • B.Tech III Year AI & Data Science (Batch B13)<br>
  Seshadri Rao Gudlavalleru Engineering College (Autonomous) • Academic Year 2026-2027
</div>
""", unsafe_allow_html=True)
