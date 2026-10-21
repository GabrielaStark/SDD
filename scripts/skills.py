#!/usr/bin/env python3
"""Validate and package SDD skills using the Python standard library only."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = {
    'requirements.md': ('sdd-requirements', 'requirements.md'),
    'design.md': ('sdd-design', 'design.md'),
    'tasks.md': ('sdd-tasks', 'tasks.md'),
    'intent.md': ('sdd-requirements-mantenimiento', 'intent.md'),
    'requirements-mantenimiento.md': ('sdd-requirements-mantenimiento', 'requirements-mantenimiento.md'),
    'design-delta.md': ('sdd-design-delta', 'design-delta.md'),
    'tasks-riesgo.md': ('sdd-tasks-risk', 'tasks-riesgo.md'),
}


class InvalidSkill(ValueError):
    pass


def markdown_prose(text):
    """Ignore link-like examples inside fenced code blocks."""
    result, fence = [], None
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            value = marker[1]
            if fence is None:
                fence = value
            elif value[0] == fence[0] and len(value) >= len(fence):
                fence = None
            continue
        if fence is None:
            result.append(line)
    return '\n'.join(result)


def frontmatter(text):
    """Enforce this repo's two single-line YAML string fields (quoted as JSON)."""
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if not match:
        raise InvalidSkill('Missing YAML frontmatter')
    fields = {}
    for line in match[1].splitlines():
        key, separator, value = line.partition(':')
        if not separator or key not in {'name', 'description'} or key in fields:
            raise InvalidSkill(f'Unsupported or duplicate metadata: {line}')
        value = value.strip()
        try:
            fields[key] = json.loads(value) if value.startswith('"') else value
        except json.JSONDecodeError as exc:
            raise InvalidSkill(f'Invalid quoted value for {key}') from exc
    if set(fields) != {'name', 'description'}:
        raise InvalidSkill('name and description are required')
    name, description = fields['name'], fields['description']
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
        raise InvalidSkill('Invalid name')
    if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
        raise InvalidSkill('description must have 1–1024 characters')
    # Plain metadata strings must not contain YAML syntax ambiguities.
    for line in match[1].splitlines():
        value = line.partition(':')[2].strip()
        if not value.startswith('"') and any(token in value for token in (': ', ' #', '[', '{')):
            raise InvalidSkill('Quote metadata with JSON-compatible double quotes')
    return fields


def validate_skill(directory):
    directory = Path(directory)
    if directory.is_symlink() or not directory.is_dir():
        raise InvalidSkill(f'Not a regular skill directory: {directory}')
    source = directory / 'SKILL.md'
    if not source.is_file() or source.is_symlink():
        raise InvalidSkill('SKILL.md missing or symlinked')
    text = source.read_text(encoding='utf-8')
    metadata = frontmatter(text)
    if metadata['name'] != directory.name:
        raise InvalidSkill('name must match skill directory')
    if len(text.splitlines()) >= 500:
        raise InvalidSkill('Keep SKILL.md below 500 lines')
    if not (directory / 'LICENSE').is_file():
        raise InvalidSkill('LICENSE missing')
    required = {'## Entradas', '## Salidas', '## Procedimiento', '## Revisión y aprobación'}
    if not required.issubset(set(text.splitlines())):
        raise InvalidSkill('Missing independent input/output/workflow/review contract')
    for file in directory.rglob('*'):
        if file.is_symlink():
            raise InvalidSkill(f'Symlink not allowed in package: {file}')
        if not file.is_file():
            continue
        if file.suffix in {'.pyc', '.zip'} or '.git' in file.parts or '__pycache__' in file.parts:
            raise InvalidSkill(f'Build artifact in source package: {file}')
        if file.suffix != '.md':
            continue
        content = file.read_text(encoding='utf-8')
        if re.search(r'\.claude/(skills|agents)/|docs/documentacion/|/workspace/|/root/', content):
            raise InvalidSkill(f'Repository/runtime dependency in {file}')
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', markdown_prose(content)):
            if target.startswith(('https://', 'http://', '#', 'mailto:')):
                continue
            resolved = (file.parent / target.split('#')[0]).resolve()
            if not resolved.is_relative_to(directory.resolve()) or not resolved.is_file():
                raise InvalidSkill(f'Missing or external local reference in {file}: {target}')
    # Every bundled reference, asset and executable must be discoverable directly.
    for category in ('references', 'assets', 'scripts'):
        for file in (directory / category).rglob('*') if (directory / category).exists() else []:
            if file.is_file() and f'({file.relative_to(directory).as_posix()})' not in text:
                raise InvalidSkill(f'Resource not linked from SKILL.md: {file.name}')
    return metadata


def catalog(root=ROOT):
    data = json.loads((root / 'skills.json').read_text(encoding='utf-8'))
    if not re.fullmatch(r'\d+\.\d+\.\d+', data['version']):
        raise InvalidSkill('Use a numeric semantic version')
    names = [entry['name'] for entry in data['skills']]
    if len(names) != len(set(names)):
        raise InvalidSkill('Duplicate catalog entry')
    actual = {p.name for p in (root / '.claude/skills').iterdir() if p.is_dir()}
    if actual != set(names):
        raise InvalidSkill('Catalog and source skill folders differ')
    for entry in data['skills']:
        if entry['path'] != f'.claude/skills/{entry["name"]}':
            raise InvalidSkill('Catalog path must match name')
    return data


def validate_repository(root=ROOT):
    data = catalog(root)
    for entry in data['skills']:
        validate_skill(root / entry['path'])
    for old, (name, file) in TEMPLATES.items():
        if (root / 'templates' / old).read_bytes() != (root / '.claude/skills' / name / 'assets' / file).read_bytes():
            raise InvalidSkill(f'Stale compatibility template: {old}; run sync-templates')
    return data


def build_zip(directory, destination):
    validate_skill(directory)
    files = sorted(p for p in directory.rglob('*') if p.is_file())
    with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for file in files:
            info = zipfile.ZipInfo(f'{directory.name}/{file.relative_to(directory).as_posix()}', date_time=(2020, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, file.read_bytes(), compresslevel=9)
    return {'files': [str(p.relative_to(directory)) for p in files], 'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}


def package(root=ROOT, selected=None, output=None):
    data = validate_repository(root)
    entries = [e for e in data['skills'] if not selected or e['name'] == selected]
    if not entries:
        raise InvalidSkill(f'Unknown skill: {selected}')
    output = Path(output or root / 'dist').resolve()
    skill_root = (root / '.claude/skills').resolve()
    if output.is_relative_to(skill_root):
        raise InvalidSkill('Output cannot be inside skill sources')
    output.mkdir(parents=True, exist_ok=True)
    manifest = {'version': data['version'], 'source': data['source'], 'packages': []}
    for entry in entries:
        filename = f'{entry["name"]}-{data["version"]}.zip'
        details = build_zip(root / entry['path'], output / filename)
        manifest['packages'].append({'name': entry['name'], 'file': filename, **details})
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'package', 'sync-templates'])
    parser.add_argument('--skill', help='Package only this named skill')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'sync-templates':
            for old, (name, file) in TEMPLATES.items():
                (ROOT / 'templates' / old).write_bytes((ROOT / '.claude/skills' / name / 'assets' / file).read_bytes())
            print('Compatibility templates synchronized.')
        elif args.command == 'validate':
            data = validate_repository()
            print(f'Validated {len(data["skills"])} independent skill packages.')
        else:
            manifest = package(selected=args.skill, output=args.output)
            for item in manifest['packages']:
                print(f'{item["file"]}  sha256:{item["sha256"]}')
    except (InvalidSkill, OSError, KeyError, ValueError) as exc:
        parser.exit(1, f'Validation failed: {exc}\n')


if __name__ == '__main__':
    main()
