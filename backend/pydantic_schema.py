from pydantic import BaseModel,field_validator
import re
class RegistrationData(BaseModel):    
    name: str
    age: int
    education_level: str
    phone_no: str
    
    # Validators for data validation
    @field_validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        if not re.match(r'^[a-zA-Z\s]+$', v.strip()):
            raise ValueError('Name must contain only letters and spaces')
        return v.strip().title()
    
    @field_validator('age')
    def validate_age(cls, v):
        if v < 16 or v > 100:
            raise ValueError('Age must be between 16 and 100')
        return v
    
    @field_validator('education_level')
    def validate_education_level(cls, v):
        valid_levels = [
            'High School', 'Diploma', 'Bachelor\'s Degree', 
            'Master\'s Degree', 'PhD', 'Other'
        ]
        if v not in valid_levels:
            raise ValueError(f'Education level must be one of: {", ".join(valid_levels)}')
        return v
    
    @field_validator('phone_no')
    def validate_phone(cls, v):
        # Remove any spaces, dashes, or parentheses
        phone_clean = re.sub(r'[\s\-\(\)]', '', v)
        
        # Check if it's a valid phone number format (10 digits for most countries)
        if not re.match(r'^\+?[1-9]\d{9,14}$', phone_clean):
            raise ValueError('Phone number must be a valid format (10-15 digits)')
        return phone_clean

