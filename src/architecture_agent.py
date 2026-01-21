"""
Architecture Diagram Agent using Agno SDK and Gemini Nano Banana
"""
import os
from typing import Dict, Any, Optional
from agno import Agent, Runner
from pydantic import BaseModel, Field


class DiagramRequest(BaseModel):
    """Model for diagram generation request"""
    description: str = Field(..., description="Description of the architecture to diagram")
    architecture_type: str = Field(default="cloud", description="Type of architecture (cloud, microservices, network, etc.)")
    cloud_provider: Optional[str] = Field(default=None, description="Cloud provider (AWS, GCP, Azure)")
    components: Optional[str] = Field(default=None, description="Specific components to include")


class DiagramResponse(BaseModel):
    """Model for diagram generation response"""
    image_prompt: str = Field(..., description="Detailed prompt for Nano Banana image generation")
    description: str = Field(..., description="Description of the diagram")
    components: list[str] = Field(..., description="List of components in the diagram")
    best_practices: list[str] = Field(..., description="Architecture best practices applied")


class ArchitectureAgent:
    """Agent for generating professional architecture diagrams"""

    def __init__(self, google_api_key: str):
        """Initialize the architecture agent with Gemini"""
        self.google_api_key = google_api_key

        # Create the Agno agent with Gemini model
        self.agent = Agent(
            name="Architecture Diagram Expert",
            model="gemini/gemini-2.0-flash-exp",
            description="Expert in creating detailed prompts for AI-generated architecture diagrams",
            instructions=[
                "You are an expert solutions architect and visual prompt designer.",
                "You create detailed, comprehensive prompts for generating professional architecture diagrams using AI image generation.",
                "Always follow industry best practices for architecture design.",
                "Use proper naming conventions and clear component relationships.",
                "Include security considerations, scalability patterns, and resilience.",
                "Generate a highly detailed prompt for Nano Banana (Google's Gemini Image Generation) that describes:",
                "  - The overall layout and structure of the architecture diagram",
                "  - All components and their visual representation (boxes, icons, shapes)",
                "  - The connections and data flows between components (arrows, lines)",
                "  - Logical groupings and boundaries (clusters, zones, networks)",
                "  - Labels, text annotations, and component names",
                "  - Colors and styling to indicate different layers or types of components",
                "  - Professional diagram style (technical, clean, infographic-style)",
                "The prompt should be detailed enough for an AI to generate a professional, publication-ready architecture diagram.",
                "Focus on visual details: shapes, positions, connections, colors, labels, and overall composition.",
            ],
            response_model=DiagramResponse,
            markdown=True,
            show_tool_calls=False,
            api_key=google_api_key
        )

    def generate_image_prompt(self, request: DiagramRequest) -> DiagramResponse:
        """Generate architecture diagram image prompt based on request"""

        # Build the prompt
        prompt = self._build_prompt(request)

        # Run the agent
        runner = Runner(agent=self.agent, api_key=self.google_api_key)
        response = runner.run(prompt)

        # Extract the response
        if hasattr(response, 'content'):
            # If response has structured content
            return response.content
        else:
            # Fallback to parsing the response
            return self._parse_response(response)

    def _build_prompt(self, request: DiagramRequest) -> str:
        """Build the prompt for the agent"""
        prompt_parts = [
            f"Create a detailed visual prompt for generating a professional architecture diagram image with the following requirements:",
            f"\nDescription: {request.description}",
            f"\nArchitecture Type: {request.architecture_type}",
        ]

        if request.cloud_provider:
            prompt_parts.append(f"\nCloud Provider: {request.cloud_provider}")

        if request.components:
            prompt_parts.append(f"\nSpecific Components: {request.components}")

        prompt_parts.extend([
            "\n\nGenerate a comprehensive, highly detailed prompt for Nano Banana (Google's Gemini Image Generation model).",
            "The prompt should describe:",
            "1. Overall composition: professional technical architecture diagram, clean infographic style, white background",
            "2. All components: describe each as labeled boxes/icons with specific names and purposes",
            "3. Visual hierarchy: different colors for different layers (e.g., blue for frontend, green for backend, orange for data layer)",
            "4. Connections: arrows showing data flow between components with labels",
            "5. Groupings: dotted boundaries or shaded areas for logical groups (e.g., VPC, security zones)",
            "6. Layout: left-to-right or top-to-bottom flow showing request/data paths",
            "7. Professional styling: clean lines, consistent spacing, readable labels",
            "8. Technical details: icons representing the technology (databases, servers, APIs, etc.)",
            "\n\nThe image_prompt should be 2-4 paragraphs, extremely detailed and visual, describing every element of the diagram.",
            "Think like you're instructing an artist to draw a technical diagram - be specific about positions, colors, shapes, and labels.",
            "\n\nProvide the response in the structured format with:",
            "- image_prompt: Comprehensive visual prompt for Nano Banana",
            "- description: Clear explanation of the architecture",
            "- components: List of all components in the diagram",
            "- best_practices: Architecture best practices applied"
        ])

        return "\n".join(prompt_parts)

    def _parse_response(self, response: Any) -> DiagramResponse:
        """Parse the agent response into DiagramResponse"""
        # This is a fallback parser if the response isn't already structured
        if isinstance(response, DiagramResponse):
            return response

        # Default response if parsing fails
        return DiagramResponse(
            image_prompt="Error: Could not generate image prompt",
            description="Error generating diagram prompt",
            components=[],
            best_practices=[]
        )


def create_architecture_agent(google_api_key: Optional[str] = None) -> ArchitectureAgent:
    """Factory function to create an architecture agent"""
    api_key = google_api_key or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "Google API key is required. Set GOOGLE_API_KEY environment variable "
            "or pass it as an argument."
        )

    return ArchitectureAgent(google_api_key=api_key)
