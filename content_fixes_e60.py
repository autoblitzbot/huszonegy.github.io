#!/usr/bin/env python3
"""
E60 transcript content fixes — tartalmi javítások és bekezdéstörések.

Specifically handles E60 of the HUSZONEGY podcast:
- Paragraph breaks (the md file is one giant line)
- Name corrections (speech-to-text garbled names)
- Technical term fixes
- Place name standardization
- Garbled word corrections
- Word deduplication

Usage:
    python3 content_fixes_e60.py input.md -o output.md
    python3 content_fixes_e60.py input.md --inplace
"""

import argparse
import re
import sys


# ──────────────────────────────────────────────────────────
# 1. Name corrections
# ──────────────────────────────────────────────────────────
NAME_FIXES = [
    # Speaker names
    ("Artivval", "Árpival"),
    ("Karóval", "Karóval"),  # keeping as-is, seems intentional

    # Public figures
    ("Peter Shiff", "Peter Schiff"),
    ("Petershiff", "Peter Schiff"),
    ("Lagard", "Lagarde"),
    ("Naib Bukele", "Nayib Bukele"),
    ("Bookelre", "Bukelére"),
    ("Ludwig von Misses", "Ludwig von Mises"),
    ("André Kosztolányi", "André Kostolany"),
    ("Antoni Pompliano", "Anthony Pompliano"),
    ("Sveckytől", "Svetskitől"),

    # Bitcoin figures
    ("SFID könyveit", "Saifedean könyveit"),
    ("Parker Lois", "Parker Lewis"),
    ("Vangu Guardot", "Vanguardot"),
    ("Vangu Guard", "Vanguard"),
    ("Max Skyer", "Max Keiser"),
    ("Micro Strategy", "MicroStrategy"),

    # Historical/cultural
    ("Szuncu", "Szun-Ce"),
    ("Gandi", "Gandhi"),
]

# ──────────────────────────────────────────────────────────
# 2. Technical term fixes
# ──────────────────────────────────────────────────────────
TERM_FIXES = [
    # Psychology terms
    ("tömegpsichológia", "tömegpszichológia"),
    ("tömegpsichológiai", "tömegpszichológiai"),
    ("tömegpsichológiáról", "tömegpszichológiáról"),
    ("praxzeológia", "praxeológia"),
    ("status qu torzítás", "status quo torzítás"),
    ("ellentmódásos", "ellentmondásos"),

    # Economics/finance
    ("inflációlló", "inflációálló"),
    ("cenzórázhatatlan", "cenzúrázhatatlan"),
    ("Fortnx", "Fort Knox"),
    ("Chicago Mercenti Exchange", "Chicago Mercantile Exchange"),
    ("fractional reserve", "fractional reserve"),  # already correct

    # Crypto/Bitcoin terms
    ("cyfer punk", "cypherpunk"),
    ("multisziges", "multisig-es"),
    ("custodialt", "custodiant"),
    ("custodybe", "custody-be"),
    ("custodalje", "custodian-je"),
    ("Castadal", "custodian"),
    ("coach managedment", "key management"),
    ("korfejlesztők", "core fejlesztők"),
    ("hitmenek", "hitman-ek"),
    ("UTXON-on", "UTXO-n"),

    # Garbled words
    ("oszcjat", "Oscar-t"),
    ("slajomat", "diámat"),
    ("slajot", "diát"),
    ("makas", "makacs"),
    ("elbáb játékozott", "elbábjátékozott"),
]

# ──────────────────────────────────────────────────────────
# 3. Regex-based fixes
# ──────────────────────────────────────────────────────────
REGEX_FIXES = [
    # Sailor → Saylor (but not in other words)
    (r'\bSailor\b', 'Saylor'),

    # Mizes → Mises (standalone)
    (r'\bMizes\b', 'Mises'),

    # FAD → FUD (the speaker means FUD but speech-to-text writes FAD)
    # Be careful: "FAD" standalone or in context
    (r'\bFAD\b', 'FUD'),
    (r'\bFADRA\b', 'FUD-ra'),
    (r'\bfadot\b', 'FUD-ot'),
    (r'\bfad\b(?!\w)', 'FUD'),

    # FOMT → FOMO
    (r'\bFOMT\b', 'FOMO'),
    (r'\bFOMORA\b', 'FOMO-ra'),
    (r'\bhomóval\b', 'FOMO-val'),
    (r'\bfomó\b', 'FOMO'),

    # LTF → ETF (speech-to-text error)
    (r'\bLTF\b', 'ETF'),
    (r'\bLTF-ekkel\b', 'ETF-ekkel'),

    # UTX-on → UTXO-n
    (r'\bUTX-on\b', 'UTXO-n'),

    # CBD → CBDC, CVDC → CBDC
    (r'\bCBD\b(?!C)', 'CBDC'),
    (r'\bCVDC\b', 'CBDC'),
    (r'\bCBD-nek\b', 'CBDC-nek'),

    # MiCA consistency
    (r'\bMika\b(?!\s+vagy)', 'MiCA'),
    (r'\bMica\b', 'MiCA'),

    # El Salvador variants normalization
    (r'\bElszágador\b', 'El Salvador'),
    (r'\bEl Salzalvador\b', 'El Salvador'),
    (r'\belszalgadóri\b', 'salvadori'),
    (r'\belszárvadi\b', 'salvadori'),
    (r'\belszárvadori\b', 'salvadori'),
    (r'\belszalvadorba\b', 'El Salvadorba'),
    (r'\belszarvadóban\b', 'El Salvadorban'),
    (r'\belszálladolnak\b', 'El Salvadornak'),
    (r'\bElszalvador\b', 'El Salvador'),
    (r'\bElszárvador\b', 'El Salvador'),
    (r'\bElszágdor\b', 'El Salvador'),
    (r'\bEl Salvador\b', 'El Salvador'),  # normalize capitalization

    # tőzsde
    (r'\btölz\b', 'tőzsde'),

    # pszichológiai műveletek
    (r'\bpszichopok\b', 'psziop-ok'),
]


# ──────────────────────────────────────────────────────────
# 4. Duplicate word removal
# ──────────────────────────────────────────────────────────
DUPLICATE_WORDS = [
    "hogy", "a", "az", "és", "ez", "is", "de", "nem", "meg",
    "itt", "ott", "van", "volt", "én", "te", "ő", "mi", "ti",
    "már", "még", "majd", "csak", "most", "hát", "na", "ugye",
    "ilyen", "olyan", "akkor", "tehát", "mert", "vagy", "ha",
    "ezt", "azt", "egy", "két", "három", "más", "minden",
    "persze", "szóval", "amúgy", "egyébként", "nyilván",
    "mondjuk", "gondolom", "tudom", "tudod", "nagyon",
    "elég", "igen", "jó", "kell", "mint",
]


def remove_duplicate_words(text: str) -> str:
    """Remove adjacent duplicate words (speech stuttering)."""
    for word in DUPLICATE_WORDS:
        pattern = re.compile(
            r'\b(' + re.escape(word) + r')\s+(' + re.escape(word) + r')\b',
            re.IGNORECASE
        )
        text = pattern.sub(r'\1', text)
    return text


# ──────────────────────────────────────────────────────────
# 5. Paragraph breaks
# ──────────────────────────────────────────────────────────

# Markers that indicate a good place for a paragraph break
# (when they appear at the start of a sentence)
PARA_BREAK_MARKERS = [
    "Tehát ",
    "Szóval ",
    "Na most ",
    "Na most, ",
    "Na most én ",
    "Viszont ",
    "Egyébként ",
    "Mindenesetre ",
    "Továbbá ",
    "Ezzel szemben ",
    "De ",
    "Hát ",
    "Miért ",
    "Ugye ",
    "Az ",
    "Ez ",
    "Én ",
    "Van ",
    "Aztán ",
    "Illetve ",
    "Nem ",
    "Persze ",
    "Jó ",
    "Visszanyúlnék ",
    "Figyelj ",
    "Igen ",
    "Érdekes ",
    "Biztos ",
    "Most ",
    "Hogyha ",
    "John ",
    "Negyedik ",
    "Ötödik ",
]

# Known speaker change patterns for E60 discussion section
SPEAKER_CHANGES = [
    "Igen.",
    "Ühüm.",
    "Aha.",
    "Hm.",
    "Persze.",
    "Persze, persze.",
    "Ja.",
    "Na de mindegy.",
    "Nem, hát mer",
    "Ja, ugyanaz",
    "Ja, jól van.",
]


def add_paragraph_breaks(text: str) -> str:
    """Add paragraph breaks to a single-line transcript.

    Strategy:
    - Split into sentences
    - Group into paragraphs based on topic transitions and length
    - Mark speaker changes with – (en dash)
    """
    # First, split into sentences at ". " boundaries
    # But preserve the period with the sentence
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÖŐÚÜŰ\[])', text)

    paragraphs = []
    current_para = []
    current_len = 0

    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue

        # Check if this looks like a speaker change (short affirmation/response)
        is_speaker_change = False
        for marker in SPEAKER_CHANGES:
            if sent.startswith(marker) and len(sent) < 200:
                is_speaker_change = True
                break

        # Check if this starts a new topic
        is_topic_change = False
        for marker in PARA_BREAK_MARKERS:
            if sent.startswith(marker) and current_len > 300:
                is_topic_change = True
                break

        # Force paragraph break if current paragraph is getting long
        is_too_long = current_len > 800

        if (is_speaker_change or is_topic_change or is_too_long) and current_para:
            paragraphs.append(' '.join(current_para))
            current_para = []
            current_len = 0

        current_para.append(sent)
        current_len += len(sent)

    if current_para:
        paragraphs.append(' '.join(current_para))

    return '\n\n'.join(paragraphs)


# ──────────────────────────────────────────────────────────
# Main processing
# ──────────────────────────────────────────────────────────
def apply_content_fixes(text: str) -> str:
    """Apply all content fixes in order."""

    # 1. Name fixes (simple replacements)
    for old, new in NAME_FIXES:
        text = text.replace(old, new)

    # 2. Term fixes (simple replacements)
    for old, new in TERM_FIXES:
        text = text.replace(old, new)

    # 3. Regex-based fixes
    for pattern, replacement in REGEX_FIXES:
        text = re.sub(pattern, replacement, text)

    # 4. Remove duplicate words
    text = remove_duplicate_words(text)

    # 5. Add paragraph breaks
    text = add_paragraph_breaks(text)

    # 6. Capitalize sentence starts after paragraph breaks
    lines = text.split('\n')
    for i in range(len(lines)):
        if lines[i].strip() and (i == 0 or (i > 0 and lines[i-1].strip() == '')):
            lines[i] = re.sub(
                r'^(\s*)([a-záéíóöőúüű])',
                lambda m: m.group(1) + m.group(2).upper(),
                lines[i]
            )
    text = '\n'.join(lines)

    return text


def main():
    parser = argparse.ArgumentParser(
        description="E60 transcript content fixes"
    )
    parser.add_argument("input", help="Input .md file")
    parser.add_argument("--inplace", "-i", action="store_true",
                        help="Overwrite file in-place")
    parser.add_argument("-o", "--output", help="Output file")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        original = f.read()

    result = apply_content_fixes(original)

    if args.inplace:
        with open(args.input, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✓ {args.input} overwritten.", file=sys.stderr)
    elif args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"✓ Output: {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
