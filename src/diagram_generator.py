"""
Diagram Generator Module
Safely executes generated diagram code and creates professional diagrams
"""
import os
import sys
import tempfile
from pathlib import Path
from typing import Optional, Tuple
import subprocess


class DiagramGenerator:
    """Generates diagram images from Python code"""

    def __init__(self, output_dir: str = "outputs"):
        """Initialize the diagram generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_diagram(
        self,
        diagram_code: str,
        output_filename: str = "architecture_diagram"
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Generate a diagram from Python code

        Args:
            diagram_code: Python code that uses diagrams library
            output_filename: Base name for the output file (without extension)

        Returns:
            Tuple of (success, output_path, error_message)
        """
        try:
            # Create a temporary Python file
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix='.py',
                delete=False,
                dir=str(self.output_dir)
            ) as temp_file:
                # Modify the code to save to our output directory
                modified_code = self._prepare_code(diagram_code, output_filename)
                temp_file.write(modified_code)
                temp_file_path = temp_file.name

            # Execute the code in a subprocess for safety
            result = subprocess.run(
                [sys.executable, temp_file_path],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.output_dir)
            )

            # Clean up the temporary file
            os.unlink(temp_file_path)

            if result.returncode == 0:
                # Find the generated diagram file
                output_path = self.output_dir / f"{output_filename}.png"
                if output_path.exists():
                    return True, str(output_path), None
                else:
                    return False, None, "Diagram file was not created"
            else:
                error_msg = result.stderr or result.stdout
                return False, None, f"Execution error: {error_msg}"

        except subprocess.TimeoutExpired:
            return False, None, "Diagram generation timed out (30s limit)"
        except Exception as e:
            return False, None, f"Error generating diagram: {str(e)}"

    def _prepare_code(self, diagram_code: str, output_filename: str) -> str:
        """
        Prepare the diagram code for execution

        Ensures proper imports and output configuration
        """
        lines = diagram_code.strip().split('\n')
        prepared_lines = []

        # Track if we've found the Diagram constructor
        diagram_found = False

        for line in lines:
            # Look for Diagram constructor and modify it
            if 'Diagram(' in line and not diagram_found:
                # Extract the diagram name if present
                if 'name=' in line:
                    # Keep the original line but ensure it has the right filename
                    modified_line = line
                    if 'filename=' not in line:
                        # Add filename parameter before the closing parenthesis
                        modified_line = modified_line.rstrip()
                        if modified_line.endswith('):'):
                            modified_line = modified_line[:-2] + f', filename="{output_filename}"):'
                        elif modified_line.endswith(')'):
                            modified_line = modified_line[:-1] + f', filename="{output_filename}")'
                    prepared_lines.append(modified_line)
                else:
                    # Add both name and filename
                    modified_line = line.replace(
                        'Diagram(',
                        f'Diagram(name="Architecture Diagram", filename="{output_filename}", '
                    )
                    prepared_lines.append(modified_line)
                diagram_found = True
            else:
                prepared_lines.append(line)

        return '\n'.join(prepared_lines)

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
