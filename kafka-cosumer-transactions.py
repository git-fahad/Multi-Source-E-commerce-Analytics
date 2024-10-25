import psycopg2
from kafka import KafkaConsumer
import json

conn = psycopg2.connect(
    host="localhost",
    database="ecommerce",
    user="your_postgres_user",
    password="your_postgres_password"
)
cursor = conn.cursor()

consumer = KafkaConsumer(
    'ecommerce-transactions-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='transaction-group',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

for message in consumer:
    transaction = message.value
    transaction_id = transaction['transaction_id']
    product_id = transaction['product_id']
    customer_id = transaction['customer_id']
    quantity = transaction['quantity']
    transaction_amount = transaction['transaction_amount']
    transaction_time = transaction['transaction_time']

    cursor.execute("""
        INSERT INTO transactions (transaction_id, product_id, customer_id, quantity, transaction_amount, transaction_time)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (transaction_id, product_id, customer_id, quantity, transaction_amount, transaction_time))

    conn.commit()
    print(f"Stored transaction ID: {transaction_id}")

cursor.close()
conn.close()
