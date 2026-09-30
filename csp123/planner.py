import sqlite3
import streamlit as st
import requests
import math
import matplotlib.pyplot as plt
import pandas as pd
import random
import string

# ===================== STEP 1: DATABASE SETUP =====================
# Connect to SQLite (creates planner.db if it doesn't exist)
conn = sqlite3.connect("planner.db", check_same_thread=False)
c = conn.cursor()

# Create tables if they don’t exist
c.execute("""
CREATE TABLE IF NOT EXISTS rooms (
    code TEXT PRIMARY KEY,
    host TEXT,
    budget INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS members (
    room_code TEXT,
    name TEXT,
    UNIQUE(room_code, name),
    FOREIGN KEY(room_code) REFERENCES rooms(code)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS votes (
    room_code TEXT,
    destination TEXT,
    votes INTEGER,
    PRIMARY KEY(room_code, destination),
    FOREIGN KEY(room_code) REFERENCES rooms(code)
)
""")

conn.commit()
# Insert data into database
def add_room(code, host, budget):
    c.execute("INSERT INTO rooms VALUES (?, ?, ?)", (code, host, budget))
    conn.commit()

# Get all rooms
def get_rooms():
    c.execute("SELECT * FROM rooms")
    return c.fetchall()
# ===== STREAMLIT UI =====

st.title("AI Trip Planner")

code = st.text_input("Room Code")
host = st.text_input("Host Name")
budget = st.number_input("Budget")

if st.button("Create Room"):
    add_room(code, host, budget)
    st.success("Room Created Successfully!")

if st.button("Show Rooms"):
    rooms = get_rooms()
    st.write(rooms)

# ===================== HELPER FUNCTIONS FOR DATABASE =====================
def create_room_db(code, host, budget=12000):
    """Create a new room in the database"""
    c.execute("INSERT INTO rooms (code, host, budget) VALUES (?, ?, ?)", (code, host, budget))
    # Initialize votes
    for dest in ["Goa", "Manali", "Kerala", "Jaipur"]:
        c.execute("INSERT INTO votes (room_code, destination, votes) VALUES (?, ?, ?)", (code, dest, 0))
    # Add host as member
    c.execute("INSERT INTO members (room_code, name) VALUES (?, ?)", (code, host))
    conn.commit()

def join_room_db(code, username):
    """Add a member to a room"""
    try:
        c.execute("INSERT INTO members (room_code, name) VALUES (?, ?)", (code, username))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # member already exists

def get_room_db(code):
    """Fetch room info, members, and votes"""
    c.execute("SELECT host, budget FROM rooms WHERE code=?", (code,))
    room_info = c.fetchone()
    if not room_info: return None
    host, budget = room_info
    c.execute("SELECT name FROM members WHERE room_code=?", (code,))
    members = [row[0] for row in c.fetchall()]
    c.execute("SELECT destination, votes FROM votes WHERE room_code=?", (code,))
    votes = {row[0]: row[1] for row in c.fetchall()}
    return {"host": host, "budget": budget, "members": members, "votes": votes, "code": code}

def submit_vote_db(code, destination):
    """Increment vote for a destination"""
    c.execute("UPDATE votes SET votes = votes + 1 WHERE room_code=? AND destination=?", (code, destination))
    conn.commit()

# ===================== UTILITY FUNCTION =====================
def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
