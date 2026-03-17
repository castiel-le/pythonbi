import os
import csv
import time
from collections import defaultdict

# --- Environment Keyword Set ---
E_KEYWORDS = {
    "climate", "carbon", "emissions", "renewable", "energy", 
    "waste", "environmental", "sustainability", "net-zero", "green"
}

TRANSCRIPTS_DIR = 'transcripts'
HUMAN_OUTPUT = 'environment_report_readable.txt'
MACHINE_OUTPUT = 'environment_data_machine.csv'

def analyze_environment_raw():
    start_time = time.time()
    grouped_results = defaultdict(list)
    all_flat_results = []
    
    if not os.path.exists(TRANSCRIPTS_DIR):
        print(f"Error: Folder '{TRANSCRIPTS_DIR}' not found.")
        return

    subfolders = [f for f in os.listdir(TRANSCRIPTS_DIR) if os.path.isdir(os.path.join(TRANSCRIPTS_DIR, f))]
    total_folders = len(subfolders)
    
    print(f"--- Starting Raw Environment (E) Count for {total_folders} Companies ---")

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
                    
                    entry = {
                        "company": company_name,
                        "filename": file,
                        "total_words": total_words,
                        "environment_mentions": e_count
                    }
                    grouped_results[company_name].append(entry)
                    all_flat_results.append(entry)
            except Exception as e:
                print(f"  [!] Error reading {file}: {e}")

        print(f"[{index}/{total_folders}] Processed: {company_name}")

    # 1. Write Human-Readable Version
    with open(HUMAN_OUTPUT, 'w', encoding='utf-8') as out:
        out.write("ENVIRONMENTAL (E) COUNT REPORT\n" + "="*55 + "\n\n")
        for company, records in sorted(grouped_results.items()):
            out.write(f"COMPANY: {company}\n{'-'*10}\n")
            header = f"  {'FILENAME':<30} | {'TOTAL WORDS':<12} | {'E-COUNT'}\n"
            out.write(header)
            for r in sorted(records, key=lambda x: x['filename']):
                out.write(f"  {r['filename']:<30} | {r['total_words']:<12} | {r['environment_mentions']}\n")
            out.write("\n" + "="*55 + "\n\n")

    # 2. Write Machine-Readable Version (CSV)
    with open(MACHINE_OUTPUT, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['company', 'filename', 'total_words', 'environment_mentions']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_flat_results)

    # Final Summary
    duration = round(time.time() - start_time, 2)
    print("\n" + "*"*45)
    print("FINISHED ENVIRONMENT COUNT")
    print(f"Time Taken:         {duration} seconds")
    print(f"Companies Checked:  {len(grouped_results)}")
    print(f"Files Processed:    {len(all_flat_results)}")
    print("*"*45)

if __name__ == "__main__":
    analyze_environment_raw()