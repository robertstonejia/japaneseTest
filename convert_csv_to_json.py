#!/usr/bin/env python3
"""
CSV to JSON Converter for Japanese Vocabulary
CSVファイルをJSONファイルに変換するツール

Usage:
    python convert_csv_to_json.py input.csv output.json

CSV Format:
    word,reading,meaning
    学生,がくせい,student
    先生,せんせい,teacher
"""

import csv
import json
import sys
import os

def csv_to_json(csv_file, json_file):
    """
    Convert CSV file to JSON format for vocabulary

    Args:
        csv_file: Path to input CSV file
        json_file: Path to output JSON file
    """
    vocabulary = []

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Check if required columns exist
            if not all(col in reader.fieldnames for col in ['word', 'reading', 'meaning']):
                print("❌ Error: CSV must have columns: word, reading, meaning")
                return False

            for row in reader:
                # Skip empty rows
                if not row['word'] or not row['reading'] or not row['meaning']:
                    continue

                vocabulary.append({
                    'word': row['word'].strip(),
                    'reading': row['reading'].strip(),
                    'meaning': row['meaning'].strip()
                })

        # Write to JSON file
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(vocabulary, f, ensure_ascii=False, indent=2)

        print(f"✅ Success! Converted {len(vocabulary)} words")
        print(f"📄 Output: {json_file}")
        return True

    except FileNotFoundError:
        print(f"❌ Error: File not found: {csv_file}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def merge_json_files(json_files, output_file):
    """
    Merge multiple JSON vocabulary files into one

    Args:
        json_files: List of JSON file paths
        output_file: Path to output merged JSON file
    """
    all_vocabulary = []
    seen_words = set()

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                vocabulary = json.load(f)

                for word in vocabulary:
                    # Remove duplicates
                    word_key = word['word']
                    if word_key not in seen_words:
                        all_vocabulary.append(word)
                        seen_words.add(word_key)
        except Exception as e:
            print(f"⚠️ Warning: Could not read {json_file}: {str(e)}")

    # Write merged file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_vocabulary, f, ensure_ascii=False, indent=2)

    print(f"✅ Merged {len(all_vocabulary)} unique words")
    print(f"📄 Output: {output_file}")

def main():
    if len(sys.argv) < 3:
        print("📚 CSV to JSON Converter for Japanese Vocabulary")
        print()
        print("Usage:")
        print("  python convert_csv_to_json.py input.csv output.json")
        print()
        print("CSV Format:")
        print("  word,reading,meaning")
        print("  学生,がくせい,student")
        print("  先生,せんせい,teacher")
        print()
        print("Example:")
        print("  python convert_csv_to_json.py N5_words.csv vocabulary/N5.json")
        sys.exit(1)

    csv_file = sys.argv[1]
    json_file = sys.argv[2]

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(json_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    csv_to_json(csv_file, json_file)

if __name__ == '__main__':
    main()
