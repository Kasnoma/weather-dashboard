import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    filename='weather_dashboard.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.s3_client = boto3.client('s3', region_name=self.region)

        # Check environment variables
        self._check_env_vars()

    def _check_env_vars(self):
        """Ensure required environment variables are loaded."""
        missing_vars = []
        if not self.api_key:
            missing_vars.append("OPENWEATHER_API_KEY")
        if not self.bucket_name:
            missing_vars.append("AWS_BUCKET_NAME")
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist, with region support."""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' already exists.")
        except self.s3_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print(f"Bucket '{self.bucket_name}' does not exist. Creating it...")
                try:
                    if self.region == "us-east-1":
                        self.s3_client.create_bucket(Bucket=self.bucket_name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=self.bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': self.region}
                        )
                    print(f"Successfully created bucket '{self.bucket_name}'.")
                except Exception as create_error:
                    logging.error(f"Error creating bucket: {create_error}")
                    raise
            else:
                logging.error(f"Error checking bucket existence: {e}")
                raise

    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API."""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "imperial"
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching weather data for {city}: {e}")
            return None

    def save_to_s3(self, weather_data, city):
        """Save weather data to S3 bucket."""
        if not weather_data:
            return False

        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.json"

        try:
            weather_data['timestamp'] = timestamp
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(weather_data),
                ContentType='application/json'
            )
            print(f"Successfully saved data for {city} to S3.")
            return True
        except Exception as e:
            logging.error(f"Error saving data to S3 for {city}: {e}")
            return False

def main():
    try:
        dashboard = WeatherDashboard()
        
        # Create bucket if needed
        dashboard.create_bucket_if_not_exists()
        
        # Allow users to input cities
        cities_input = input("Enter city names separated by commas (e.g., New York, Texas, Lagos): ")
        cities = [city.strip() for city in cities_input.split(",")]

        for city in cities:
            print(f"\nFetching weather for {city}...")
            weather_data = dashboard.fetch_weather(city)
            if weather_data:
                temp = weather_data['main']['temp']
                feels_like = weather_data['main']['feels_like']
                humidity = weather_data['main']['humidity']
                description = weather_data['weather'][0]['description']
                
                print(f"Temperature: {temp}°F")
                print(f"Feels like: {feels_like}°F")
                print(f"Humidity: {humidity}%")
                print(f"Conditions: {description}")
                
                # Save to S3
                success = dashboard.save_to_s3(weather_data, city)
                if success:
                    print(f"Weather data for {city} saved to S3!")
            else:
                print(f"Failed to fetch weather data for {city}")
    except Exception as e:
        logging.error(f"Unexpected error in main(): {e}")
        print("An unexpected error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main()
