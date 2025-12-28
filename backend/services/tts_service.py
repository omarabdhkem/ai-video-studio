import edge_tts
import os
from typing import Optional
from config.settings import settings
import asyncio


class TTSService:
    """Service for text-to-speech using Edge-TTS"""
    
    def __init__(self):
        """Initialize TTS service"""
        self.output_path = settings.OUTPUT_PATH
        self.temp_path = settings.TEMP_PATH
        
        # Ensure directories exist
        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.temp_path, exist_ok=True)
    
    def get_voice_name(self, language: str, gender: str) -> str:
        """
        Get voice name based on language and gender
        
        Args:
            language: Language code (ar or en)
            gender: Gender (male or female)
            
        Returns:
            Voice name for Edge-TTS
        """
        voice_map = {
            ("ar", "male"): settings.ARABIC_VOICE_MALE,
            ("ar", "female"): settings.ARABIC_VOICE_FEMALE,
            ("en", "male"): settings.ENGLISH_VOICE_MALE,
            ("en", "female"): settings.ENGLISH_VOICE_FEMALE,
        }
        
        return voice_map.get((language, gender), settings.ARABIC_VOICE_MALE)
    
    async def generate_speech(
        self,
        text: str,
        output_file: str,
        language: str = "ar",
        gender: str = "male",
        rate: str = "+0%",
        volume: str = "+0%"
    ) -> tuple[str, float]:
        """
        Generate speech from text using Edge-TTS
        
        Args:
            text: Text to convert to speech
            output_file: Output file path
            language: Language code
            gender: Voice gender
            rate: Speech rate (-50% to +50%)
            volume: Speech volume (-50% to +50%)
            
        Returns:
            Tuple of (output_file_path, duration_in_seconds)
        """
        try:
            # Get voice name
            voice = self.get_voice_name(language, gender)
            
            # Create communicate object
            communicate = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=rate,
                volume=volume
            )
            
            # Save audio file
            await communicate.save(output_file)
            
            # Calculate duration (approximate - 150 words per minute average)
            words = len(text.split())
            duration = (words / 150.0) * 60.0
            
            return output_file, duration
            
        except Exception as e:
            raise Exception(f"Failed to generate speech: {str(e)}")
    
    async def generate_speech_for_scenes(
        self,
        scenes: list,
        project_id: str,
        language: str = "ar",
        gender: str = "male"
    ) -> list:
        """
        Generate speech for multiple scenes
        
        Args:
            scenes: List of scene dictionaries
            project_id: Project identifier
            language: Language code
            gender: Voice gender
            
        Returns:
            List of scenes with voice_file and duration added
        """
        updated_scenes = []
        
        for scene in scenes:
            scene_number = scene.get("scene_number", 0)
            text = scene.get("text", "")
            
            if not text:
                continue
            
            # Generate output filename
            output_filename = f"{project_id}_scene_{scene_number}.mp3"
            output_path = os.path.join(self.temp_path, output_filename)
            
            # Generate speech
            audio_file, duration = await self.generate_speech(
                text=text,
                output_file=output_path,
                language=language,
                gender=gender
            )
            
            # Update scene with audio info
            updated_scene = scene.copy()
            updated_scene["voice_file"] = audio_file
            updated_scene["duration"] = duration
            updated_scenes.append(updated_scene)
        
        return updated_scenes
    
    @staticmethod
    async def list_available_voices() -> list:
        """
        List all available voices
        
        Returns:
            List of available voice names
        """
        try:
            voices = await edge_tts.list_voices()
            return [
                {
                    "name": voice["Name"],
                    "language": voice["Locale"],
                    "gender": voice["Gender"]
                }
                for voice in voices
            ]
        except Exception as e:
            raise Exception(f"Failed to list voices: {str(e)}")


# Singleton instance
tts_service = TTSService()
