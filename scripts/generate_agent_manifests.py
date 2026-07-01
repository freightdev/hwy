from pathlib import Path
import re
import yaml

root = Path('/home/nabrith/hwy')
agents_root = root / 'moonrust/agents'

def clean_line(line: str) -> str:
    line = line.replace('\\n', '\n')
    line = re.sub(r'^\s*#+\s*', '', line)
    line = line.replace('**', '').replace('`', '')
    line = re.sub(r'^\s*[-*]\s*', '', line)
    return line.strip()

def keep(value: str) -> bool:
    return bool(value) and value not in {'---', '--'} and not value.lower().startswith('examples')

def title_from_slug(slug: str) -> str:
    return slug.replace('-', ' ').replace('_', ' ').title()

def section_text(lines: list[str], heading: str) -> list[str]:
    out=[]
    capture=False
    for raw in lines:
        c=clean_line(raw)
        if c.lower() == heading.lower():
            capture=True
            continue
        if capture and raw.lstrip().startswith('#') and c.lower() != heading.lower():
            break
        if capture:
            for part in c.split('\n'):
                part=part.strip()
                if keep(part): out.append(part)
    return out

def first_sentence(text: str) -> str:
    text = ' '.join(clean_line(x) for x in text.splitlines())
    text = re.sub(r'\s+', ' ', text).strip()
    if not text: return 'TODO'
    m = re.match(r'(.+?[.!?])(?:\s|$)', text)
    return m.group(1).strip() if m else text

def purpose(lines: list[str]) -> str:
    s = section_text(lines, 'Purpose') or section_text(lines, 'Mission')
    return first_sentence('\n'.join(s)) if s else 'TODO'

def identity_domain(lines: list[str], agent_slug: str) -> str:
    ident = ' '.join(section_text(lines, 'Identity'))
    m = re.search(r'agent that ([^.]+)', ident, re.I)
    if m: return m.group(1).strip()
    p = purpose(lines)
    if p != 'TODO':
        return re.sub(r'^(I|This agent|It)\s+', '', p, flags=re.I).rstrip('.')
    return agent_slug.replace('-', ' ')

def interface_values(lines: list[str], key: str) -> list[str]:
    iface = '\n'.join(section_text(lines, 'Interface'))
    vals=[]
    for line in iface.replace('\\n','\n').split('\n'):
        clean=clean_line(line)
        if clean.lower().startswith(f'{key}:'):
            val=clean.split(':',1)[1].strip()
            if keep(val): vals.append(val)
    if vals: return vals
    pattern = rf'{key}\**\s*:\s*([^\n]+)'
    for m in re.finditer(pattern, iface, re.I):
        val=m.group(1).strip()
        if keep(val): vals.append(val)
    return vals or ['TODO']

def dedupe(vals):
    out=[]
    for v in vals:
        v=v.strip().rstrip('.')
        if keep(v) and v not in out: out.append(v)
    return out

def deps(lines: list[str]) -> list[str]:
    vals=[]
    for line in section_text(lines, 'Dependencies'):
        for part in line.replace('\\n','\n').split('\n'):
            part=clean_line(part)
            if keep(part): vals.append(part)
    return dedupe(vals) or ['TODO']

def sentence_extract(text, patterns):
    vals=[]
    for raw in text.splitlines():
        for piece in raw.replace('\\n','\n').split('\n'):
            c=clean_line(piece).rstrip('.')
            if not keep(c): continue
            l=c.lower()
            if any(p in l for p in patterns): vals.append(c)
    return dedupe(vals) or ['TODO']

def logbooks(text):
    vals=[m.group(1).strip() for m in re.finditer(r'\b([A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+){0,2} Logbook)\b', text)]
    return dedupe(vals) or ['TODO']

def reports(text):
    vals=[m.group(1).strip() for m in re.finditer(r'\b([A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+){0,2} Report)\b', text)]
    return dedupe(vals) or ['TODO']

def main():
    count=0
    for arch in sorted(agents_root.glob('*/*/ARCHITECTURE.md')):
        category = arch.parent.parent.name
        slug = arch.parent.name
        text = arch.read_text()
        lines = text.splitlines()
        manifest = {
            'agent_id': f'{category}.{slug}',
            'name': title_from_slug(slug),
            'category': category,
            'capability_domain': identity_domain(lines, slug),
            'mission': purpose(lines),
            'inputs': interface_values(lines, 'in'),
            'outputs': interface_values(lines, 'out'),
            'allowed_callers': ['TODO'],
            'allowed_actors': ['TODO'],
            'required_permissions': ['TODO'],
            'risk_level': 'TODO',
            'tools_needed': deps(lines),
            'workers_needed': ['TODO'],
            'truth_rules': sentence_extract(text, ['truth', 'verify', 'confidence', 'uncertain', 'do not claim', 'must not', 'never ']),
            'logbooks_written': logbooks(text),
            'reports_contributed_to': reports(text),
            'human_review_required_for': sentence_extract(text, ['human review', 'human approval', 'manual review', 'approval required', 'requires approval']),
            'cannot_do': sentence_extract(text, ['does not', 'cannot ', 'must not', 'should not', 'never ']),
            'architecture_source': f'moonrust/agents/{category}/{slug}/ARCHITECTURE.md',
        }
        (arch.parent / 'manifest.yaml').write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=1000))
        count += 1
    print(f'wrote {count} agent manifests')

if __name__ == '__main__':
    main()
