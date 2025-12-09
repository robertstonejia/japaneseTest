#!/usr/bin/env python3
"""
Add multi-language translations to vocabulary JSON files
単語JSONファイルに多言語翻訳を追加

This script uses the googletrans library to automatically translate
English meanings to other languages.

Install required library:
    pip install googletrans==4.0.0-rc1
"""

import json
import os
import time
from googletrans import Translator

# Language codes
LANGUAGES = {
    'zh-cn': '中文',      # Chinese (Simplified)
    'ne': 'नेपाली',       # Nepali
    'vi': 'Tiếng Việt',   # Vietnamese
    'my': 'မြန်မာ',       # Myanmar (Burmese)
    'ko': '한국어',        # Korean
    'ar': 'العربية',      # Arabic
    'es': 'Español',      # Spanish
    'de': 'Deutsch',      # German
    'fr': 'Français'      # French
}

def translate_vocabulary_file(input_file, output_file=None):
    """
    Translate a vocabulary JSON file to multiple languages

    Args:
        input_file: Path to input JSON file
        output_file: Path to output JSON file (optional, defaults to input_file)
    """
    if output_file is None:
        output_file = input_file

    print(f"Reading {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        vocabulary = json.load(f)

    translator = Translator()
    total = len(vocabulary)

    print(f"Translating {total} words to {len(LANGUAGES)} languages...")

    for idx, word_entry in enumerate(vocabulary, 1):
        # Skip if already has meanings object
        if 'meanings' in word_entry and isinstance(word_entry['meanings'], dict):
            print(f"[{idx}/{total}] Skipping '{word_entry['word']}' (already translated)")
            continue

        # Get English meaning
        english_meaning = word_entry.get('meaning', '')

        if not english_meaning:
            print(f"[{idx}/{total}] Skipping '{word_entry['word']}' (no meaning)")
            continue

        print(f"[{idx}/{total}] Translating '{word_entry['word']}' ({english_meaning})...")

        # Create meanings object
        meanings = {'en': english_meaning}

        # Translate to each language
        for lang_code, lang_name in LANGUAGES.items():
            try:
                # Translate
                translation = translator.translate(english_meaning, dest=lang_code)
                meanings[lang_code.split('-')[0]] = translation.text

                print(f"  → {lang_name}: {translation.text}")

                # Add delay to avoid rate limiting
                time.sleep(0.5)

            except Exception as e:
                print(f"  ✗ Error translating to {lang_name}: {str(e)}")
                meanings[lang_code.split('-')[0]] = english_meaning  # Fallback to English

        # Update word entry
        word_entry['meanings'] = meanings
        # Keep old 'meaning' field for backwards compatibility
        # word_entry['meaning'] = english_meaning

    # Write updated vocabulary
    print(f"\nWriting to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(vocabulary, f, ensure_ascii=False, indent=2)

    print(f"✓ Complete! Updated {output_file}")

def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python add_translations.py <json_file> [output_file]")
        print("\nExample:")
        print("  python add_translations.py vocabulary/N5.json")
        print("  python add_translations.py vocabulary/N5.json vocabulary/N5_translated.json")
        print("\nOr translate all files:")
        print("  python add_translations.py all")
        return

    if sys.argv[1] == 'all':
        # Translate all vocabulary files
        vocab_dir = 'vocabulary'
        levels = ['N5', 'N4', 'N3', 'N2', 'N1']

        for level in levels:
            input_file = os.path.join(vocab_dir, f'{level}.json')
            if os.path.exists(input_file):
                print(f"\n{'='*60}")
                print(f"Processing {level}")
                print('='*60)
                translate_vocabulary_file(input_file)
            else:
                print(f"Skipping {level}: file not found")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        translate_vocabulary_file(input_file, output_file)

if __name__ == '__main__':
    main()
