import re
from code.agents.registry import get_agent
from code.analyzer import Analyzer
from code.config import DEFAULT_CONFIG
from code.tools import list_domains, list_files_in_domain, read_crawled_file

def execute_tool(tool_call):
    match = re.match(r"TOOL_CALL: (\w+)\((.*)\)", tool_call)
    if not match:
        return "Invalid tool call format."
    
    tool_name, args_str = match.groups()
    args = [arg.strip().strip('"').strip("'") for arg in args_str.split(",")] if args_str else []
    
    try:
        if tool_name == "list_domains":
            return list_domains()
        elif tool_name == "list_files_in_domain":
            return list_files_in_domain(args[0]) if args else "Missing domain argument."
        elif tool_name == "read_crawled_file":
            return read_crawled_file(args[0], args[1]) if len(args) >= 2 else "Missing arguments."
        else:
            return f"Unknown tool: {tool_name}"
    except Exception as e:
        return f"Error executing tool {tool_name}: {str(e)}"

def run_engine(io, config=DEFAULT_CONFIG, analyzer=None):
  analyzer = analyzer or Analyzer()

  while True:
    try:
      user_input = io.read_input("> ")
    except EOFError:
      return

    result = analyzer.analyze(user_input, config)
    output = result.content

    if result.kind == "message":
      agent = get_agent(config.provider)
      history = []
      current_input = result.content
      
      while True:
        response = agent.respond(current_input, config, history=history)
        
        if "TOOL_CALL:" in response:
          # Output the "thought" part to the user (strip the tool call line)
          thought = "\n".join([line for line in response.split("\n") if "TOOL_CALL:" not in line]).strip()
          if thought:
            if config.use_stream:
              io.stream_output([thought, "\n"])
              io.write_output()
            else:
              io.write_output(thought)
          
          # Extract the tool call (taking the last one if multiple)
          tool_call = [line for line in response.split("\n") if "TOOL_CALL:" in line][-1]
          tool_result = execute_tool(tool_call)
          
          history.append({"role": "assistant", "content": response})
          history.append({"role": "user", "content": f"Tool Result: {tool_result}"})
          current_input = "Based on the tool result, please continue your response."
        else:
          if config.use_stream:
             io.stream_output([response, "\n"])
             io.write_output()
          else:
             io.write_output(response)
          break
    elif config.use_stream:
      io.stream_output([output, "\n"])
    else:
      io.write_output(output)

    if result.should_exit:
      return

