**WEATHER DASHBOARD**
# Project Overview

The Weather Dashboard is a Python application that fetches weather data for specified cities using the OpenWeather API and stores the data in an AWS S3 bucket. It supports dynamic city input (manually listing the cities you want to check their weather condidtions), ensures proper environment variable handling, and logs errors for easy debugging.

# Project Structure

weather-dashboard/

  src/
  
    __init__.py
    
    weather_dashboard.py
    
  tests/
  
  data/
  
  .env
  .gitignore
  requirements.txt

**Prerequisites**

Before running this project, ensure you have the following:

1. Python
Version 3.7 or higher is required.
Confirm you have python and pip installed already by running this command:
`python3 --version`
`pip --version`

If you don't, follow the installation guide on [python official page](https://www.python.org/downloads/) 

2. AWS Credentials
   
You'll need your Access Key, Secret Key, default region, and output format.
If you dont already have an AWS account you can create a free tier account using this [link](https://signin.aws.amazon.com/signup?request_type=register).
After your registration, logon and create a unique user
Create an access key for this user
Initialize your AWS Cli using this command: 

`aws configure`

3. OPENWEATHER API KEY
   
Sign up at [OpenWeather](https://openweathermap.org/).

Generate an API key from your OpenWeather dashboard.

4. Configure environment variables (.env):
   
OPENWEATHER_API_KEY=your_api_key
AWS_BUCKET_NAME=your_bucket_name

**Run the weather application**

python3 src/weather_dashboard.py


*******

Sample of Expected Result:

Fetching weather for Abuja...

Temperature: 93.74°F

Feels like: 89.13°F

Humidity: 11%

Conditions: broken clouds

Successfully saved data for Abuja to S3.

Weather data for Abuja saved to S3!

