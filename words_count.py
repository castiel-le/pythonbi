import os
import csv
from collections import defaultdict

# --- ESG Keyword Sets ---
E_KEYWORDS = {"climate", "carbon", "emissions", "renewable", "energy", "waste", "environmental"}
S_KEYWORDS = {"diversity", "inclusion", "safety", "labor", "community", "employees", "human rights"}
G_KEYWORDS = {"board", "ethics", "compliance", "transparency", "audit", "shareholders", "governance"}

TRANSCRIPTS_DIR = 'transcripts'
HUMAN_OUTPUT = 'esg_report_by_company.txt'
MACHINE_OUTPUT = 'esg_data_machine.csv'

def analyze_esg_with_progress():
    grouped_results = defaultdict(list)
    all_flat_results = []
    
    # Get list of subfolders to track progress
    subfolders = [f for f in os.listdir(TRANSCRIPTS_DIR) if os.path.isdir(os.path.join(TRANSCRIPTS_DIR, f))]
    total_folders = len(subfolders)
    
    print(f"--- Starting Analysis of {total_folders} Companies ---")

    # 1. Process Files
    for index, company_name in enumerate(subfolders, 1):
        folder_path = os.path.join(TRANSCRIPTS_DIR, company_name)
        files_in_folder = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        
        for file in files_in_folder:
            file_path = os.path.join(folder_path, file)
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
                print(f"  [!] Error reading {file}: {e}")

        # PROGRESS UPDATE AFTER EACH FOLDER
        print(f"[{index}/{total_folders}] Completed: {company_name} ({len(files_in_folder)} files)")

    # 2. Write Human-Readable Version
    with open(HUMAN_OUTPUT, 'w', encoding='utf-8') as out:
        out.write("ESG ANALYSIS - GROUPED BY COMPANY\n" + "="*60 + "\n\n")
        for company, records in sorted(grouped_results.items()):
            out.write(f"COMPANY: {company}\n{'-'*10}\n")
            header = f"  {'FILENAME':<25} | {'TOTAL':<8} | {'E':<4} | {'S':<4} | {'G':<4}\n"
            out.write(header)
            for r in sorted(records, key=lambda x: x['filename']):
                out.write(f"  {r['filename']:<25} | {r['total']:<8} | {r['E']:<4} | {r['S']:<4} | {r['G']:<4}\n")
            out.write("\n" + "="*60 + "\n\n")

    # 3. Write Machine-Readable Version
    with open(MACHINE_OUTPUT, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['company', 'filename', 'total', 'E', 'S', 'G']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_flat_results)

    # FINAL COMPLETION OUTPUT
    print("\n" + "*"*40)
    print("ANALYSIS COMPLETE!")
    print(f"Total Companies Processed: {len(grouped_results)}")
    print(f"Total Files Analyzed:    {len(all_flat_results)}")
    print(f"Readable Report:        {HUMAN_OUTPUT}")
    print(f"Data File (CSV):        {MACHINE_OUTPUT}")
    print("*"*40)

if __name__ == "__main__":
    analyze_esg_with_progress()