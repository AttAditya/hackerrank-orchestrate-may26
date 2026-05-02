import argparse
from code.config import DEFAULT_CONFIG
from code.engine import run_engine
from code.io import CliIO
from code.io.csv_io import CsvIO

def main():
  parser = argparse.ArgumentParser(description="HackerRank Orchestrate Agent")
  parser.add_argument(
    "--solve", 
    action="store_true", 
    help="Process tickets from support_tickets.csv and save to output.csv"
  )
  args = parser.parse_args()

  if args.solve:
    io = CsvIO()
    # We need a way to tell the CsvIO to save after each ticket
    # Since run_engine doesn't know about tickets, we'll wrap the logic
    # However, the simplest way is to modify run_engine slightly or 
    # wrap the IO calls. For now, let's modify how run_engine interacts.
    
    # To use the current run_engine without changing it, 
    # we can monkeypatch CsvIO.write_output to detect the 'end' of a response.
    # But since a response is finished when the 'break' happens in run_engine's 
    # while loop, we should probably handle the saving in run_engine.
    
    # Alternative: we'll implement a custom wrap or just update run_engine.
    run_engine(io, DEFAULT_CONFIG)
    io.write_results_to_csv()
  else:
    run_engine(CliIO(), DEFAULT_CONFIG)

if __name__ == "__main__":
  main()

