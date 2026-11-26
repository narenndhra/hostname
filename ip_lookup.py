
import pandas as pd

# Input files
excel_file = "hosts.xlsx"
ip_file = "ips.txt"

# Read Excel file
df = pd.read_excel(excel_file, dtype=str).fillna("")

# Remove unwanted whitespace
df.columns = df.columns.str.strip()
df["Internal IP"] = df["Internal IP"].str.strip()
df["Hostname"] = df["Hostname"].str.strip()

# Create IP to hostname mapping
ip_mapping = df.groupby("Internal IP")["Hostname"].apply(list).to_dict()

# Read IPs and ignore blank lines, spaces and commas
with open(ip_file, "r", encoding="utf-8-sig") as f:
    ips = f.read().replace(",", " ").split()

# Match IP addresses with hostnames
results = []

for entry in ips:
    # Remove port only for hostname lookup
    ip = entry.split(":")[0]

    hostnames = ip_mapping.get(ip, ["Hostname not found"])

    for hostname in hostnames:
        # Preserve original IP and port in output
        results.append(f"{entry} ({hostname})")

# Display results separated by comma and new line
print(",\n".join(results))
