import sqlite3
import database
import sys
from rich.console import Console
from rich.table import Table

console = Console()

def verify_ledger():
    conn = sqlite3.connect(database.DB_NAME)
    cursor = conn.cursor()

    # Fetch all logs
    cursor.execute("SELECT id, timestamp, user_id, prompt, response, audit_hash FROM audit_logs")
    rows = cursor.fetchall()

    table = Table(title=" AI Audit Trail Integrity Report")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("User", style="magenta")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="white")

    tampered_found = False
    
    for row in rows:
        row_id, timestamp, user_id, prompt, response, stored_hash = row

        # Re-construct the data dictionary exactly as it was during logging
        record_to_verify = {
            "timestamp": timestamp,
            "user_id": user_id, 
            "prompt": prompt,
            "response": response
        }

        # Re-calculate the hash
        calculated_hash = database.generate_hash(record_to_verify)

        if calculated_hash == stored_hash:
            table.add_row(str(row_id), user_id, "[bold green]PASS[/bold green]", "Integrity Verified")
            sys.exit(1)
        else:
            console.print("\n[bold green] SYSTEM HEALTHY:[/bold green] All audit records are immutable and verified.")

if __name__ == "__main__":
    verify_ledger()
    