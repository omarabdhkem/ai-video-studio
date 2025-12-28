"""Video assembly agent using MoviePy"""
from moviepy.editor import (
    VideoClip,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips
)
from typing import List, Dict, Any, Optional
import logging
import os
from config.settings import settings

logger = logging.getLogger(__name__)


class VideoAgent:
    """Agent for assembling videos from scenes"""
    
    # Constants
    MAX_CHARS_PER_LINE = 40  # Maximum characters per line for subtitles
    
    def __init__(self):
        """Initialize video agent"""
        self.output_path = settings.OUTPUT_PATH
        self.temp_path = settings.TEMP_PATH
        
        # Ensure directories exist
        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.temp_path, exist_ok=True)
    
    async def create_video_from_scenes(
        self,
        scenes: List[Dict[str, Any]],
        output_filename: str,
        background_color: str = "#1a1a1a",
        text_color: str = "#ffffff",
        font_size: int = 60,
        add_subtitles: bool = True,
        resolution: tuple = (1920, 1080)
    ) -> str:
        """
        Create video from scenes with voice and text
        
        Args:
            scenes: List of scene dictionaries with text, voice_file, duration
            output_filename: Output video file path
            background_color: Background color (hex)
            text_color: Text color (hex)
            font_size: Font size for subtitles
            add_subtitles: Whether to add subtitles
            resolution: Video resolution (width, height)
            
        Returns:
            Path to output video file
        """
        try:
            logger.info(f"Creating video from {len(scenes)} scenes")
            
            video_clips = []
            
            for i, scene in enumerate(scenes):
                logger.info(f"Processing scene {i + 1}/{len(scenes)}")
                
                text = scene.get("text", "")
                voice_file = scene.get("voice_file")
                duration = scene.get("duration", 5.0)
                
                # Create scene clip
                scene_clip = await self._create_scene_clip(
                    text=text,
                    voice_file=voice_file,
                    duration=duration,
                    background_color=background_color,
                    text_color=text_color,
                    font_size=font_size,
                    add_subtitles=add_subtitles,
                    resolution=resolution
                )
                
                if scene_clip:
                    video_clips.append(scene_clip)
            
            if not video_clips:
                raise ValueError("No video clips were created")
            
            # Concatenate all clips
            logger.info("Concatenating video clips")
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            # Write output file
            logger.info(f"Writing video to {output_filename}")
            final_video.write_videofile(
                output_filename,
                fps=24,
                codec="libx264",
                audio_codec="aac",
                temp_audiofile=os.path.join(self.temp_path, "temp_audio.m4a"),
                remove_temp=True,
                threads=4,
                preset="medium"
            )
            
            # Close clips
            for clip in video_clips:
                clip.close()
            final_video.close()
            
            logger.info(f"Video created successfully: {output_filename}")
            return output_filename
            
        except Exception as e:
            logger.error(f"Failed to create video: {str(e)}")
            raise Exception(f"Video creation failed: {str(e)}")
    
    async def _create_scene_clip(
        self,
        text: str,
        voice_file: Optional[str],
        duration: float,
        background_color: str,
        text_color: str,
        font_size: int,
        add_subtitles: bool,
        resolution: tuple
    ) -> Optional[VideoClip]:
        """
        Create a single scene clip
        
        Args:
            text: Scene text
            voice_file: Path to voice audio file
            duration: Scene duration
            background_color: Background color
            text_color: Text color
            font_size: Font size
            add_subtitles: Whether to add subtitles
            resolution: Video resolution
            
        Returns:
            VideoClip or None
        """
        try:
            width, height = resolution
            
            # Create background clip
            def make_frame(t):
                """Create a solid color frame"""
                import numpy as np
                # Convert hex color to RGB
                color = self._hex_to_rgb(background_color)
                return np.full((height, width, 3), color, dtype=np.uint8)
            
            # Load audio if available
            if voice_file and os.path.exists(voice_file):
                audio = AudioFileClip(voice_file)
                duration = audio.duration
            else:
                audio = None
            
            # Create video clip with background
            video_clip = VideoClip(make_frame, duration=duration)
            
            # Add audio
            if audio:
                video_clip = video_clip.set_audio(audio)
            
            # Add subtitles if requested
            if add_subtitles and text:
                text_clip = self._create_text_clip(
                    text=text,
                    duration=duration,
                    text_color=text_color,
                    font_size=font_size,
                    resolution=resolution
                )
                
                if text_clip:
                    # Position text in center
                    text_clip = text_clip.set_position("center")
                    video_clip = CompositeVideoClip([video_clip, text_clip])
            
            return video_clip
            
        except Exception as e:
            logger.error(f"Failed to create scene clip: {str(e)}")
            return None
    
    def _create_text_clip(
        self,
        text: str,
        duration: float,
        text_color: str,
        font_size: int,
        resolution: tuple
    ) -> Optional[TextClip]:
        """
        Create text clip for subtitles
        
        Args:
            text: Text content
            duration: Clip duration
            text_color: Text color
            font_size: Font size
            resolution: Video resolution
            
        Returns:
            TextClip or None
        """
        try:
            width, height = resolution
            
            # Split text into lines if too long
            max_chars_per_line = self.MAX_CHARS_PER_LINE
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                current_line.append(word)
                if len(" ".join(current_line)) > max_chars_per_line:
                    if len(current_line) > 1:
                        current_line.pop()
                        lines.append(" ".join(current_line))
                        current_line = [word]
                    else:
                        lines.append(" ".join(current_line))
                        current_line = []
            
            if current_line:
                lines.append(" ".join(current_line))
            
            # Join lines
            formatted_text = "\n".join(lines)
            
            # Create text clip
            txt_clip = TextClip(
                formatted_text,
                fontsize=font_size,
                color=text_color,
                size=(int(width * 0.8), None),
                method="caption",
                align="center"
            )
            
            txt_clip = txt_clip.set_duration(duration)
            
            return txt_clip
            
        except Exception as e:
            logger.error(f"Failed to create text clip: {str(e)}")
            return None
    
    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """
        Convert hex color to RGB tuple
        
        Args:
            hex_color: Hex color string (e.g., "#1a1a1a")
            
        Returns:
            RGB tuple (r, g, b)
        """
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# Singleton instance
video_agent = VideoAgent()
