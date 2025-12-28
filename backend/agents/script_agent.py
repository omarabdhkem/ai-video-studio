"""Script generation agent using Groq API"""
from services.groq_service import groq_service
from api.models import ScriptRequest, ScriptResponse, Scene, Language
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class ScriptAgent:
    """Agent for generating video scripts"""
    
    def __init__(self):
        """Initialize script agent"""
        self.groq_service = groq_service
    
    async def generate_script(self, request: ScriptRequest) -> ScriptResponse:
        """
        Generate video script based on request
        
        Args:
            request: Script generation request
            
        Returns:
            Generated script response
        """
        try:
            logger.info(f"Generating script for topic: {request.topic}")
            
            # Generate script using Groq
            script_data = await self.groq_service.generate_script(
                topic=request.topic,
                language=request.language.value,
                duration_minutes=request.duration_minutes,
                style=request.style or "informative"
            )
            
            # Convert to Scene objects
            scenes = []
            for scene_data in script_data.get("scenes", []):
                scene = Scene(
                    scene_number=scene_data["scene_number"],
                    text=scene_data["text"],
                    duration=None,
                    voice_file=None
                )
                scenes.append(scene)
            
            # Create response
            response = ScriptResponse(
                title=script_data.get("title", "Untitled"),
                description=script_data.get("description", ""),
                scenes=scenes,
                total_duration=None,
                language=request.language
            )
            
            logger.info(f"Script generated successfully with {len(scenes)} scenes")
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate script: {str(e)}")
            raise Exception(f"Script generation failed: {str(e)}")
    
    async def enhance_scene_text(self, text: str, language: Language) -> str:
        """
        Enhance scene text for better speech output
        
        Args:
            text: Original text
            language: Language
            
        Returns:
            Enhanced text
        """
        try:
            return await self.groq_service.enhance_text(
                text=text,
                language=language.value
            )
        except Exception as e:
            logger.warning(f"Failed to enhance text: {str(e)}")
            return text


# Singleton instance
script_agent = ScriptAgent()
