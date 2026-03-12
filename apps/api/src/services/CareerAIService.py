from google import genai
import os

class CareerAIService:
    def __init__(self, project_id: str, location: str = "us-central1"):
        # The SDK automatically finds the JSON file via the 
        # GOOGLE_APPLICATION_CREDENTIALS environment variable
        self.client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location
        )
        self.model_id = "gemini-1.5-flash"

    def summarize_job(self, description: str) -> str:
        prompt = f"Summarize the following job description in 3-5 sentences: {description}"
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"AI Error: {e}")
            return "Summary unavailable at this time."