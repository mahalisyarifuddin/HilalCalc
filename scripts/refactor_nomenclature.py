import re
import sys

replacements = {
    r'\but\b': 'universalTime',
    r'\bjd\b': 'julianDate',
    r'\balt\b': 'altitude',
    r'\belong\b': 'elongation',
    r'\bconj\b': 'conjunction',
    r'\bbtn\b': 'Button',
    r'\bcalc\b': 'calculate', # or calculation depending on context
    r'\bindo\b': 'indonesia',
    r'\bgic\b': 'globalIslamicCriteria',
    r'\bfnz\b': 'fajrNewZealand',
    r'\blat\b': 'latitude',
    r'\blon\b': 'longitude',
    r'\btr\b': 'translations',
    r'\bsfx\b': 'suffix',
    r'\bpfx\b': 'prefix',
    r'\bAE_OFFSET\b': 'ASTRONOMY_ENGINE_OFFSET',
    r'\bBA_LAT\b': 'BANDA_ACEH_LATITUDE',
    r'\bBA_LON\b': 'BANDA_ACEH_LONGITUDE',
}

def refactor(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Special cases for btn which is often used in IDs or classes
    content = content.replace('.nav-btn', '.navigation-button')
    content = content.replace('nav-btn', 'navigation-button')

    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)
        # Also handle CamelCase
        pattern_cap = r'\b' + pattern[2:-2].capitalize() + r'\b'
        content = re.sub(pattern_cap, replacement.capitalize(), content)

    # Specific fixes for HilalSync
    content = content.replace('jd29', 'julianDate29')
    content = content.replace('detailAceh', 'detailIndonesia')
    content = content.replace('jdAceh', 'julianDateIndonesia')
    content = content.replace('jdGic', 'julianDateGlobal')
    content = content.replace('gicInfo', 'globalInformation')
    content = content.replace('acehInfo', 'indonesiaInformation')

    with open(filepath, 'w') as f:
        f.write(content)

if __name__ == "__main__":
    for arg in sys.argv[1:]:
        refactor(arg)
