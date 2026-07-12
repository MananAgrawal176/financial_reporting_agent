from main import research_stock
import os

a1 = ["ASIANPAINT", "AXISBANK"]
a2 = ["Asian_Paints_report.txt", "Axis_Bank_report.txt"]

# Folder where reports will be stored
output_folder = "demo_reports_generated"

# Create folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

for ticker, filename in zip(a1, a2):
    brief = research_stock(ticker, stream=False)
    with open(os.path.join(output_folder, filename), "w") as f:
        f.write(brief)
    print(f"Report for {ticker} saved to {os.path.join(output_folder, filename)}")
