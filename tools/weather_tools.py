def get_soil_data(location):
    """
    Fetch comprehensive soil data for a given location with detailed analysis.
    Args:
        location (str): Location for soil data
    Returns:
        dict: Comprehensive soil information including moisture, pH, nutrients, etc.
    """
    # Mock comprehensive soil data based on different regions
    soil_database = {
        "Punjab": {
            "location": "Punjab",
            "moisture": 45.2,
            "ph": 7.2,
            "nitrogen": "Medium",
            "phosphorus": "High",
            "potassium": "Medium",
            "organic_matter": 2.8,
            "soil_type": "Alluvial",
            "texture": "Loamy",
            "drainage": "Good",
            "salinity": "Low",
            "temperature": 18.5,
            "conductivity": 0.8,
            "carbon_content": 1.4
        },
        "Karnataka": {
            "location": "Karnataka",
            "moisture": 38.7,
            "ph": 6.8,
            "nitrogen": "Medium",
            "phosphorus": "High",
            "potassium": "Low",
            "organic_matter": 3.2,
            "soil_type": "Red Laterite",
            "texture": "Clay Loam",
            "drainage": "Moderate",
            "salinity": "Very Low",
            "temperature": 22.3,
            "conductivity": 0.6,
            "carbon_content": 1.8
        },
        "Maharashtra": {
            "location": "Maharashtra",
            "moisture": 42.1,
            "ph": 7.5,
            "nitrogen": "Low",
            "phosphorus": "Medium",
            "potassium": "High",
            "organic_matter": 2.5,
            "soil_type": "Black Cotton",
            "texture": "Clay",
            "drainage": "Poor",
            "salinity": "Medium",
            "temperature": 25.1,
            "conductivity": 1.2,
            "carbon_content": 1.2
        },
        "West Bengal": {
            "location": "West Bengal",
            "moisture": 52.3,
            "ph": 6.2,
            "nitrogen": "High",
            "phosphorus": "Medium",
            "potassium": "Medium",
            "organic_matter": 4.1,
            "soil_type": "Alluvial",
            "texture": "Silty Clay",
            "drainage": "Good",
            "salinity": "Low",
            "temperature": 26.8,
            "conductivity": 0.7,
            "carbon_content": 2.3
        }
    }
    
    # Return location-specific data or default data
    if location in soil_database:
        soil_data = soil_database[location]
    else:
        # Default soil data for unknown locations
        soil_data = {
            "location": location,
            "moisture": 40.0,
            "ph": 6.8,
            "nitrogen": "Medium",
            "phosphorus": "Medium",
            "potassium": "Medium",
            "organic_matter": 3.0,
            "soil_type": "Mixed",
            "texture": "Loamy",
            "drainage": "Moderate",
            "salinity": "Low",
            "temperature": 20.0,
            "conductivity": 0.8,
            "carbon_content": 1.5
        }
    
    # Add analysis and recommendations
    soil_data.update({
        "analysis": {
            "fertility_status": "Good" if soil_data["organic_matter"] > 3.0 else "Moderate",
            "water_retention": "High" if soil_data["moisture"] > 45 else "Medium",
            "ph_status": "Optimal" if 6.5 <= soil_data["ph"] <= 7.5 else "Needs adjustment",
            "nutrient_balance": "Balanced" if all(n != "Low" for n in [soil_data["nitrogen"], soil_data["phosphorus"], soil_data["potassium"]]) else "Requires supplementation"
        },
        "recommendations": [
            f"Maintain moisture level around {soil_data['moisture']}%",
            "Add organic compost to improve soil structure" if soil_data["organic_matter"] < 3.0 else "Organic matter levels are good",
            "Apply lime to increase pH" if soil_data["ph"] < 6.5 else "Apply sulfur to decrease pH" if soil_data["ph"] > 7.5 else "pH levels are optimal",
            f"Supplement {soil_data['nitrogen']} nitrogen" if soil_data["nitrogen"] == "Low" else f"Nitrogen levels are {soil_data['nitrogen'].lower()}",
            f"Add phosphorus fertilizer" if soil_data["phosphorus"] == "Low" else f"Phosphorus levels are {soil_data['phosphorus'].lower()}",
            f"Apply potash fertilizer" if soil_data["potassium"] == "Low" else f"Potassium levels are {soil_data['potassium'].lower()}"
        ],
        "suitable_crops": [
            "Wheat", "Rice", "Cotton", "Sugarcane" if soil_data["moisture"] > 45 else "Millet",
            "Vegetables" if soil_data["ph"] > 6.0 else "Acidic crops",
            "Pulses" if soil_data["nitrogen"] != "High" else "Leafy vegetables"
        ]
    })
    
    return soil_data

def get_weather_forecast(location, days=7):
    """
    Get weather forecast for agricultural planning.
    Args:
        location (str): Location for weather forecast
        days (int): Number of days for forecast
    Returns:
        dict: Weather forecast data
    """
    import random
    from datetime import datetime, timedelta
    
    # Mock weather forecast
    forecast = []
    base_temp = 25
    for i in range(days):
        date = datetime.now() + timedelta(days=i)
        temp_variation = random.uniform(-5, 5)
        rainfall_chance = random.uniform(0, 100)
        
        day_forecast = {
            "date": date.strftime("%Y-%m-%d"),
            "temperature": {
                "min": round(base_temp + temp_variation - 3, 1),
                "max": round(base_temp + temp_variation + 5, 1),
                "avg": round(base_temp + temp_variation, 1)
            },
            "humidity": random.randint(40, 80),
            "rainfall": round(random.uniform(0, 25) if rainfall_chance > 60 else 0, 1),
            "wind_speed": round(random.uniform(5, 20), 1),
            "condition": random.choice(["sunny", "cloudy", "rainy", "partly_cloudy"]),
            "agricultural_advisory": []
        }
        
        # Add agricultural advisories based on conditions
        if day_forecast["rainfall"] > 10:
            day_forecast["agricultural_advisory"].append("Avoid field operations due to rain")
            day_forecast["agricultural_advisory"].append("Good for transplanting rice")
        elif day_forecast["temperature"]["max"] > 35:
            day_forecast["agricultural_advisory"].append("Ensure adequate irrigation")
            day_forecast["agricultural_advisory"].append("Avoid midday field work")
        elif day_forecast["humidity"] > 70:
            day_forecast["agricultural_advisory"].append("Monitor for fungal diseases")
            day_forecast["agricultural_advisory"].append("Ensure good air circulation")
        
        if not day_forecast["agricultural_advisory"]:
            day_forecast["agricultural_advisory"].append("Good conditions for most farm activities")
        
        forecast.append(day_forecast)
    
    return {
        "location": location,
        "forecast_days": days,
        "forecast": forecast,
        "summary": {
            "avg_temperature": round(sum(d["temperature"]["avg"] for d in forecast) / len(forecast), 1),
            "total_rainfall": round(sum(d["rainfall"] for d in forecast), 1),
            "rainy_days": len([d for d in forecast if d["rainfall"] > 0]),
            "avg_humidity": round(sum(d["humidity"] for d in forecast) / len(forecast), 1)
        },
        "agricultural_recommendations": [
            "Plan irrigation based on rainfall predictions",
            "Monitor temperature for crop stress",
            "Prepare for pest/disease management in humid conditions"
        ]
    }