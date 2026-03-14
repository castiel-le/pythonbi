import os
import csv
from collections import defaultdict

# --- ESG Keyword Sets ---
# Thay từ khóa vào đây
E_KEYWORDS = {"climate", "carbon", "emissions", "renewable", "energy", "waste", "environmental"}
S_KEYWORDS = {"diversity", "inclusion", "safety", "labor", "community", "employees", "human rights"}
G_KEYWORDS = {"board", "ethics", "compliance", "transparency", "audit", "shareholders", "governance"}

TRANSCRIPTS_DIR = 'transcripts'
HUMAN_OUTPUT = 'esg_report_by_company.txt'
MACHINE_OUTPUT = 'esg_data.csv'

def analyze_esg_grouped():
    # Store data as: { "AAPL": [data1, data2], "MSFT": [data1, data2] }
    grouped_results = defaultdict(list)
    all_flat_results = [] # For the CSV

    # 1. Process Files and Group by Company (Subfolder)
    for root, _, files in os.walk(TRANSCRIPTS_DIR):
        # The immediate subfolder name is the company name
        company_name = os.path.basename(root)
        
        # Skip the root directory itself if it contains .txt files
        if company_name == TRANSCRIPTS_DIR:
            continue

        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        clean_text = content.replace('.', ' ').replace(',', ' ').replace(';', ' ')
                        words = clean_text.split()
                        
                        total_words = len(words)
                        e_count = sum(words.count(kw) for kw in E_KEYWORDS)
                        s_count = sum(words.count(kw) for kw in S_KEYWORDS)
                        g_count = sum(words.count(kw) for kw in G_KEYWORDS)
                        
                        entry = {
                            "company": company_name,
                            "filename": file,
                            "total": total_words,
                            "E": e_count,
                            "S": s_count,
                            "G": g_count
                        }
                        
                        grouped_results[company_name].append(entry)
                        all_flat_results.append(entry)
                except Exception as e:
                    print(f"Error reading {file}: {e}")

    # 2. Write Human-Readable Version (Grouped)
    with open(HUMAN_OUTPUT, 'w', encoding='utf-8') as out:
        out.write("ESG ANALYSIS - GROUPED BY COMPANY\n")
        out.write("=" * 60 + "\n\n")

        for company, records in sorted(grouped_results.items()):
            out.write(f"COMPANY: {company}\n")
            out.write(f"{'-'*10}\n")
            header = f"  {'FILENAME':<25} | {'TOTAL':<8} | {'E':<4} | {'S':<4} | {'G':<4}"
            out.write(header + "\n")
            
            # Sort records by filename so Q1, Q2, Q3, Q4 appear in order
            for r in sorted(records, key=lambda x: x['filename']):
                line = f"  {r['filename']:<25} | {r['total']:<8} | {r['E']:<4} | {r['S']:<4} | {r['G']:<4}"
                out.write(line + "\n")
            out.write("\n" + "="*60 + "\n\n")

    # 3. Write Machine-Readable Version (CSV remains flat for easy filtering)
    with open(MACHINE_OUTPUT, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['company', 'filename', 'total', 'E', 'S', 'G']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_flat_results)

    print(f"Analysis complete! Checked {len(grouped_results)} companies.")

if __name__ == "__main__":
    analyze_esg_grouped()