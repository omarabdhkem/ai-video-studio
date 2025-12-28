"""Voice generation agent using Edge-TTS"""
from services.tts_service import tts_service
from api.models import VoiceRequest, VoiceResponse, Language, VoiceGender
from typing import List, Dict, Any
import logging
import os

logger = logging.getLogger(__name__)


class VoiceAgent:
    """Agent for generating voice/speech from text"""
    
    def __init__(self):
        """Initialize voice agent"""
        self.tts_service = tts_service
    
    async def generate_voice(self, request: VoiceRequest, output_filename: str) -> VoiceResponse:
        """
        Generate voice from text
        
        Args:
            request: Voice generation request
            output_filename: Output file name
            
        Returns:
            Voice generation response
        """
        try:
            logger.info(f"Generating voice for text: {request.text[:50]}...")
            
            # Calculate rate parameter from speed
            rate = self._speed_to_rate(request.speed)
            
            # Generate speech
            output_file, duration = await self.tts_service.generate_speech(
                text=request.text,
                output_file=output_filename,
                language=request.language.value,
                gender=request.gender.value,
                rate=rate
            )
            
            # Get voice name
            voice_name = self.tts_service.get_voice_name(
                language=request.language.value,
                gender=request.gender.value
            )
            
            response = VoiceResponse(
                audio_file=output_file,
                duration=duration,
                language=request.language,
                voice_name=voice_name
            )
            
            logger.info(f"Voice generated successfully: {output_file}")
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate voice: {str(e)}")
            raise Exception(f"Voice generation failed: {str(e)}")
    
    async def generate_voices_for_scenes(
        self,
        scenes: List[Dict[str, Any]],
        project_id: str,
        language: Language,
        gender: VoiceGender
    ) -> List[Dict[str, Any]]:
        """
        Generate voices for multiple scenes
        
        Args:
            scenes: List of scene dictionaries
            project_id: Project identifier
            language: Language
            gender: Voice gender
            
        Returns:
            List of scenes with voice files and durations
        """
        try:
            logger.info(f"Generating voices for {len(scenes)} scenes")
            
            # Convert scenes to list of dicts if needed
            scenes_list = []
            for scene in scenes:
                if hasattr(scene, 'dict'):
                    scenes_list.append(scene.dict())
                else:
                    scenes_list.append(scene)
            
            # Generate speeches
            updated_scenes = await self.tts_service.generate_speech_for_scenes(
                scenes=scenes_list,
                project_id=project_id,
                language=language.value,
                gender=gender.value
            )
            
            logger.info(f"Generated {len(updated_scenes)} voice files")
            return updated_scenes
            
        except Exception as e:
            logger.error(f"Failed to generate voices for scenes: {str(e)}")
            raise Exception(f"Batch voice generation failed: {str(e)}")
    
    def _speed_to_rate(self, speed: float) -> str:
        """
        Convert speed multiplier to Edge-TTS rate parameter
        
        Args:
            speed: Speed multiplier (0.5 to 2.0)
            
        Returns:
            Rate string (e.g., "+20%" or "-30%")
        """
        # Convert speed to percentage
        # speed 1.0 = +0%
        # speed 1.5 = +50%
        # speed 0.5 = -50%
        percentage = int((speed - 1.0) * 100)
        
        if percentage >= 0:
            return f"+{percentage}%"
        else:
            return f"{percentage}%"
    
    @staticmethod
    async def list_available_voices() -> List[Dict[str, str]]:
        """
        List all available voices
        
        Returns:
            List of available voices
        """
        try:
            return await tts_service.list_available_voices()
        except Exception as e:
            logger.error(f"Failed to list voices: {str(e)}")
            return []


# Singleton instance
voice_agent = VoiceAgent()
