"""
Normalization Layer Module

This module combines all environmental data into a unified output schema.
"""

from datetime import datetime
from typing import Optional, Dict, Any


def normalize_environmental_data(
    location: Optional[Dict[str, float]],
    weather: Optional[Dict[str, Any]],
    soil: Optional[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Combine all environmental data into the unified output schema.
    
    This is the normalization layer that ensures consistent output format
    regardless of which APIs were successful.
    
    Args:
        location: GPS location data
        weather: Processed weather data
        soil: Processed soil data
        
    Returns:
        Dict: Normalized environmental context with all required fields
    """
    # Build the normalized output structure using .get() for safe key access
    normalized = {
        "location": {
            "latitude": location.get("latitude") if location else None,
            "longitude": location.get("longitude") if location else None
        },
        "weather": {
            "temperature_c": weather.get("temperature_c") if weather else None,
            "humidity": weather.get("humidity") if weather else None,
            "rainfall_mm": weather.get("rainfall_mm") if weather else None,
            "weather_alert": weather.get("weather_alert") if weather else None
        },
        "soil": {
            "soil_type": soil.get("soil_type") if soil else None,
            "soil_ph": soil.get("soil_ph") if soil else None,
            "soil_moisture": soil.get("soil_moisture") if soil else None
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return normalized

