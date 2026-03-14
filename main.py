import sqlite3
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import datetime

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; specify origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "ilakku.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create subscribers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT,
            email TEXT NOT NULL,
            country_code TEXT,
            phone TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create donations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT NOT NULL,
            email TEXT NOT NULL,
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'INR',
            payment_method TEXT,
            transaction_id TEXT,
            status TEXT DEFAULT 'pending',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create volunteers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            address TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create interns table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            contact_person TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            social_links TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

class SubscriptionRequest(BaseModel):
    firstName: str
    lastName: Optional[str] = None
    email: str
    country_code: Optional[str] = None
    phone: Optional[str] = None

class DonationRequest(BaseModel):
    name: str
    email: str
    amount: float
    payment_method: Optional[str] = None

class VolunteerRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class InternRequest(BaseModel):
    company: Optional[str] = None
    contact_person: str
    email: str
    phone: str
    social_links: Optional[str] = None

@app.post("/api/subscribe")
async def subscribe(
    firstName: str = Form(...),
    lastName: str = Form(None),
    email: str = Form(...),
    country_code: str = Form(None),
    phone: str = Form(None)
):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO subscribers (first_name, last_name, email, country_code, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (firstName, lastName, email, country_code, phone))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Subscribed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/donate")
async def donate(request: DonationRequest):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO donations (donor_name, email, amount)
            VALUES (?, ?, ?)
        ''', (request.name, request.email, request.amount))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Donation record created", "amount": request.amount}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/volunteer")
async def volunteer(request: VolunteerRequest):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO volunteers (first_name, last_name, email, phone, address)
            VALUES (?, ?, ?, ?, ?)
        ''', (request.first_name, request.last_name, request.email, request.phone, request.address))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Volunteer application submitted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/intern")
async def intern(request: InternRequest):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO interns (company, contact_person, email, phone, social_links)
            VALUES (?, ?, ?, ?, ?)
        ''', (request.company, request.contact_person, request.email, request.phone, request.social_links))
        conn.commit()
        conn.close()
        return {"status": "success", "message": "Internship application submitted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {"message": "Ilakku NGO API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
