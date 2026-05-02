# Support Ticket Resolution Agent

This agent is designed to resolve real support tickets by utilizing a knowledge base of crawled documentation from relevant companies.

## Features
- **Automated Ticket Processing**: Capable of reading tickets from `support_tickets/support_tickets.csv` and writing resolutions to `support_tickets/output.csv`.
- **RAG Capabilities**: Uses an autonomous tool-calling loop to explore crawled documentation stored in the `data/` directory.
- **Configurable Persona**: Professional support agent persona with persistent configuration.
- **Provider Flexibility**: Supports multiple LLM providers (including Ollama).

## Installation & Setup
1. **Environment**: Ensure you have Python 3.10+ installed.
2. **Dependencies**: The agent uses standard libraries (`json`, `csv`, `urllib`, `pathlib`).
3. **LLM Provider**: 
   - If using Ollama, ensure the Ollama server is running locally (`http://localhost:11434`).
   - Configure the desired model via the `/model` command in interactive mode.
4. **Knowledge Base**: The agent expects crawled data to be present in the `data/` folder (organized by company name).

## Usage

## Usage

### 1. Automated Solving (Submission Mode)
To process all tickets in the support CSV and generate the required 5-column output file:
```bash
python3 -m code --solve
```
This will:
- Read tickets from `support_tickets/support_tickets.csv`.
- Use the agent's tool-calling capabilities to find answers in `data/`.
- Generate a structured response containing `status`, `product_area`, `response`, `justification`, and `request_type`.
- Save these resolutions to `support_tickets/output.csv`.

### 2. Interactive Mode (Testing)
To chat with the agent and test its capabilities:
```bash
python3 -m code
```
In interactive mode, you can use:
- `/model <model_name>`: Change the LLM model.
- `/provider <provider_name>`: Change the provider.
- `/config use <path>`: Change the configuration save location.
- `/exit`: Exit the application.

## Project Structure
- `code/`: Main application logic.
- `data/`: Cached knowledge base documentation.
- `support_tickets/`: Input and output CSV files for evaluations.
- `saves/`: Persistent configuration and session data.
