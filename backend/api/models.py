from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class Language(str, Enum):
    """Supported languages"""
    ARABIC = "ar"
    ENGLISH = "en"


class ProjectStatus(str, Enum):
    """Project status"""
    CREATED = "created"
    GENERATING_SCRIPT = "generating_script"
    GENERATING_VOICE = "generating_voice"
    GENERATING_VIDEO = "generating_video"
    COMPLETED = "completed"
    FAILED = "failed"


class VoiceGender(str, Enum):
    """Voice gender"""
    MALE = "male"
    FEMALE = "female"


class Scene(BaseModel):
    """Video scene model"""
    scene_number: int
    text: str
    duration: Optional[float] = None
    voice_file: Optional[str] = None


class ScriptRequest(BaseModel):
    """Request model for script generation"""
    topic: str = Field(..., description="Video topic", min_length=5, max_length=500)
    language: Language = Field(default=Language.ARABIC, description="Script language")
    duration_minutes: int = Field(default=3, ge=1, le=10, description="Target video duration in minutes")
    style: Optional[str] = Field(default="informative", description="Script style")


class ScriptResponse(BaseModel):
    """Response model for generated script"""
    title: str
    description: str
    scenes: List[Scene]
    total_duration: Optional[float] = None
    language: Language


class VoiceRequest(BaseModel):
    """Request model for voice generation"""
    text: str = Field(..., description="Text to convert to speech")
    language: Language = Field(default=Language.ARABIC, description="Voice language")
    gender: VoiceGender = Field(default=VoiceGender.MALE, description="Voice gender")
    speed: float = Field(default=1.0, ge=0.5, le=2.0, description="Speech speed")


class VoiceResponse(BaseModel):
    """Response model for voice generation"""
    audio_file: str
    duration: float
    language: Language
    voice_name: str


class ProjectCreateRequest(BaseModel):
    """Request model for creating a project"""
    title: str = Field(..., description="Project title", min_length=3, max_length=200)
    topic: str = Field(..., description="Video topic", min_length=5, max_length=500)
    language: Language = Field(default=Language.ARABIC, description="Content language")
    voice_gender: VoiceGender = Field(default=VoiceGender.MALE, description="Voice gender")
    duration_minutes: int = Field(default=3, ge=1, le=10, description="Target duration")
    style: Optional[str] = Field(default="informative", description="Video style")


class ProjectResponse(BaseModel):
    """Response model for project"""
    id: str
    title: str
    topic: str
    language: Language
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    script: Optional[ScriptResponse] = None
    video_url: Optional[str] = None
    progress: int = Field(default=0, ge=0, le=100, description="Progress percentage")
    error_message: Optional[str] = None


class ProjectListResponse(BaseModel):
    """Response model for project list"""
    projects: List[ProjectResponse]
    total: int
    page: int
    page_size: int


class VideoGenerationRequest(BaseModel):
    """Request model for video generation"""
    project_id: str
    background_color: str = Field(default="#1a1a1a", description="Background color")
    text_color: str = Field(default="#ffffff", description="Text color")
    font_size: int = Field(default=60, ge=20, le=100, description="Font size")
    add_subtitles: bool = Field(default=True, description="Add subtitles to video")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    services: Dict[str, str]


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
