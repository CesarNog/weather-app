
# Weather App with FastAPI
This Weather App is a simple FastAPI application that provides real-time weather information for Lisbon, Portugal. It uses the WeatherAPI to fetch current weather data, focusing on temperature and rain predictions for the next three days.

## Features
- Get the predicted temperature in Lisbon for the next three days.
- Check if it will rain in Lisbon in the next three days.

## Live API Endpoints
The application is hosted and can be accessed at the following live endpoints:
- Temperature Forecast: [https://weather-app-rzdp.onrender.com/temperature](https://weather-app-rzdp.onrender.com/temperature)
- Rain Forecast: [https://weather-app-rzdp.onrender.com/rain](https://weather-app-rzdp.onrender.com/rain)

## API Documentation
Explore the API documentation using the Swagger UI:
- [Swagger UI Documentation](https://weather-app-rzdp.onrender.com/docs)

## Setup

### Requirements
- Python 3.8+
- An API key from [WeatherAPI](https://www.weatherapi.com/)

### Installation
1. Clone the repository:

   ```
   git clone https://your-repository-url/weather-app.git
   cd weather-app
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your WeatherAPI API key:
   Create a `.env` file in the root directory and add your API key like this:

   ```
   WEATHER_API_KEY=your_api_key_here
   ```

## Running the Application
1. Start the FastAPI server:

   ```
   uvicorn app.main:app --reload
   ```

   The `--reload` flag enables auto-reload so the server will restart after code changes. This is useful for development, but should be removed in a production environment.

2. Access the application:
   Open your web browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000). You will see the FastAPI automatic documentation where you can test the endpoints.

## Endpoints
- `GET /temperature`: Returns the predicted temperature in Lisbon for the next three days. The temperature can be returned in either Celsius or Fahrenheit, based on the provided query parameter.
- `GET /rain`: Indicates whether it will rain in Lisbon in the next three days with a descriptive message.

## Running Tests

```
export PYTHONPATH=$PYTHONPATH:/path/to/weather_app_project
```

To run the tests, ensure you are in the project's root directory and execute:

```
pytest
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request.

## License
This project is open-source and available under the MIT License.
