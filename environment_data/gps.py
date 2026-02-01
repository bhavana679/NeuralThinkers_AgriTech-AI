from typing import Optional, Dict

def get_gps_location() -> Optional[Dict[str, float]]:
    try:
        from streamlit_js_eval import get_geolocation
        import requests
        
        geo_data = get_geolocation()
        
        if geo_data:
             coords = geo_data.get('coords')
             if coords:
                 latitude = coords.get('latitude')
                 longitude = coords.get('longitude')
                 if latitude and longitude:
                     return {"latitude": float(latitude), "longitude": float(longitude)}
        
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                lat = data.get('latitude')
                lon = data.get('longitude')
                if lat is not None and lon is not None:
                    return {
                        "latitude": float(lat),
                        "longitude": float(lon)
                    }
        except Exception as e:
            print(f"IP Geolocation failed: {e}")

        return {
            "latitude": 28.6139,
            "longitude": 77.2090
        }
        
    except ImportError:
        return {"latitude": 28.6139, "longitude": 77.2090}
    except Exception as e:
        return {"latitude": 28.6139, "longitude": 77.2090}
