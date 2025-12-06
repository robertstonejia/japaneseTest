#!/usr/bin/env python3
"""
Update first 10 words of N5.json with multilingual translations
"""

import json

# Read the sample multilingual data
with open('vocabulary/N5_sample.json', 'r', encoding='utf-8') as f:
    multilingual_words = json.load(f)

# Read the existing N5 vocabulary
with open('vocabulary/N5.json', 'r', encoding='utf-8') as f:
    n5_vocab = json.load(f)

# Create a mapping from word to multilingual data
multilingual_map = {word['word']: word for word in multilingual_words}

# Update matching words
updated_count = 0
for word_entry in n5_vocab:
    if word_entry['word'] in multilingual_map:
        word_entry['meanings'] = multilingual_map[word_entry['word']]['meanings']
        updated_count += 1
        print(f"Updated: {word_entry['word']}")

# Write back
with open('vocabulary/N5.json', 'w', encoding='utf-8') as f:
    json.dump(n5_vocab, f, ensure_ascii=False, indent=2)

print(f"\n✓ Updated {updated_count} words in N5.json")
