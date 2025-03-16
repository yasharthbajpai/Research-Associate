# Research Associate

A Python-based research tool that leverages Perplexity AI, web search, and Wikipedia to generate comprehensive research summaries on user-specified topics.

## Overview

Research Associate is an intelligent assistant that combines multiple data sources to create well-structured research summaries. The application uses the Perplexity AI Sonar Pro model to process information gathered from web searches and Wikipedia, delivering organized research results saved as text files.

## Features

- **AI-Powered Research**: Utilizes Perplexity AI's Sonar Pro model for intelligent summary generation
- **Multiple Data Sources**: Integrates DuckDuckGo web search and Wikipedia for comprehensive information gathering
- **Structured Output**: Presents research in a well-organized format with topic, summary, sources, and tools used
- **Progress Tracking**: Provides detailed status updates throughout the research process
- **Error Handling**: Implements robust fallback mechanisms for reliability
- **Local Storage**: Saves all research results as text files for future reference

## Project Structure

```
RESEARCH_ASSOCIATE/
├── __pycache__/
├── .env                  # Environment variables (API keys)
├── Include/
├── Lib/
├── Scripts/
├── desktop.ini
├── pyvenv.cfg
├── results/              # Directory for saved research results
│   ├── desktop.ini
│   ├── Narendra Modi.txt
│   ├── Raspberry.txt
│   ├── raw_Narendra Modi.txt
│   └── raw_Raspberry.txt
├── .gitignore
├── main.py               # Main application file
├── requirements.txt      # Project dependencies
├── tools.py              # Tool definitions for search and saving
```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/research-associate.git
   cd research-associate
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your Perplexity API key:
   ```
   PPLX_API_KEY=your_api_key_here
   ```

## Usage

Run the main script:
```bash
python main.py
```

When prompted, enter a research topic. The Research Associate will:
1. Search the web for relevant information
2. Query Wikipedia for additional content
3. Generate a comprehensive research summary
4. Save the results to a text file in the `results` directory

## Demo

Watch the demo video: [Research Associate Demo](https://drive.google.com/file/d/1hBrBrNKlVpLzCLnnJBNk0gXAEGTde6Pb/view?usp=sharing)

## Example Output

```
[14:30:25] Initializing research assistant...
[14:30:25] Research will be saved to: results/Artificial Intelligence.txt
[14:30:25] Connecting to Perplexity AI...
[14:30:26] Searching the web for information...
[14:30:28] Web search completed successfully
[14:30:28] Querying Wikipedia...
[14:30:30] Wikipedia query completed successfully
[14:30:30] Data sources combined
[14:30:30] Creating structured output model...
[14:30:30] Creating research prompt...
[14:30:30] Prompt formatted successfully
[14:30:30] Generating research summary with AI...
[14:30:35] Research summary generated successfully
[14:30:35] Saving research to results/Artificial Intelligence.txt...
[14:30:35] Research successfully saved to results/Artificial Intelligence.txt

=================================================
--- Research Results ---
=================================================
Topic: Artificial Intelligence

Summary: Artificial Intelligence (AI) refers to computer systems designed to perform tasks that typically require human intelligence...

Sources: Web Search, Wikipedia

Tools Used: search, wikipedia

Research saved to: results/Artificial Intelligence.txt
```

## Dependencies

- python-dotenv==1.0.1
- langchain-community==0.3.19
- langchain-core==0.3.45
- openai
- langchain
- wikipedia
- langchain-openai
- langchain-anthropic
- pydantic
- duckduckgo-search

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT

---

© 2025 Yasharth Bajpai  
All rights reserved

