"""
Integration Layer: Member 4 (Prompts) ↔ Member 3 (Environment Tools)

This module bridges Member 4's Pydantic data models with Member 3's
environmental data fetching. Ensures type safety and data contract compliance.
"""

from typing import Optional
from environment_data.wrapper import get_environmental_context
from src.agents.state import WeatherData, SoilData


def fetch_and_validate_environment_data(latitude: float, longitude: float) -> dict:
    """
    Fetch environmental data from Member 3's tools and convert to Member 4's models.
    
    This function:
    1. Calls Member 3's get_environmental_context()
    2. Extracts weather and soil data
    3. Validates against Pydantic models (WeatherData, SoilData)
    4. Returns typed data ready for Member 4's chains
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
        
    Returns:
        dict with keys:
            - weather_data: WeatherData model instance
            - soil_data: SoilData model instance
            - raw_response: Original response from Member 3
    """
    try:
        # Get environmental context from Member 3
        raw_env_data = get_environmental_context()
        
        # Extract weather data and validate against WeatherData model
        weather_dict = raw_env_data.get("weather", {})
        weather_data = WeatherData(
            temperature_c=weather_dict.get("temperature_c"),
            humidity=weather_dict.get("humidity", 0),
            rainfall_mm=weather_dict.get("rainfall_mm"),
            weather_alert=weather_dict.get("weather_alert")
        )
        
        # Extract soil data and validate against SoilData model
        soil_dict = raw_env_data.get("soil", {})
        soil_data = SoilData(
            soil_type=soil_dict.get("soil_type"),
            soil_ph=soil_dict.get("soil_ph"),
            soil_moisture=soil_dict.get("soil_moisture"),
            nitrogen=None,  # Not provided by Member 3 yet
            phosphorus=None,
            potassium=None
        )
        
        return {
            "weather_data": weather_data,
            "soil_data": soil_data,
            "raw_response": raw_env_data
        }
        
    except Exception as e:
        print(f"Error in fetch_and_validate_environment_data: {str(e)}")
        # Return default/empty data rather than failing
        return {
            "weather_data": WeatherData(
                temperature_c=None,
                humidity=0,
                rainfall_mm=None,
                weather_alert=None
            ),
            "soil_data": SoilData(
                soil_type=None,
                soil_ph=None,
                soil_moisture=None
            ),
            "raw_response": None
        }


def format_environment_for_prompt(weather_data: WeatherData, soil_data: SoilData) -> dict:
    """
    Format Member 3's data into variables for Member 4's prompt templates.
    
    This function converts Pydantic models into the exact variable names
    expected by ADVICE_GENERATION_SYSTEM_PROMPT and other prompts.
    
    Args:
        weather_data: WeatherData model from Member 3
        soil_data: SoilData model from Member 3
        
    Returns:
        dict with keys matching prompt template variables:
            - temperature_c
            - humidity
            - rainfall_mm
            - weather_alert
            - soil_ph
            - soil_moisture
            - soil_type
    """
    return {
        # Weather variables (from Member 3 → WeatherData)
        "temperature_c": weather_data.temperature_c or "Unknown",
        "humidity": weather_data.humidity or "Unknown",
        "rainfall_mm": weather_data.rainfall_mm or 0,
        "weather_alert": weather_data.weather_alert or "None",
        
        # Soil variables (from Member 3 → SoilData)
        "soil_ph": soil_data.soil_ph or "Unknown",
        "soil_moisture": soil_data.soil_moisture or "Unknown",
        "soil_type": soil_data.soil_type or "Unknown",
    }
