import snowflake.connector
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# Snowflake Connection
# =========================

conn = snowflake.connector.connect(
    user='DEVAPRIYA',
    password='Devapriya@4354',
    account='DK09684',
    warehouse='COMPUTE_WH',
    database='OPENWEATHER',
    schema='WEATHERSCHEMA'
)

# =========================
# Read Data
# =========================

query = """
SELECT
    COUNTRY,
    CITY,
    HUMIDITY,
    TEMPERATURE,
    TIME
FROM WEATHER_DATA
"""

df = pd.read_sql(query, conn)

conn.close()

# Convert TIME column
df['TIME'] = pd.to_datetime(df['TIME'])

print(df.head())

# =========================
# Chart 1
# Temperature by City
# =========================

plt.figure(figsize=(10,5))
plt.bar(df['CITY'], df['TEMPERATURE'])

plt.title('Temperature by City'
plt.xlabel('City')
plt.ylabel('Temperature (°C)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# =========================
# Chart 2
# Humidity by City
# =========================

plt.figure(figsize=(10,5))
plt.bar(df['CITY'], df['HUMIDITY'])

plt.title('Humidity by City')
plt.xlabel('City')
plt.ylabel('Humidity (%)')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# =========================
# Chart 3
# Temperature Trend
# =========================

plt.figure(figsize=(12,5))
plt.plot(df['TIME'], df['TEMPERATURE'])

plt.title('Temperature Trend Over Time')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')

plt.grid(True)
plt.tight_layout()
plt.show()

# =========================
# Chart 4
# Humidity vs Temperature
# =========================

plt.figure(figsize=(8,5))
plt.scatter(df['TEMPERATURE'], df['HUMIDITY'])

plt.title('Humidity vs Temperature')
plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')

plt.tight_layout()
plt.show()

# =========================
# Chart 5
# Average Temperature by Country
# =========================

avg_temp = df.groupby('COUNTRY')['TEMPERATURE'].mean()

plt.figure(figsize=(10,5))
avg_temp.plot(kind='bar')

plt.title('Average Temperature by Country')
plt.xlabel('Country')
plt.ylabel('Average Temperature (°C)')

plt.tight_layout()
plt.show()