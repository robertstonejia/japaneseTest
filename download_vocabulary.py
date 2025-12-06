#!/usr/bin/env python3
"""
Download JLPT vocabulary from GitHub and convert to JSON format
GitHubからJLPT単語リストをダウンロードしてJSON形式に変換
"""

import requests
import csv
import json
import io

# GitHub repository raw file URLs
GITHUB_BASE_URL = "https://raw.githubusercontent.com/elzup/jlpt-word-list/master/src/"

LEVELS = {
    'N5': 'n5.csv',
    'N4': 'n4.csv',
    'N3': 'n3.csv',
    'N2': 'n2.csv',
    'N1': 'n1.csv'
}

def download_and_convert(level, csv_filename):
    """
    Download CSV from GitHub and convert to JSON

    Args:
        level: JLPT level (N5, N4, N3, N2, N1)
        csv_filename: Name of CSV file on GitHub
    """
    url = GITHUB_BASE_URL + csv_filename
    output_file = f"vocabulary/{level}.json"

    print(f"Downloading {level} vocabulary from GitHub...")

    try:
        # Download CSV file
        response = requests.get(url)
        response.raise_for_status()

        # Parse CSV
        csv_content = response.content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(csv_content))

        vocabulary = []
        for row in csv_reader:
            # The CSV has these columns: expression, reading, meaning
            # We need to map them to our format: word, reading, meaning

            # Get the word (expression)
            word = row.get('expression', '').strip()
            if not word:
                continue

            # Get the reading
            reading = row.get('reading', '').strip()
            if not reading:
                reading = word  # Use word itself if no reading provided

            # Get the meaning
            meaning = row.get('meaning', '').strip()
            if not meaning:
                continue

            vocabulary.append({
                'word': word,
                'reading': reading,
                'meaning': meaning
            })

        # Write to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(vocabulary, f, ensure_ascii=False, indent=2)

        print(f"[OK] {level}: {len(vocabulary)} words saved to {output_file}")
        return len(vocabulary)

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error downloading {level}: {str(e)}")
        return 0
    except Exception as e:
        print(f"[ERROR] Error processing {level}: {str(e)}")
        return 0

def main():
    print("=" * 60)
    print("JLPT Vocabulary Downloader")
    print("=" * 60)
    print()
    print("Downloading vocabulary from GitHub repository:")
    print("https://github.com/elzup/jlpt-word-list")
    print()

    total_words = 0

    for level, csv_file in LEVELS.items():
        count = download_and_convert(level, csv_file)
        total_words += count
        print()

    print("=" * 60)
    print(f"Complete! Total: {total_words} words downloaded")
    print("=" * 60)
    print()
    print("Note: Refresh your browser (F5) to see the new vocabulary!")

if __name__ == '__main__':
    main()
