import sqlite3
import json
import os
from typing import List, Optional, Dict, Any
from .models import UserProfile, Goal

DB_PATH = os.path.join(os.path.dirname(__file__), "finwise.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Profiles table
    c.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        id TEXT PRIMARY KEY,
        name TEXT,
        age INTEGER,
        annual_income_range TEXT,
        annual_income REAL,
        monthly_expenses_range TEXT,
        monthly_expenses REAL,
        investment_goal TEXT,
        investment_horizon TEXT,
        risk_appetite TEXT,
        existing_investments_liabilities TEXT,
        existing_savings REAL,
        total_debt REAL,
        risk_score INTEGER,
        risk_category TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Goals table
    c.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        name TEXT,
        target_amount REAL,
        current_amount REAL,
        target_months INTEGER,
        priority TEXT,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Chat audit table
    c.execute("""
    CREATE TABLE IF NOT EXISTS chat_audit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        query TEXT,
        status TEXT,
        checks_applied TEXT,
        response_summary TEXT,
        evidence TEXT
    )
    """)
    
    conn.commit()
    conn.close()
    
    # Pre-populate demo user if not present
    seed_demo_user()

def seed_demo_user():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM profiles WHERE id = 'user_default'")
    row = c.fetchone()
    if not row:
        c.execute("""
        INSERT INTO profiles (
            id, name, age, annual_income_range, annual_income,
            monthly_expenses_range, monthly_expenses, investment_goal,
            investment_horizon, risk_appetite, existing_investments_liabilities,
            existing_savings, total_debt, risk_score, risk_category
        ) VALUES (
            'user_default', 'Rupesh', 21, '₹5–10 Lakh', 600000.0,
            '₹25,000–₹50,000', 30000.0, 'Wealth Creation',
            '5–10 years', 'Moderate', 'Mutual Funds: ₹60,000, Bank FD: ₹40,000',
            100000.0, 0.0, 67, 'Moderate'
        )
        """)
        
        # Add demo goals
        c.execute("""
        INSERT INTO goals (id, user_id, name, target_amount, current_amount, target_months, priority, category)
        VALUES 
        ('g1', 'user_default', 'Wealth Creation', 1000000.0, 100000.0, 60, 'High', 'Wealth'),
        ('g2', 'user_default', 'Emergency Fund', 150000.0, 40000.0, 12, 'High', 'Safety')
        """)
        conn.commit()
    conn.close()

def save_profile(profile: UserProfile):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO profiles (
        id, name, age, annual_income_range, annual_income,
        monthly_expenses_range, monthly_expenses, investment_goal,
        investment_horizon, risk_appetite, existing_investments_liabilities,
        existing_savings, total_debt, risk_score, risk_category, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ON CONFLICT(id) DO UPDATE SET
        name=excluded.name,
        age=excluded.age,
        annual_income_range=excluded.annual_income_range,
        annual_income=excluded.annual_income,
        monthly_expenses_range=excluded.monthly_expenses_range,
        monthly_expenses=excluded.monthly_expenses,
        investment_goal=excluded.investment_goal,
        investment_horizon=excluded.investment_horizon,
        risk_appetite=excluded.risk_appetite,
        existing_investments_liabilities=excluded.existing_investments_liabilities,
        existing_savings=excluded.existing_savings,
        total_debt=excluded.total_debt,
        risk_score=excluded.risk_score,
        risk_category=excluded.risk_category,
        updated_at=CURRENT_TIMESTAMP
    """, (
        profile.id, profile.name, profile.age, profile.annual_income_range, profile.annual_income,
        profile.monthly_expenses_range, profile.monthly_expenses, profile.investment_goal,
        profile.investment_horizon, profile.risk_appetite, profile.existing_investments_liabilities,
        profile.existing_savings, profile.total_debt, profile.risk_score, profile.risk_category
    ))
    conn.commit()
    conn.close()

def load_profile(user_id: str = "user_default") -> UserProfile:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM profiles WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return UserProfile(
            id=row["id"],
            name=row["name"],
            age=row["age"],
            annual_income_range=row["annual_income_range"],
            annual_income=row["annual_income"],
            monthly_expenses_range=row["monthly_expenses_range"],
            monthly_expenses=row["monthly_expenses"],
            investment_goal=row["investment_goal"],
            investment_horizon=row["investment_horizon"],
            risk_appetite=row["risk_appetite"],
            existing_investments_liabilities=row["existing_investments_liabilities"],
            existing_savings=row["existing_savings"],
            total_debt=row["total_debt"],
            risk_score=row["risk_score"],
            risk_category=row["risk_category"]
        )
    return UserProfile()

def get_goals(user_id: str = "user_default") -> List[Goal]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM goals WHERE user_id = ?", (user_id,))
    rows = c.fetchall()
    conn.close()
    goals = []
    for r in rows:
        goals.append(Goal(
            id=r["id"],
            user_id=r["user_id"],
            name=r["name"],
            target_amount=r["target_amount"],
            current_amount=r["current_amount"],
            target_months=r["target_months"],
            priority=r["priority"],
            category=r["category"]
        ))
    return goals

def save_goal(goal: Goal):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    INSERT INTO goals (id, user_id, name, target_amount, current_amount, target_months, priority, category)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        name=excluded.name,
        target_amount=excluded.target_amount,
        current_amount=excluded.current_amount,
        target_months=excluded.target_months,
        priority=excluded.priority,
        category=excluded.category
    """, (
        goal.id, goal.user_id, goal.name, goal.target_amount,
        goal.current_amount, goal.target_months, goal.priority, goal.category
    ))
    conn.commit()
    conn.close()

def delete_goal(goal_id: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()

def reset_demo():
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM profiles")
    c.execute("DELETE FROM goals")
    c.execute("DELETE FROM chat_audit")
    conn.commit()
    conn.close()
    seed_demo_user()

# Auto-initialize database tables and seed
init_db()

