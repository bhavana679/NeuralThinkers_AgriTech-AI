import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env

from typing import TypedDict, Annotated, Optional, List, Literal
from pydantic import BaseModel, Field, field_validator, model_validator

class FarmerInput(BaseModel):
    soil_type: Literal['loamy', 'clay', 'sandy', 'silty', 'peaty', 'chalky', 'unknown']
    crop: Annotated[str, Field(min_length=2)]
    reported_action: Annotated[str, Field(min_length=5)]   #Description of the issue or action taken
    location: Annotated[str, Field(min_length=2)]
    
class ExtractedKeywords(BaseModel):
    pests: Annotated[List[str], Field(default=[])]
    symptoms: Annotated[List[str], Field(default=[])]
    urgency: Literal['low', 'medium', 'high', 'critical'] = 'medium'
    
    @field_validator('pests', 'symptoms', mode='before')
    @classmethod
    def normalize_lists(cls, v):
        """Ensure pests and symptoms are lists of non-empty strings."""
        if isinstance(v, str):
            v = [v]
        if not isinstance(v, list):
            v = list(v) if hasattr(v, '__iter__') else [v]
        v = [item.strip().lower() for item in v if isinstance(item, str) and item.strip()]
        return v

    @model_validator(mode='after')
    def check_keywords_not_empty(self):
        """Warn if no keywords were extracted, but don't fail."""
        if not self.pests and not self.symptoms:
            pass
        return self


class ExtractionModel(BaseModel):
    crop: str
    symptoms: List[str] = Field(default=[])
    pests: List[str] = Field(default=[])
    action_taken: str = ""
    urgency: Literal['low', 'medium', 'high', 'critical'] = 'medium'
    primary_category: Literal['pest', 'disease', 'nutrient', 'irrigation', 'weather'] = 'pest'
class ValidationResult(BaseModel):
    is_valid: bool
    error_message: str = ""
    warnings: Annotated[List[str], Field(default=[])]
    
    @model_validator(mode='after')
    def validate_consistency(self):
        """Ensure is_valid and error_message are consistent."""
        if self.is_valid and self.error_message:
            raise ValueError(
                "is_valid=True but error_message is non-empty"
            )
        if not self.is_valid and not self.error_message:
            raise ValueError(
                "is_valid=False but error_message is empty"
            )
        return self
class SoilData(BaseModel):
    soil_type: Optional[str] = None
    soil_ph: Annotated[Optional[float], Field(ge=0, le=14)] = None
    soil_moisture: Annotated[Optional[float], Field(ge=0, le=100)] = None
    nitrogen: Annotated[Optional[float], Field(ge=0)] = None
    phosphorus: Annotated[Optional[float], Field(ge=0)] = None
    potassium: Annotated[Optional[float], Field(ge=0)] = None


class WeatherData(BaseModel):
    temperature_c: float
    humidity: Annotated[int, Field(ge=0, le=100)]
    rainfall_mm: Optional[float] = None
    weather_alert: Optional[str] = None

class AgriAdvice(BaseModel):
    recommendations: Annotated[List[str], Field(default=[])]
    pest_management: Annotated[List[str], Field(default=[])]
    soil_amendments: Annotated[List[str], Field(default=[])]
    irrigation_advice: Optional[str] = None
    estimated_impact: Optional[str] = None
    
    @field_validator('recommendations', 'pest_management', 'soil_amendments', mode='before')
    @classmethod
    def normalize_recommendation_lists(cls, v):
        """Ensure recommendation lists are properly formatted."""
        if isinstance(v, str):
            v = [v]
        if not isinstance(v, list):
            v = list(v) if hasattr(v, '__iter__') else [v]
        v = [item.strip() for item in v if isinstance(item, str) and item.strip()]
        return v

# Global State TypedDict
class AgentState(TypedDict):
    farmer_input: Optional[FarmerInput]
    extracted_keywords: Optional[ExtractedKeywords]
    validation_result: Optional[ValidationResult]
    
    location_coords: Optional[dict]
    weather_data: Optional[WeatherData]
    soil_data: Optional[SoilData]
    timestamp: Optional[str]
    
    advice: Optional[AgriAdvice]
    messages: List[dict]
    processing_errors: List[str]
    processing_status: Literal['pending', 'processing', 'completed', 'failed']
