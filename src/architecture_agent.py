"""
Architecture Diagram Agent using Agno SDK and Gemini
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
    diagram_code: str = Field(..., description="Python code to generate the diagram")
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
            description="Expert in creating professional architecture diagrams with best practices",
            instructions=[
                "You are an expert solutions architect and diagram designer.",
                "You create professional, clear, and well-structured architecture diagrams.",
                "Always follow industry best practices for architecture design.",
                "Use proper naming conventions and clear component relationships.",
                "Include security considerations, scalability patterns, and resilience.",
                "Generate Python code using the 'diagrams' library that creates professional diagrams.",
                "Ensure the diagram code is complete, runnable, and follows best practices.",
                "Include relevant components, connections, and groupings (clusters).",
                "Add appropriate labels, directions, and styling for professional appearance.",
            ],
            response_model=DiagramResponse,
            markdown=True,
            show_tool_calls=False,
            api_key=google_api_key
        )

    def generate_diagram_code(self, request: DiagramRequest) -> DiagramResponse:
        """Generate architecture diagram code based on request"""

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
            f"Create a professional architecture diagram with the following requirements:",
            f"\nDescription: {request.description}",
            f"\nArchitecture Type: {request.architecture_type}",
        ]

        if request.cloud_provider:
            prompt_parts.append(f"\nCloud Provider: {request.cloud_provider}")

        if request.components:
            prompt_parts.append(f"\nSpecific Components: {request.components}")

        prompt_parts.extend([
            "\n\nGenerate complete, runnable Python code using the 'diagrams' library.",
            "The code should:",
            "1. Import necessary modules from diagrams library",
            "2. Create a Diagram object with appropriate name and direction",
            "3. Define all components with proper icons based on the cloud provider",
            "4. Use Cluster objects for logical groupings",
            "5. Connect components with arrows showing data/control flow",
            "6. Follow architecture best practices",
            "7. Be production-ready and professional",
            "\n\nProvide the response in the structured format with:",
            "- diagram_code: Complete Python code",
            "- description: Clear explanation of the architecture",
            "- components: List of all components used",
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
            diagram_code="# Error: Could not generate diagram code",
            description="Error generating diagram",
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
