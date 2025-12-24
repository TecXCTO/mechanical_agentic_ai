class MechanicalAIError(Exception):
    """Base exception for this project."""
    pass

class CADIntegrationError(MechanicalAIError):
    """Exception for errors during CAD integration."""
    pass

class SimulationError(MechanicalAIError):
    """Exception for errors during simulation."""
    pass

class AnalysisError(MechanicalAIError):
    """Exception for errors during analysis."""
    pass

class ManufacturingError(MechanicalAIError):
    """Exception for errors during manufacturing operations."""
    pass

class KnowledgeBaseError(MechanicalAIError):
    """Exception for errors related to the knowledge base."""
    pass
