from code.agents.registry import get_agent
from code.analyzer import Analyzer
from code.config import DEFAULT_CONFIG

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

      if config.use_stream:
        io.stream_output(agent.stream_respond(result.content, config))
        io.write_output()
      else:
        io.write_output(agent.respond(result.content, config))
    elif config.use_stream:
      io.stream_output([output, "\n"])
    else:
      io.write_output(output)

    if result.should_exit:
      return

