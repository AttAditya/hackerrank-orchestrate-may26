from code.config import DEFAULT_CONFIG
from code.engine import run_engine
from code.io import CliIO

def main():
  run_engine(CliIO(), DEFAULT_CONFIG)

if __name__ == "__main__":
  main()

