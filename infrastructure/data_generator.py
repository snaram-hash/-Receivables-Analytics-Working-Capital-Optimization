import sqlite3
import random
from datetime import datetime, timedelta
import os

def generate_data():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'receivables_analytics.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Create Tables
    cursor.execute('''
    CREATE TABLE Contractor_Master (
        contractor_id TEXT PRIMARY KEY,
        contractor_name TEXT,
        industry TEXT,
        region TEXT,
        credit_limit REAL,
        payment_terms INTEGER,
        risk_segment TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE Invoice_Table (
        invoice_id TEXT PRIMARY KEY,
        contractor_id TEXT,
        invoice_date DATE,
        due_date DATE,
        invoice_amount REAL,
        status TEXT,
        FOREIGN KEY(contractor_id) REFERENCES Contractor_Master(contractor_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE Payment_Table (
        payment_id TEXT PRIMARY KEY,
        invoice_id TEXT,
        payment_date DATE,
        amount_paid REAL,
        payment_method TEXT,
        FOREIGN KEY(invoice_id) REFERENCES Invoice_Table(invoice_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE Collection_Activity (
        activity_id TEXT PRIMARY KEY,
        invoice_id TEXT,
        activity_date DATE,
        activity_type TEXT,
        outcome TEXT,
        FOREIGN KEY(invoice_id) REFERENCES Invoice_Table(invoice_id)
    )
    ''')
    
    # 2. Seed Contractors (34 Contractors)
    industries = ['Manufacturing', 'Logistics', 'Warehousing', 'Commercial Facilities', 'Infrastructure']
    regions = ['North', 'South', 'East', 'West']
    
    contractors = []
    # Identify the "bad actors" - Top 20% (7 contractors) causing 80% delays
    bad_actors = set(random.sample(range(1, 35), 7))
    
    for i in range(1, 35):
        contractor_id = f'CONT-{i:03d}'
        name = f"Enterprise Client {i}"
        industry = random.choice(industries)
        region = random.choice(regions)
        
        if i in bad_actors:
            credit_limit = random.randint(500, 1500) * 1000 # Higher credit limits to cause 80% impact
            payment_terms = random.choice([60, 90])
            risk = "High"
        else:
            credit_limit = random.randint(50, 300) * 1000
            payment_terms = random.choice([15, 30, 45])
            risk = "Low" if random.random() > 0.3 else "Medium"
            
        contractors.append((contractor_id, name, industry, region, credit_limit, payment_terms, risk))
        
    cursor.executemany('INSERT INTO Contractor_Master VALUES (?,?,?,?,?,?,?)', contractors)
    
    # 3. Generate Invoices & Payments (24 Months)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2 * 365) # Approx 24 months
    
    invoices = []
    payments = []
    activities = []
    
    inv_counter = 1
    pay_counter = 1
    act_counter = 1
    
    current_date = start_date
    while current_date <= end_date:
        # Every month, generate invoices for most active clients
        for cont in contractors:
            if random.random() > 0.1: # 90% chance of an invoice this month
                c_id, name, ind, reg, climit, terms, risk = cont
                
                invoice_id = f'INV-{inv_counter:05d}'
                inv_date = current_date + timedelta(days=random.randint(1, 28))
                due_date = inv_date + timedelta(days=terms)
                
                # Invoice amount depends on client size/risk
                if risk == "High":
                    amount = random.uniform(80000, 250000)
                else:
                    amount = random.uniform(10000, 50000)
                    
                amount = round(amount, 2)
                
                # Determine Payment Behavior
                is_paid = False
                pay_date = None
                
                if risk == "High":
                    # Bad actors pay very late or don't pay recent ones
                    delay_days = random.randint(45, 120)
                    pay_date = due_date + timedelta(days=delay_days)
                elif risk == "Medium":
                    delay_days = random.randint(-5, 30)
                    pay_date = due_date + timedelta(days=delay_days)
                else:
                    delay_days = random.randint(-10, 5)
                    pay_date = due_date + timedelta(days=delay_days)
                    
                status = "Open"
                if pay_date <= end_date:
                    status = "Paid"
                    is_paid = True
                    
                invoices.append((invoice_id, c_id, inv_date.strftime("%Y-%m-%d"), due_date.strftime("%Y-%m-%d"), amount, status))
                
                if is_paid:
                    payments.append((f'PAY-{pay_counter:05d}', invoice_id, pay_date.strftime("%Y-%m-%d"), amount, random.choice(['Wire Transfer', 'ACH', 'Check'])))
                    pay_counter += 1
                
                # Generate Collection Activity for overdue invoices
                if pay_date and pay_date > due_date + timedelta(days=15):
                    # Activity 1: Email
                    act_date = due_date + timedelta(days=10)
                    if act_date <= end_date:
                        activities.append((f'ACT-{act_counter:05d}', invoice_id, act_date.strftime("%Y-%m-%d"), 'Email', 'No Response'))
                        act_counter += 1
                        
                    # Activity 2: Call
                    act_date = due_date + timedelta(days=30)
                    if act_date <= end_date:
                        activities.append((f'ACT-{act_counter:05d}', invoice_id, act_date.strftime("%Y-%m-%d"), 'Phone Call', 'Promised to Pay'))
                        act_counter += 1
                
                inv_counter += 1
                
        # Move to next month
        current_date += timedelta(days=30)
        
    cursor.executemany('INSERT INTO Invoice_Table VALUES (?,?,?,?,?,?)', invoices)
    cursor.executemany('INSERT INTO Payment_Table VALUES (?,?,?,?,?)', payments)
    cursor.executemany('INSERT INTO Collection_Activity VALUES (?,?,?,?,?)', activities)
    
    conn.commit()
    conn.close()
    print(f"Successfully generated {len(contractors)} contractors, {len(invoices)} invoices, {len(payments)} payments, and {len(activities)} activities.")
    print(f"Database saved to {db_path}")

if __name__ == "__main__":
    generate_data()
