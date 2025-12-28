from fastapi import APIRouter, HTTPException, BackgroundTasks
from api.models import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectListResponse,
    ScriptRequest,
    ScriptResponse,
    VoiceRequest,
    VoiceResponse,
    VideoGenerationRequest,
    HealthResponse,
    ErrorResponse,
    ProjectStatus,
    Language,
    VoiceGender
)
from agents.script_agent import script_agent
from agents.voice_agent import voice_agent
from agents.video_agent import video_agent
from typing import List, Dict, Any
import uuid
import logging
from datetime import datetime
import os
from config.settings import settings

logger = logging.getLogger(__name__)

# Router
router = APIRouter(prefix=settings.API_V1_PREFIX)

# In-memory storage for projects (replace with database in production)
projects_db: Dict[str, Dict[str, Any]] = {}


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        services={
            "groq": "available" if settings.GROQ_API_KEY else "not_configured",
            "edge_tts": "available",
            "moviepy": "available"
        }
    )


@router.post("/projects/create", response_model=ProjectResponse)
async def create_project(
    request: ProjectCreateRequest,
    background_tasks: BackgroundTasks
):
    """
    Create a new video project
    
    This endpoint creates a project and initiates the video generation pipeline:
    1. Generate script
    2. Generate voice
    3. Assemble video
    """
    try:
        # Generate project ID
        project_id = str(uuid.uuid4())
        
        # Create project record
        project = {
            "id": project_id,
            "title": request.title,
            "topic": request.topic,
            "language": request.language,
            "voice_gender": request.voice_gender,
            "duration_minutes": request.duration_minutes,
            "style": request.style,
            "status": ProjectStatus.CREATED,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "script": None,
            "video_url": None,
            "progress": 0,
            "error_message": None
        }
        
        # Store project
        projects_db[project_id] = project
        
        # Start video generation in background
        background_tasks.add_task(
            generate_video_pipeline,
            project_id=project_id,
            topic=request.topic,
            language=request.language,
            voice_gender=request.voice_gender,
            duration_minutes=request.duration_minutes,
            style=request.style
        )
        
        logger.info(f"Project created: {project_id}")
        
        return ProjectResponse(**project)
        
    except Exception as e:
        logger.error(f"Failed to create project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/script", response_model=ScriptResponse)
async def generate_script(request: ScriptRequest):
    """
    Generate video script using Groq API
    """
    try:
        logger.info(f"Generating script for topic: {request.topic}")
        
        # Generate script
        script = await script_agent.generate_script(request)
        
        return script
        
    except Exception as e:
        logger.error(f"Failed to generate script: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate/voice", response_model=VoiceResponse)
async def generate_voice(request: VoiceRequest):
    """
    Generate voice from text using Edge-TTS
    """
    try:
        logger.info("Generating voice")
        
        # Generate output filename
        output_filename = os.path.join(
            settings.TEMP_PATH,
            f"voice_{uuid.uuid4()}.mp3"
        )
        
        # Generate voice
        voice = await voice_agent.generate_voice(request, output_filename)
        
        return voice
        
    except Exception as e:
        logger.error(f"Failed to generate voice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects", response_model=ProjectListResponse)
async def list_projects(
    page: int = 1,
    page_size: int = 10
):
    """
    List all projects with pagination
    """
    try:
        # Get all projects sorted by creation date
        all_projects = sorted(
            projects_db.values(),
            key=lambda x: x["created_at"],
            reverse=True
        )
        
        # Calculate pagination
        total = len(all_projects)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        projects_page = all_projects[start_idx:end_idx]
        
        # Convert to response models
        projects_list = [ProjectResponse(**p) for p in projects_page]
        
        return ProjectListResponse(
            projects=projects_list,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Failed to list projects: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """
    Get project details by ID
    """
    try:
        if project_id not in projects_db:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project = projects_db[project_id]
        return ProjectResponse(**project)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/projects/{project_id}/regenerate")
async def regenerate_video(
    project_id: str,
    background_tasks: BackgroundTasks
):
    """
    Regenerate video for an existing project
    """
    try:
        if project_id not in projects_db:
            raise HTTPException(status_code=404, detail="Project not found")
        
        project = projects_db[project_id]
        
        # Reset status
        project["status"] = ProjectStatus.CREATED
        project["progress"] = 0
        project["error_message"] = None
        project["updated_at"] = datetime.utcnow()
        
        # Start video generation in background
        background_tasks.add_task(
            generate_video_pipeline,
            project_id=project_id,
            topic=project["topic"],
            language=project["language"],
            voice_gender=project["voice_gender"],
            duration_minutes=project["duration_minutes"],
            style=project.get("style", "informative")
        )
        
        return ProjectResponse(**project)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to regenerate video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def generate_video_pipeline(
    project_id: str,
    topic: str,
    language: Language,
    voice_gender: VoiceGender,
    duration_minutes: int,
    style: str
):
    """
    Background task to generate complete video
    
    Pipeline:
    1. Generate script
    2. Generate voices for all scenes
    3. Assemble video
    """
    try:
        project = projects_db[project_id]
        
        # Step 1: Generate script
        logger.info(f"[{project_id}] Generating script...")
        project["status"] = ProjectStatus.GENERATING_SCRIPT
        project["progress"] = 10
        project["updated_at"] = datetime.utcnow()
        
        script_request = ScriptRequest(
            topic=topic,
            language=language,
            duration_minutes=duration_minutes,
            style=style
        )
        
        script = await script_agent.generate_script(script_request)
        project["script"] = script.dict()
        project["progress"] = 30
        project["updated_at"] = datetime.utcnow()
        
        # Step 2: Generate voices
        logger.info(f"[{project_id}] Generating voices...")
        project["status"] = ProjectStatus.GENERATING_VOICE
        project["progress"] = 40
        project["updated_at"] = datetime.utcnow()
        
        scenes_with_voice = await voice_agent.generate_voices_for_scenes(
            scenes=script.scenes,
            project_id=project_id,
            language=language,
            gender=voice_gender
        )
        
        project["script"]["scenes"] = scenes_with_voice
        project["progress"] = 60
        project["updated_at"] = datetime.utcnow()
        
        # Step 3: Assemble video
        logger.info(f"[{project_id}] Assembling video...")
        project["status"] = ProjectStatus.GENERATING_VIDEO
        project["progress"] = 70
        project["updated_at"] = datetime.utcnow()
        
        output_filename = os.path.join(
            settings.OUTPUT_PATH,
            f"{project_id}.mp4"
        )
        
        video_path = await video_agent.create_video_from_scenes(
            scenes=scenes_with_voice,
            output_filename=output_filename,
            background_color="#1a1a1a",
            text_color="#ffffff",
            font_size=60,
            add_subtitles=True
        )
        
        # Update project
        project["video_url"] = f"/api/v1/videos/{project_id}.mp4"
        project["status"] = ProjectStatus.COMPLETED
        project["progress"] = 100
        project["updated_at"] = datetime.utcnow()
        
        logger.info(f"[{project_id}] Video generation completed!")
        
    except Exception as e:
        logger.error(f"[{project_id}] Video generation failed: {str(e)}")
        project = projects_db.get(project_id)
        if project:
            project["status"] = ProjectStatus.FAILED
            project["error_message"] = str(e)
            project["updated_at"] = datetime.utcnow()
