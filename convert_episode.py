#!/usr/bin/env python3
"""Generic episode txt → md conversion with paragraph breaks."""

import re
import sys

def convert(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read().strip()

    has_punctuation = text.count('.') > 20

    if has_punctuation:
        # Split on sentence endings followed by uppercase
        lines = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÖŐÚÜŰ])', text)
    else:
        # No punctuation - split on speaker changes and topic transitions
        # Only split on STRONG boundaries to avoid over-fragmentation

        # First pass: split on very clear boundaries
        strong_splits = [
            r'(?<=[a-záéíóöőúüű]) (?=sziasztok\b)',
            r'(?<=[a-záéíóöőúüű]) (?=igen (?:már|sokszor|hát|de|ez|én|nagyon|ö|abszolút))',
            r'(?<=[a-záéíóöőúüű]) (?=na (?:most|mindegy|de)\b)',
            r'(?<=[a-záéíóöőúüű]) (?=szóval (?:hogy|én|itt|ez|hát|innentől))',
            r'(?<=[a-záéíóöőúüű]) (?=egyébként (?:milyen|ez|szerintem|én))',
            r'(?<=[a-záéíóöőúüű]) (?=mindenesetre\b)',
            r'(?<=[a-záéíóöőúüű]) (?=továbbá\b)',
        ]

        chunks = [text]
        for pattern in strong_splits:
            new_chunks = []
            for chunk in chunks:
                parts = re.split(pattern, chunk, flags=re.IGNORECASE)
                new_chunks.extend(parts)
            chunks = new_chunks

        # Second pass: split very long chunks (>800 chars) on medium boundaries
        medium_splits = [
            r'(?<=[a-záéíóöőúüű]) (?=tehát (?:hogy|a|ez|ő|nem|itt|hogyha|igazából))',
            r'(?<=[a-záéíóöőúüű]) (?=hát (?:ez|igen|az|a|persze|mindig|ilyen))',
            r'(?<=[a-záéíóöőúüű]) (?=de (?:hát|hogy|azért|ez|itt|ha|alapvetően|visszakanyarodok|érdemes|ami))',
            r'(?<=[a-záéíóöőúüű]) (?=és (?:ugye|aztán|akkor|ez|hogy|hogyha|innentől|ő|hát))',
            r'(?<=[a-záéíóöőúüű]) (?=viszont (?:ahogy|azt))',
            r'(?<=[a-záéíóöőúüű]) (?=persze (?:ez|szeretnék))',
            r'(?<=[a-záéíóöőúüű]) (?=aztán (?:az|pedig|kisösszeg|kialakul))',
            r'(?<=[a-záéíóöőúüű]) (?=én (?:azt |nem |szeret|nagyon|számom|ezért|is |a |mindig))',
        ]

        final_chunks = []
        for chunk in chunks:
            if len(chunk) > 800:
                sub = [chunk]
                for pattern in medium_splits:
                    new_sub = []
                    for s in sub:
                        if len(s) > 800:
                            parts = re.split(pattern, s, flags=re.IGNORECASE)
                            new_sub.extend(parts)
                        else:
                            new_sub.append(s)
                    sub = new_sub
                final_chunks.extend(sub)
            else:
                final_chunks.append(chunk)

        lines = [l.strip() for l in final_chunks if l.strip()]

    # Apply standard fixes
    result = []
    for line in lines:
        # Capitalize first letter
        if line and line[0].islower():
            line = line[0].upper() + line[1:]

        # HUSZONEGY nagybetűvel
        line = re.sub(r'\b21\b(?=\s+(?:bitcoin|podcast|csoport|adás))', 'HUSZONEGY', line, flags=re.IGNORECASE)
        line = re.sub(r'\ba 21\b(?=\s)', 'a HUSZONEGY', line)

        # Hotel nevek
        line = re.sub(r'hotelatlant\w*', 'Hotel Atlantis', line, flags=re.IGNORECASE)
        line = re.sub(r'hotel\s+atlant\w*', 'Hotel Atlantis', line, flags=re.IGNORECASE)
        line = re.sub(r'hotel\s*aur[oó]r\w*', 'Hotel Aurora', line, flags=re.IGNORECASE)

        # Christine Lagarde
        line = re.sub(r'kristin lagard', 'Christine Lagarde', line, flags=re.IGNORECASE)

        # CBDC nagybetűvel
        line = re.sub(r'\bcbdc\b', 'CBDC', line, flags=re.IGNORECASE)

        # fiat not fiát
        line = re.sub(r'\bfiát\b', 'fiat', line)
        line = re.sub(r'\bfiát\b', 'fiat', line, flags=re.IGNORECASE)

        # Friedrich von Hayek
        line = re.sub(r'friedrich (?:augustus )?von ha[ey]k', 'Friedrich von Hayek', line, flags=re.IGNORECASE)
        line = re.sub(r'von ha[ey]k', 'von Hayek', line, flags=re.IGNORECASE)

        # Michael Saylor
        line = re.sub(r'\bsailor\b', 'Saylor', line, flags=re.IGNORECASE)
        line = re.sub(r'\bsailer\b', 'Saylor', line, flags=re.IGNORECASE)

        # Saifedean Ammous
        line = re.sub(r'scifeden\b', 'Saifedean', line, flags=re.IGNORECASE)
        line = re.sub(r'saifedean aous', 'Saifedean Ammous', line, flags=re.IGNORECASE)

        # George Orwell
        line = re.sub(r'george orvelt', 'George Orwellt', line, flags=re.IGNORECASE)

        # Larry Fink
        line = re.sub(r'larifink', 'Larry Fink', line, flags=re.IGNORECASE)
        line = re.sub(r'larry fink', 'Larry Fink', line, flags=re.IGNORECASE)

        # Bitcoin nagy B
        line = re.sub(r'\bbitcoin\b', 'Bitcoin', line)

        # Don't trust, verify
        line = re.sub(r'dontrust verify', "don't trust, verify", line, flags=re.IGNORECASE)

        result.append(line)

    # Write with paragraph breaks
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, line in enumerate(result):
            f.write(line + '\n')
            if i < len(result) - 1:
                f.write('\n')

    print(f"Kész! {len(result)} bekezdés → {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 convert_episode.py INPUT OUTPUT")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
