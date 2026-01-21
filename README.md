# 🏗️ Architecture Diagram Generator

A professional architecture diagram generator powered by **Agno Agentic SDK** and **Google Gemini**. Create beautiful, production-ready architecture diagrams using natural language descriptions.

![Architecture Diagram Generator](https://img.shields.io/badge/Powered%20by-Agno%20SDK-blue)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)

## ✨ Features

- **AI-Powered Generation**: Uses Google Gemini through Agno Agentic SDK to intelligently design architectures
- **Professional Diagrams**: Creates publication-ready diagrams with proper icons, layouts, and connections
- **Multiple Cloud Providers**: Supports AWS, GCP, Azure, and generic architectures
- **Pre-built Templates**: Quick-start templates for common architecture patterns
- **Best Practices**: Automatically applies industry best practices and patterns
- **Code Export**: Download generated Python code for customization
- **Interactive UI**: Beautiful, modern Streamlit interface

## 🎯 Architecture Patterns Supported

- Cloud Infrastructure (AWS, GCP, Azure)
- Microservices Architecture
- Serverless Applications
- Data Pipelines
- Machine Learning Pipelines
- Event-Driven Architectures
- CI/CD Pipelines
- Network Architectures

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Google API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Graphviz installed on your system

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CCAgno2
   ```

2. **Install Graphviz** (required for diagram generation)

   **Ubuntu/Debian:**
   ```bash
   sudo apt-get install graphviz
   ```

   **macOS:**
   ```bash
   brew install graphviz
   ```

   **Windows:**
   Download from [graphviz.org](https://graphviz.org/download/)

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage

### Basic Usage

1. **Enter your Google API Key** in the sidebar (or set it in `.env`)
2. **Describe your architecture** in the text area
3. **Select architecture type** and cloud provider
4. **Click "Generate Diagram"** and watch the AI create your diagram
5. **Download** the diagram or code

### Using Templates

1. Check **"Use a template"** in the sidebar
2. Select a pre-built template
3. Customize the description if needed
4. Generate your diagram

### Example Descriptions

**Three-Tier Web App:**
```
Create a scalable three-tier web application with an application load balancer,
auto-scaling EC2 instances, RDS database with read replicas, and S3 for static
assets. Include CloudFront for content delivery and Route 53 for DNS.
```

**Microservices:**
```
Design a microservices architecture with an API gateway, 5 independent services
(user, product, order, payment, notification), message queue for async communication,
service mesh for traffic management, and monitoring stack.
```

**Data Pipeline:**
```
Build a data pipeline that ingests data from multiple sources, processes it through
transformations, stores in data warehouse, and enables analytics and visualization.
Include data quality checks and monitoring.
```

## 🏗️ Project Structure

```
CCAgno2/
├── app.py                          # Main Streamlit application
├── src/
│   ├── architecture_agent.py       # Agno agent for diagram generation
│   ├── diagram_generator.py        # Diagram execution and rendering
│   └── templates.py                # Pre-built architecture templates
├── outputs/                        # Generated diagrams (created automatically)
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## 🔧 Architecture

### How It Works

1. **User Input**: User describes desired architecture in natural language
2. **AI Agent**: Agno agent with Gemini processes the request and generates Python code
3. **Code Generation**: Agent creates code using the `diagrams` library with proper components
4. **Execution**: Code is safely executed to generate the diagram image
5. **Display**: Diagram is rendered in the Streamlit UI with metadata

### Technology Stack

- **Agno SDK**: Agentic AI framework for orchestration
- **Google Gemini**: Large language model for intelligent generation
- **Streamlit**: Web application framework
- **Diagrams Library**: Python library for creating architecture diagrams
- **Graphviz**: Graph visualization software

## 🎨 Customization

### Adding Custom Templates

Edit `src/templates.py` to add your own templates:

```python
ARCHITECTURE_TEMPLATES = {
    "Your Template Name": {
        "description": "Template description",
        "architecture_type": "cloud",
        "cloud_provider": "AWS",
        "components": "List of components"
    }
}
```

### Modifying the Agent

Edit `src/architecture_agent.py` to customize:
- Agent instructions
- Response format
- Model parameters
- Prompt engineering

### Styling the UI

Edit `.streamlit/config.toml` for theme customization or modify the CSS in `app.py`.

## 📋 Requirements

### Python Packages

- streamlit==1.31.0
- agno==0.0.70
- google-generativeai==0.3.2
- diagrams==0.23.4
- graphviz==0.20.1
- Pillow==10.2.0
- pydantic==2.6.0
- python-dotenv==1.0.0

### System Requirements

- Python 3.9+
- Graphviz (system package)
- 4GB RAM minimum
- Internet connection for API calls

## 🐛 Troubleshooting

### "Graphviz not found" Error

Install Graphviz system package (see Installation section).

### API Key Errors

- Ensure your Google API key is valid
- Check that Gemini API is enabled in your Google Cloud project
- Verify the key has proper permissions

### Diagram Generation Timeout

- Increase timeout in `src/diagram_generator.py`
- Simplify your architecture description
- Check system resources

### Import Errors

```bash
pip install --upgrade -r requirements.txt
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Agno SDK](https://github.com/agno-sdk) for the agentic framework
- [Google Gemini](https://ai.google.dev/) for the AI model
- [Diagrams](https://diagrams.mingrammer.com/) for the diagram library
- [Streamlit](https://streamlit.io/) for the UI framework

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review example templates

---

**Built with ❤️ using Agno Agentic SDK and Google Gemini**
