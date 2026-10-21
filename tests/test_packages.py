import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('skills', ROOT / 'scripts/skills.py')
skills = importlib.util.module_from_spec(spec)
spec.loader.exec_module(skills)


class PackageTests(unittest.TestCase):
    def test_each_zip_validates_in_isolation_and_is_reproducible(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            first = skills.package(output=temp / 'first')
            second = skills.package(output=temp / 'second')
            self.assertEqual(first, second)
            self.assertEqual(9, len(first['packages']))
            for package in first['packages']:
                with self.subTest(skill=package['name']):
                    target = temp / package['name']
                    with zipfile.ZipFile(temp / 'first' / package['file']) as archive:
                        self.assertEqual({package['name']}, {Path(n).parts[0] for n in archive.namelist()})
                        archive.extractall(target)
                    skills.validate_skill(target / package['name'])

    def copy_skill(self, temporary):
        directory = Path(temporary) / 'reglas-negocio'
        shutil.copytree(ROOT / '.claude/skills/reglas-negocio', directory)
        return directory

    def test_missing_resource_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = self.copy_skill(temp)
            (directory / 'assets/business-rules.md').unlink()
            with self.assertRaisesRegex(skills.InvalidSkill, 'Missing or external'):
                skills.validate_skill(directory)

    def test_reference_to_sibling_skill_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = self.copy_skill(temp)
            (directory.parent / 'external.md').write_text('outside package')
            with (directory / 'SKILL.md').open('a') as file:
                file.write('\n[Hidden dependency](../external.md)\n')
            with self.assertRaisesRegex(skills.InvalidSkill, 'Missing or external'):
                skills.validate_skill(directory)

    def test_symlink_cannot_export_external_content(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = self.copy_skill(temp)
            (directory / 'assets/outside.txt').symlink_to(Path(temp) / 'private.txt')
            with self.assertRaisesRegex(skills.InvalidSkill, 'Symlink'):
                skills.validate_skill(directory)

    def test_metadata_failures_rejected(self):
        for frontmatter in ('name: ok', 'name: bad--name\ndescription: x', 'name: ok\ndescription: ""', 'name: ok\nname: twice\ndescription: x'):
            with self.subTest(frontmatter=frontmatter), self.assertRaises(skills.InvalidSkill):
                skills.frontmatter(f'---\n{frontmatter}\n---\nbody')

    def test_single_skill_and_manifest(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest = skills.package(selected='reglas-negocio', output=Path(temp))
            self.assertEqual(1, len(manifest['packages']))
            self.assertEqual(manifest, json.loads((Path(temp) / 'manifest.json').read_text()))


if __name__ == '__main__':
    unittest.main()
