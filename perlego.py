# -*- coding: utf-8 -*-
print("I am Perlego the Sentinel, awakening...")

import fitz  # PyMuPDF
import os  # Add at the top of file if it's not there already
import json  # Add at the top of file if needed

def check_pdf_legibility(file_path):
    try:
        with fitz.open(file_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text.strip() if text.strip() else None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def extract_proof_snippet(text, max_chars=100):
    if not text:
        return None

    # Try to find the first sentence (ending with period)
    sentence_end = text.find('.') + 1
    if 0 < sentence_end <= max_chars:
        return text[:sentence_end].strip()
    
    # If no good sentence found, fall back to first characters
    return text[:max_chars].strip()

import os  # Add at the top of file if it's not there already

def summarise_result(file_path, max_chars=100):
    filename = os.path.basename(file_path)
    text = check_pdf_legibility(file_path)
    word_count = len(text.split()) if text else 0

    lines = text.splitlines() if text else []
    line_count = len(lines)
    avg_line_length = (sum(len(line) for line in lines) / line_count) if line_count > 0 else 0

    # Basic gibberish detection: lines with no alphabetical characters
    suspicious_lines = [line for line in lines if not any(char.isalpha() for char in line)]
    gibberish_ratio = len(suspicious_lines) / line_count if line_count > 0 else 0

    if avg_line_length < 25 or gibberish_ratio > 0.5:
        layout_flag = "Fragmented or gibberish layout detected. Use with caution."
    else:
        layout_flag = None

    # Punctuation ratio: total punctuation marks per word
    punctuation_marks = [".", ",", ";", ":", "!", "?", "—", "-", "(", ")"]
    punctuation_count = sum(text.count(p) for p in punctuation_marks) if text else 0
    punctuation_ratio = punctuation_count / word_count if word_count > 0 else 0

    # Detect presence of common section headers
    expected_headers = ["introduction", "background", "methods", "results", "discussion", "conclusion", "references"]
    lower_text = text.lower() if text else ""
    found_headers = [header for header in expected_headers if header in lower_text]
    has_section_headers = len(found_headers) >= 2  # flexible threshold

    # Determine structure trust score
    structure_notes = []

    if punctuation_ratio < 0.02:
        structure_notes.append("Very low punctuation ratio")
    if not has_section_headers:
        structure_notes.append("Missing expected section headers")
    if avg_line_length < 25:
        structure_notes.append("Short average line length")

    if structure_notes:
        structure_trust = "low"
    elif punctuation_ratio < 0.05 or avg_line_length < 40:
        structure_trust = "medium"
    else:
        structure_trust = "high"



    if text:
        snippet = extract_proof_snippet(text, max_chars)

        # Detect suspicious prompt-like phrases
        suspicious_phrases = [
            "you are an ai",
            "you are a language model",
            "ignore previous instructions",
            "summarise the following",
            "act as an assistant",
            "please explain the text",
            "rewrite this passage",
            "answer as helpfully as possible"
        ]

        lower_text = text.lower()
        found_prompts = [phrase for phrase in suspicious_phrases if phrase in lower_text]

        return {
            "filename": filename,
            "readable": True,
            "snippet": snippet,
            "note": f"{word_count} words extracted",
            "line_count": line_count,
            "avg_line_length": round(avg_line_length, 2),
            "layout_warning": layout_flag,
            "structure_trust": structure_trust,
            "structure_notes": "; ".join(structure_notes) if structure_notes else None,
            "prompt_warning": "Possible embedded prompt-like instructions detected." if found_prompts else None,
            "prompt_snippet": found_prompts[0] if found_prompts else None,
        }
    else:
        return {
            "filename": filename,
            "readable": False,
            "snippet": None,
            "note": "No extractable text detected. File may be image-only or corrupted.",
            "line_count": 0,
            "avg_line_length": 0,
            "layout_warning": "Unreadable document."
        }

import csv

def analyse_folder(folder_path, output_csv="perlego_summary.csv", max_chars=100):
    results = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            result = summarise_result(file_path, max_chars)
            results.append(result)

    # Save results to CSV
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = list(results[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f" Perlego has completed his Trial by File. Results saved to: {output_csv}")


if __name__ == "__main__":
    folder_to_test = "test_scrolls"  # Or full path if needed
    analyse_folder(folder_to_test)
    print("Batch scan complete.")

    print("Reached the test runner.")
