# Copyright: see copyright.txt
"""
Input modeling for symbolic execution.

Week 1: Skeleton implementation
Week 3: Will implement actual input modeling functionality
"""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from pathlib import Path


class InputType(Enum):
    """Supported input types."""
    INTEGER = "int"
    STRING = "str"
    STDIN_LINES = "stdin_lines"
    ARGV = "argv"
    BOOLEAN = "bool"
    # Future types
    # FLOAT = "float"
    # LIST = "list"
    # DICT = "dict"


@dataclass
class InputField:
    """Definition of a single input field."""
    name: str
    type: InputType
    description: Optional[str] = None
    default: Optional[Any] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    max_length: Optional[int] = None
    allowed_values: Optional[List[Any]] = None
    constraints: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "name": self.name,
            "type": self.type.value,
        }
        
        # Add optional fields if they exist
        if self.description is not None:
            result["description"] = self.description
        if self.default is not None:
            result["default"] = self.default
        if self.min_value is not None:
            result["min_value"] = self.min_value
        if self.max_value is not None:
            result["max_value"] = self.max_value
        if self.max_length is not None:
            result["max_length"] = self.max_length
        if self.allowed_values is not None:
            result["allowed_values"] = self.allowed_values
        if self.constraints is not None:
            result["constraints"] = self.constraints
            
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InputField':
        """Create from dictionary representation."""
        # Convert type string to InputType enum
        type_str = data.get('type', 'int')
        input_type = InputType(type_str)
        
        return cls(
            name=data['name'],
            type=input_type,
            description=data.get('description'),
            default=data.get('default'),
            min_value=data.get('min_value'),
            max_value=data.get('max_value'),
            max_length=data.get('max_length'),
            allowed_values=data.get('allowed_values'),
            constraints=data.get('constraints')
        )


@dataclass
class InputModel:
    """Complete input model for a program."""
    program_id: str
    fields: List[InputField] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_field(self, field: InputField) -> None:
        """Add an input field to the model."""
        self.fields.append(field)
    
    def get_field(self, name: str) -> Optional[InputField]:
        """Get field by name."""
        for field in self.fields:
            if field.name == name:
                return field
        return None
    
    def validate_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate input data against model.
        
        Returns:
            Dict with 'valid' flag and any errors
        """
        errors = []
        validated = {}
        
        for field in self.fields:
            field_name = field.name
            value = input_data.get(field_name, field.default)
            
            if value is None and field.default is None:
                errors.append(f"Field '{field_name}' is required but not provided")
                continue
            
            # Type validation
            if field.type == InputType.INTEGER:
                if not isinstance(value, int):
                    try:
                        value = int(value)
                    except (ValueError, TypeError):
                        errors.append(f"Field '{field_name}' must be an integer")
                        continue
                
                # Range validation
                if field.min_value is not None and value < field.min_value:
                    errors.append(f"Field '{field_name}' must be >= {field.min_value}")
                if field.max_value is not None and value > field.max_value:
                    errors.append(f"Field '{field_name}' must be <= {field.max_value}")
                    
            elif field.type == InputType.STRING:
                if not isinstance(value, str):
                    value = str(value)
                
                # Length validation
                if field.max_length is not None and len(value) > field.max_length:
                    errors.append(f"Field '{field_name}' length must be <= {field.max_length}")
            
            elif field.type == InputType.BOOLEAN:
                if not isinstance(value, bool):
                    if isinstance(value, str):
                        value = value.lower() in ('true', '1', 'yes', 'on')
                    elif isinstance(value, int):
                        value = bool(value)
                    else:
                        errors.append(f"Field '{field_name}' must be a boolean")
                        continue
            
            # Allowed values validation
            if field.allowed_values is not None and value not in field.allowed_values:
                errors.append(f"Field '{field_name}' must be one of {field.allowed_values}")
            
            validated[field_name] = value
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "validated_data": validated
        }
    
    def generate_symbolic_inputs(self) -> Dict[str, Any]:
        """
        Generate symbolic inputs based on model.
        
        Note: This is a skeleton implementation.
        Week 3 will implement actual symbolic input generation.
        """
        symbolic_inputs = {}
        
        for field in self.fields:
            if field.type == InputType.INTEGER:
                # For now, just return the default or a placeholder
                symbolic_inputs[field.name] = field.default if field.default is not None else 0
            elif field.type == InputType.STRING:
                symbolic_inputs[field.name] = field.default if field.default is not None else ""
            elif field.type == InputType.BOOLEAN:
                symbolic_inputs[field.name] = field.default if field.default is not None else False
            else:
                symbolic_inputs[field.name] = field.default
        
        return symbolic_inputs
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "program_id": self.program_id,
            "fields": [field.to_dict() for field in self.fields],
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InputModel':
        """Create from dictionary representation."""
        fields = [InputField.from_dict(field_data) for field_data in data.get('fields', [])]
        
        return cls(
            program_id=data['program_id'],
            fields=fields,
            metadata=data.get('metadata', {})
        )
    
    def save_to_file(self, filepath: Path) -> None:
        """Save model to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: Path) -> 'InputModel':
        """Load model from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)


class InputModelManager:
    """Manager for input models."""
    
    def __init__(self):
        self.models: Dict[str, InputModel] = {}
    
    def register_model(self, model: InputModel) -> None:
        """Register an input model."""
        self.models[model.program_id] = model
    
    def get_model(self, program_id: str) -> Optional[InputModel]:
        """Get model by program ID."""
        return self.models.get(program_id)
    
    def load_model_from_file(self, program_id: str, filepath: Path) -> None:
        """Load model from file and register it."""
        model = InputModel.load_from_file(filepath)
        self.register_model(model)
    
    def generate_all_symbolic_inputs(self) -> Dict[str, Dict[str, Any]]:
        """Generate symbolic inputs for all registered models."""
        return {
            program_id: model.generate_symbolic_inputs()
            for program_id, model in self.models.items()
        }


# Global instance for convenience
global_model_manager = InputModelManager()


def register_input_model(model: InputModel) -> None:
    """Register input model using global manager."""
    global_model_manager.register_model(model)


def get_input_model(program_id: str) -> Optional[InputModel]:
    """Get input model using global manager."""
    return global_model_manager.get_model(program_id)


def load_input_model(program_id: str, filepath: Path) -> None:
    """Load input model from file using global manager."""
    global_model_manager.load_model_from_file(program_id, filepath)