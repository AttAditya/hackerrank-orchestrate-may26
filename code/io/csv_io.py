import csv
import json
from pathlib import Path
from code.io.base import BaseIO

class CsvIO(BaseIO):
    def __init__(self, input_path="support_tickets/support_tickets.csv", output_path="support_tickets/output.csv"):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.tickets = []
        self.results = []
        self.current_ticket_index = 0
        self.current_output = []

        self._load_tickets()

    def _load_tickets(self):
        if not self.input_path.exists():
            raise FileNotFoundError(f"Input CSV not found at {self.input_path}")
        
        with open(self.input_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.tickets = list(reader)

    def read_input(self, prompt=""):
        if self.current_ticket_index < len(self.tickets):
            ticket = self.tickets[self.current_ticket_index]
            self.current_ticket_index += 1
            
            # Construct a prompt using the ticket details
            issue = ticket.get("Issue", "No issue provided")
            subject = ticket.get("Subject", "No subject provided")
            company = ticket.get("Company", "Unknown")
            
            prompt_text = f"TICKET ENTRY:\\nCompany: {company}\\nSubject: {subject}\\nIssue: {issue}"
            return prompt_text
        
        return "/exit"

    def write_output(self, message="", *, end="\n"):
        self.current_output.append(message)
        return message

    def stream_output(self, chunks):
        for chunk in chunks:
            self.current_output.append(chunk)

    def save_current_result(self):
        # Join the collected output
        raw_response = "".join(self.current_output).strip()
        
        # Attempt to extract JSON from the response
        try:
            # Find the first '{' and last '}' to handle cases where the agent adds conversational filler
            start = raw_response.find('{')
            end = raw_response.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = raw_response[start:end]
                data = json.loads(json_str)
            else:
                # Fallback if no JSON found
                data = {
                    "status": "escalated",
                    "product_area": "Unknown",
                    "response": raw_response,
                    "justification": "Agent failed to produce structured JSON output.",
                    "request_type": "invalid"
                }
        except Exception:
            data = {
                "status": "escalated",
                "product_area": "Unknown",
                "response": raw_response,
                "justification": "Failed to parse JSON output.",
                "request_type": "invalid"
            }

        self.results.append(data)
        self.current_output = []

    def write_results_to_csv(self):
        if not self.tickets:
            return

        # Required headers as per problem_statement.md
        header = ["status", "product_area", "response", "justification", "request_type"]
        
        with open(self.output_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            
            for i in range(len(self.tickets)):
                res = self.results[i] if i < len(self.results) else {}
                writer.writerow([
                    res.get("status", "escalated"),
                    res.get("product_area", "Unknown"),
                    res.get("response", ""),
                    res.get("justification", ""),
                    res.get("request_type", "invalid")
                ])
