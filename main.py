import os
import time
import json
import re
from dotenv import load_dotenv
from langchain_community.chat_models import ChatPerplexity
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

def print_status(message):
    """Print a status message with timestamp"""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def extract_json(text):
    """Extract JSON from text, handling various formats"""
    # Try to find JSON between triple backticks
    json_match = re.search(r'``````', text)
    if json_match:
        return json_match.group(1).strip()
    
    # Try to find JSON between single backticks
    json_match = re.search(r'`([\s\S]*?)`', text)
    if json_match:
        return json_match.group(1).strip()
    
    # If no backticks, try to find anything that looks like JSON
    json_match = re.search(r'(\{[\s\S]*\})', text)
    if json_match:
        return json_match.group(1).strip()
    
    # If all else fails, return the original text
    return text

def run_research(query):
    tools_used = []
    sources = []
    
    # Create filename exactly matching the user input
    filename = f"{query}.txt"
    
    # Create results directory path
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        print_status(f"Created results directory: {results_dir}")
    
    # Full path to the file
    file_path = os.path.join(results_dir, filename)
    
    print_status("Initializing research assistant...")
    print_status(f"Research will be saved to: {file_path}")
    
    # Initialize the ChatPerplexity model with your API key
    print_status("Connecting to Perplexity AI...")
    llm = ChatPerplexity(
        model="sonar-pro",
        api_key=os.getenv("PPLX_API_KEY")  
    )
    
    # Use search tool
    print_status("Searching the web for information...")
    try:
        search_results = search_tool.run(query)
        tools_used.append("search")
        sources.append("Web Search")
        print_status("Web search completed successfully")
    except Exception as e:
        search_results = f"Error with search: {str(e)}"
        print_status(f"Error during web search: {str(e)}")
    
    # Use wiki tool
    print_status("Querying Wikipedia...")
    try:
        wiki_results = wiki_tool.run(query)
        tools_used.append("wikipedia")
        sources.append("Wikipedia")
        print_status("Wikipedia query completed successfully")
    except Exception as e:
        wiki_results = f"Error with Wikipedia: {str(e)}"
        print_status(f"Error during Wikipedia query: {str(e)}")
    
    # Combine results for the LLM
    combined_results = f"Search results: {search_results}\n\nWikipedia results: {wiki_results}"
    print_status("Data sources combined")
    
    # Try the structured output approach directly
    print_status("Creating structured output model...")
    structured_llm = llm.with_structured_output(ResearchResponse)
    
    # Create prompt with improved JSON formatting instructions
    print_status("Creating research prompt...")
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        You are a research assistant that will help generate a research paper.
        Based on the provided search results and Wikipedia information, create a comprehensive research summary.
        """),
        ("human", "Research topic: {query}\n\nReference materials:\n{combined_results}")
    ])
    
    # Format the prompt
    formatted_prompt = prompt.format(
        query=query,
        combined_results=combined_results
    )
    print_status("Prompt formatted successfully")
    
    # Generate the research response using structured output
    print_status("Generating research summary with AI...")
    try:
        response = structured_llm.invoke(formatted_prompt)
        print_status("Research summary generated successfully")
    except Exception as e:
        print_status(f"Error with structured output: {str(e)}")
        print_status("Falling back to manual parsing...")
        
        # Fallback to regular output and manual parsing
        regular_response = llm.invoke(formatted_prompt)
        print_status("Received regular response, attempting to parse...")
        
        # Save the raw response for debugging
        raw_file_path = os.path.join(results_dir, f"raw_{filename}")
        with open(raw_file_path, "w", encoding="utf-8") as f:
            f.write(regular_response.content)
        print_status(f"Raw response saved to {raw_file_path}")
        
        # Create a minimal valid response
        response = ResearchResponse(
            topic=query,
            summary=f"Please see the raw output in {raw_file_path}. The AI generated a response but it couldn't be parsed as structured data.",
            sources=sources,
            tools_used=tools_used
        )
    
    # Update the response with actual tools used
    response.tools_used = tools_used
    if not set(sources).issubset(set(response.sources)):
        for source in sources:
            if source not in response.sources:
                response.sources.append(source)
    
    # Save the results to a file with the exact query as the filename
    print_status(f"Saving research to {file_path}...")
    try:
        save_to_txt(str(response), file_path)
        print_status(f"Research successfully saved to {file_path}")
    except Exception as e:
        print_status(f"Error saving: {str(e)}")
    
    return response, file_path

def save_to_txt(data, file_path):
    """Save research data to a text file at the specified path"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {file_path}"

# Get the query from the user
query = input("What can I help you research? ")
print("\n" + "="*50)
print(f"Starting research on: {query}")
print("="*50 + "\n")

# Run the research process
try:
    result, saved_file_path = run_research(query)
    print("\n" + "="*50)
    print("--- Research Results ---")
    print("="*50)
    print(f"Topic: {result.topic}")
    print(f"\nSummary: {result.summary}")
    print(f"\nSources: {', '.join(result.sources)}")
    print(f"\nTools Used: {', '.join(result.tools_used)}")
    print(f"\nResearch saved to: {saved_file_path}")
except Exception as e:
    print("\n" + "="*50)
    print(f"Error during research: {str(e)}")
    import traceback
    traceback.print_exc()
    print("="*50)
