from groq import Groq
from typing import Optional, List, Dict, Any
import json
from config.settings import settings


class GroqService:
    """Service for interacting with Groq API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Groq service"""
        self.api_key = api_key or settings.GROQ_API_KEY
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is required")
        self.client = Groq(api_key=self.api_key)
        self.model = settings.GROQ_MODEL
    
    async def generate_script(
        self,
        topic: str,
        language: str = "ar",
        duration_minutes: int = 3,
        style: str = "informative"
    ) -> Dict[str, Any]:
        """
        Generate video script using Groq API
        
        Args:
            topic: Video topic
            language: Language code (ar or en)
            duration_minutes: Target duration in minutes
            style: Script style
            
        Returns:
            Dictionary containing title, description, and scenes
        """
        
        # Determine language for prompts
        is_arabic = language == "ar"
        
        if is_arabic:
            system_prompt = """أنت كاتب محتوى محترف متخصص في إنشاء سكريبتات فيديوهات يوتيوب جذابة وممتعة.
            مهمتك هي إنشاء سكريبت منظم بشكل مشاهد (scenes) يمكن تحويله لفيديو."""
            
            user_prompt = f"""أنشئ سكريبت فيديو يوتيوب عن الموضوع التالي:
الموضوع: {topic}
المدة المستهدفة: {duration_minutes} دقائق
الأسلوب: {style}

يجب أن يحتوي السكريبت على:
1. عنوان جذاب
2. وصف مختصر
3. من 5 إلى 10 مشاهد (scenes)

أرجع النتيجة بصيغة JSON التالية:
{{
    "title": "عنوان الفيديو",
    "description": "وصف مختصر للفيديو",
    "scenes": [
        {{"scene_number": 1, "text": "نص المشهد الأول"}},
        {{"scene_number": 2, "text": "نص المشهد الثاني"}}
    ]
}}

تأكد من أن النص JSON فقط بدون أي نص إضافي."""
        else:
            system_prompt = """You are a professional content writer specialized in creating engaging YouTube video scripts.
            Your task is to create structured scripts divided into scenes that can be converted into videos."""
            
            user_prompt = f"""Create a YouTube video script about the following topic:
Topic: {topic}
Target Duration: {duration_minutes} minutes
Style: {style}

The script should contain:
1. An engaging title
2. A brief description
3. Between 5 to 10 scenes

Return the result in the following JSON format:
{{
    "title": "Video Title",
    "description": "Brief video description",
    "scenes": [
        {{"scene_number": 1, "text": "First scene text"}},
        {{"scene_number": 2, "text": "Second scene text"}}
    ]
}}

Make sure to return only JSON without any additional text."""
        
        try:
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=2048,
            )
            
            # Extract response
            response_text = chat_completion.choices[0].message.content.strip()
            
            # Try to extract JSON if there's extra text
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            script_data = json.loads(response_text)
            
            # Validate structure
            if "title" not in script_data or "scenes" not in script_data:
                raise ValueError("Invalid script structure")
            
            return script_data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse script JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to generate script: {str(e)}")
    
    async def enhance_text(self, text: str, language: str = "ar") -> str:
        """
        Enhance text for better speech output
        
        Args:
            text: Original text
            language: Language code
            
        Returns:
            Enhanced text
        """
        is_arabic = language == "ar"
        
        if is_arabic:
            prompt = f"حسّن النص التالي ليكون أكثر وضوحاً للقراءة الصوتية:\n\n{text}\n\nأرجع النص المحسّن فقط بدون أي إضافات."
        else:
            prompt = f"Improve the following text to be clearer for text-to-speech:\n\n{text}\n\nReturn only the improved text without any additions."
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.5,
                max_tokens=1024,
            )
            
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            # Fallback to original text if enhancement fails
            return text


# Singleton instance
groq_service = GroqService()
