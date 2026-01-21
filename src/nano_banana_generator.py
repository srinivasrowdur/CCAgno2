"""
Nano Banana Image Generator Module
Uses Google's Gemini Image Generation (Nano Banana) to create architecture diagrams
"""
import os
from pathlib import Path
from typing import Optional, Tuple
from io import BytesIO
from PIL import Image

try:
    from google import genai
    from google.genai import types
except ImportError:
    raise ImportError(
        "google-genai package is required. Install with: pip install google-genai"
    )


class NanoBananaGenerator:
    """Generates architecture diagram images using Nano Banana (Gemini Image Generation)"""

    def __init__(self, api_key: str, output_dir: str = "outputs"):
        """
        Initialize the Nano Banana generator

        Args:
            api_key: Google API key for authentication
            output_dir: Directory to save generated images
        """
        self.api_key = api_key
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize the Google GenAI client
        self.client = genai.Client(api_key=api_key)

    def generate_diagram(
        self,
        prompt: str,
        output_filename: str = "architecture_diagram",
        model: str = "gemini-2.5-flash-image"
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Generate an architecture diagram image from a text prompt

        Args:
            prompt: Detailed text prompt describing the architecture diagram
            output_filename: Base name for the output file (without extension)
            model: Nano Banana model to use (gemini-2.5-flash-image or gemini-3-pro-image-preview)

        Returns:
            Tuple of (success, output_path, error_message)
        """
        try:
            # Generate the image using Nano Banana
            response = self.client.models.generate_content(
                model=model,
                contents=[prompt],
            )

            # Extract and save the image
            image_saved = False
            output_path = self.output_dir / f"{output_filename}.png"

            for part in response.parts:
                if part.inline_data is not None:
                    # Get the image data
                    image_data = part.inline_data.data

                    # Open and save the image
                    image = Image.open(BytesIO(image_data))
                    image.save(str(output_path))
                    image_saved = True
                    break
                elif hasattr(part, 'as_image'):
                    # Alternative method to get image
                    image = part.as_image()
                    image.save(str(output_path))
                    image_saved = True
                    break

            if image_saved:
                return True, str(output_path), None
            else:
                return False, None, "No image was generated in the response"

        except Exception as e:
            return False, None, f"Error generating image: {str(e)}"

    def generate_diagram_with_editing(
        self,
        prompt: str,
        reference_image_path: Optional[str] = None,
        output_filename: str = "architecture_diagram",
        model: str = "gemini-2.5-flash-image"
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Generate or edit an architecture diagram image

        Args:
            prompt: Detailed text prompt describing the architecture diagram
            reference_image_path: Optional path to a reference image for editing
            output_filename: Base name for the output file (without extension)
            model: Nano Banana model to use

        Returns:
            Tuple of (success, output_path, error_message)
        """
        try:
            contents = [prompt]

            # If reference image is provided, include it
            if reference_image_path and os.path.exists(reference_image_path):
                reference_image = Image.open(reference_image_path)
                contents.append(reference_image)

            # Generate the image using Nano Banana
            response = self.client.models.generate_content(
                model=model,
                contents=contents,
            )

            # Extract and save the image
            image_saved = False
            output_path = self.output_dir / f"{output_filename}.png"

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    # Get the image data
                    image_data = part.inline_data.data

                    # Open and save the image
                    image = Image.open(BytesIO(image_data))
                    image.save(str(output_path))
                    image_saved = True
                    break

            if image_saved:
                return True, str(output_path), None
            else:
                return False, None, "No image was generated in the response"

        except Exception as e:
            return False, None, f"Error generating/editing image: {str(e)}"

    def list_generated_diagrams(self) -> list[str]:
        """List all generated diagram files"""
        return [
            str(f)
            for f in self.output_dir.glob("*.png")
        ]

    def clear_outputs(self):
        """Clear all generated diagrams"""
        for file in self.output_dir.glob("*.png"):
            file.unlink()
