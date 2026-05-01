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

    if config.use_stream:
      io.stream_output([result.content, "\n"])
    else:
      io.write_output(result.content)

    if result.should_exit:
      return

