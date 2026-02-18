import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_data(num_rows):
    data = {
        'trans_date_trans_time': [datetime.now() - timedelta(days=x) for x in range(num_rows)],
        'cc_num': [random.randint(1000000000000000, 9999999999999999) for _ in range(num_rows)],
        'merchant': [f'merchant_{i}' for i in range(num_rows)],
        'category': [random.choice(['grocery_pos', 'entertainment', 'shopping_pos', 'misc_pos', 'shopping_net', 'gas_transport', 'misc_net', 'grocery_net', 'food_dining', 'health_fitness', 'kids_pets', 'home', 'personal_care', 'travel']) for _ in range(num_rows)],
        'amt': [random.uniform(1.0, 1000.0) for _ in range(num_rows)],
        'first': [f'first_{i}' for i in range(num_rows)],
        'last': [f'last_{i}' for i in range(num_rows)],
        'gender': [random.choice(['M', 'F']) for _ in range(num_rows)],
        'street': [f'street_{i}' for i in range(num_rows)],
        'city': [f'city_{i}' for i in range(num_rows)],
        'state': [random.choice(['NY', 'CA', 'TX', 'FL', 'IL']) for _ in range(num_rows)],
        'zip': [random.randint(10000, 99999) for _ in range(num_rows)],
        'lat': [random.uniform(30.0, 45.0) for _ in range(num_rows)],
        'long': [random.uniform(-120.0, -70.0) for _ in range(num_rows)],
        'city_pop': [random.randint(1000, 1000000) for _ in range(num_rows)],
        'job': [random.choice(['Engineer', 'Doctor', 'Teacher', 'Artist', 'Manager']) for _ in range(num_rows)],
        'dob': [datetime(1980, 1, 1) + timedelta(days=random.randint(0, 10000)) for _ in range(num_rows)],
        'trans_num': [f'trans_{i}' for i in range(num_rows)],
        'unix_time': [int(datetime.now().timestamp()) for _ in range(num_rows)],
        'merch_lat': [random.uniform(30.0, 45.0) for _ in range(num_rows)],
        'merch_long': [random.uniform(-120.0, -70.0) for _ in range(num_rows)],
        'is_fraud': [random.choice([0, 1]) for _ in range(num_rows)]
    }
    return pd.DataFrame(data)

print("Generating dummy train data...")
train_data = generate_data(1000)
train_data.to_csv('train_data.csv', index=False)

print("Generating dummy test data...")
test_data = generate_data(200)
test_data.to_csv('test_data.csv', index=False)

print("Dummy data generated successfully.")
