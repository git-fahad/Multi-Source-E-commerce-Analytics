# Multi-Source E-commerce Analytics Platform with Real-Time Social Media Sentiment Analysis

This project is a multi-source analytics platform that integrates real-time e-commerce transactional data with social media sentiment analysis. By gathering transactional data and analyzing customer sentiment from Twitter, the platform provides valuable insights into how social trends correlate with sales.

## Table of Contents
1. [Overview](#overview)
2. [Tech Stack](#tech-stack)
3. [Architecture](#architecture)
4. [Setup and Installation](#setup-and-installation)
5. [Kafka Streaming and Data Ingestion](#kafka-streaming-and-data-ingestion)
6. [Data Transformation](#data-transformation)
7. [Database Setup](#database-setup)
8. [Visualization with Grafana](#visualization-with-grafana)

## Overview
The platform gathers e-commerce transactional data from a local PostgreSQL database and real-time Twitter data using the `Tweepy` library. The data is processed and integrated to provide insights into how social sentiment (e.g., positive or negative tweets about a product) correlates with sales.

## Tech Stack
- **Kafka & Zookeeper**: Data streaming and messaging queue
- **Tweepy**: API for Twitter
- **Python**: Backend programming language
- **Docker**: Containerization
- **PostgreSQL**: Database for storage
- **Grafana**: Data visualization
- **Kafka**: Python client for Kafka

## Architecture
1. **Data Ingestion**:
   - E-commerce transactions are streamed to Kafka topics.
   - Tweets are pulled in real-time from Twitter using Tweepy and sent to Kafka.

2. **Data Processing**:
   - Both transaction data and tweets are consumed from Kafka.
   - Data is processed, transformed, and stored in a PostgreSQL database.

3. **Visualization**:
   - Data from PostgreSQL is visualized using Grafana to show insights such as sales trends, sentiment correlations, and customer feedback.

## Setup and Installation

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Kafka-Python](https://kafka-python.readthedocs.io/)
- [Tweepy](https://docs.tweepy.org/)

### Installation Steps

i. **Clone the Repository**:
    ```bash
    git clone [https://github.com/your-username/ecommerce-analytics-platform.git](https://github.com/git-fahad/Multi-Source-E-commerce-Analytics)
    cd ecommerce-analytics-platform
    ```

ii. **Set Up Docker Compose**:
   Use Docker Compose to set up Kafka, Zookeeper, and PostgreSQL services. Refer to the `docker-compose.yml` file in this repository.

   ```bash
   docker-compose up -d
```

iii. **Configure Twitter API Keys**:
	•	Sign up for a free version of Twitter Developer and fetch the keys.

### Kafka Streaming and Data Ingestion
	
 i.	Starting Zookeeper and Kafka:

Kafka requires Zookeeper. The following Docker Compose services are defined in docker-compose.yml:
```
services:
  zookeeper:
    image: confluentinc/cp-zookeeper
  kafka:
    image: confluentinc/cp-kafka
```

ii. Twitter Data Producer: The Python script kafka-producer-X.py streams tweets containing a specified keyword to the Kafka tweets topic.

iii.  E-commerce Transaction Data Producer:
Another Python script kafka-consumer-transactions.py streams mock transactional data to the Kafka transactions topic.

### Data Transformation

The data transformation pipeline consumes messages from Kafka, processes them, and stores them in PostgreSQL. The transformation script data_consumer.py performs data enrichment, cleaning, and deduplication.

Run the consumer script ```kafka-consumer.py```

### Database Setup

Create two tables in postgresql to store transaction and twitter data:
```
CREATE TABLE transactions (
  transaction_id SERIAL PRIMARY KEY,
  transaction_time TIMESTAMP,
  product_id INT,
  transaction_amount DECIMAL
);
```

```
CREATE TABLE tweets (
  tweet_id SERIAL PRIMARY KEY,
  tweet_time TIMESTAMP,
  sentiment TEXT,
  tweet_text TEXT
);
```

### Visualization with Grafana

	1.	Add PostgreSQL as Data Source in grafana
	2.	Create Dashboards
