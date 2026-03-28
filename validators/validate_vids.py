#!/usr/bin/env python3
"""
VIDS Unified Validator - 21-Rule Compliance Check
Validates a dataset against the full VIDS specification.

Usage:
    python validate_vids.py /path/to/dataset
    python validate_vids.py /path/to/dataset --profile full
    python validate_vids.py /path/to/dataset --json
    python validate_vids.py /path/to/dataset --fix  (auto-fix minor issues)
"""

import json
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timezone


class VIDSValidator:
    """Validates a dataset against the VIDS specification."""

    RULES = [
        # Structure rules (S001-S006)
        ('S001', 'vids_marker',            '.vids marker file exists'),
        ('S002', 'dataset_description',    'dataset_description.json exists and valid'),
        ('S003', 'participants_file',      'participants.json or .tsv exists'),
        ('S004', 'readme_exists',          'README.md exists'),
        ('S005', 'subject_directories',    'Subject directories follow sub-XXX pattern'),
        ('S006', 'session_directories',    'Session directories follow ses-XXX pattern'),
        # Imaging rules (I001-I004)
        ('I001', 'imaging_files',          'Imaging NIfTI files present for each subject'),
        ('I002', 'imaging_sidecars',       'Imaging sidecar JSON files present'),
        ('I003', 'imaging_json_valid',     'Imaging sidecar JSONs are valid'),
        ('I004', 'filename_convention',    'Files follow VIDS naming convention'),
        # Annotation rules (A001-A005)
        ('A001', 'annotation_directory',   'derivatives/annotations/ exists'),
        ('A002', 'annotation_files',       'Segmentation files present for annotated subjects'),
        ('A003', 'annotation_sidecars',    'Annotation sidecar JSONs present'),
        ('A004', 'annotation_json_valid',  'Annotation JSONs valid and contain required fields'),
        ('A005', 'provenance_complete',    'Provenance fields populated (Annotator, Tool, Date)'),
        # Quality rules (Q001-Q003) - Full profile only
        ('Q001', 'quality_directory',      'quality/ directory exists (Full profile)'),
        ('Q002', 'quality_summary',        'quality_summary.json present (Full profile)'),
        ('Q003', 'annotation_agreement',   'annotation_agreement.json present (Full profile)'),
        # ML rules (M001-M002) - Full profile only
        ('M001', 'ml_directory',           'ml/ directory exists (Full profile)'),
        ('M002', 'ml_splits',             'ml/splits.json present (Full profile)'),
        # Metadata rules (D001)
        ('D001', 'changes_file',           'CHANGES.md exists'),
    ]

    def __init__(self, dataset_path: str, profile: str = 'auto'):
        self.dataset_path = Path(dataset_path).resolve()
        self.profile = profile
        self.results = []
        self.errors = []
        self.warnings = []
        self.subjects = []

    def detect_profile(self) -> str:
        """Auto-detect profile from .vids marker."""
        marker = self.dataset_path / '.vids'
        if marker.exists():
            content = marker.read_text()
            if 'full' in content.lower():
                return 'full'
            if 'poc' in content.lower():
                return 'poc'
        return 'poc'  # default

    def _pass(self, rule_id: str, message: str):
        self.results.append({'rule': rule_id, 'status': 'PASS', 'message': message})

    def _fail(self, rule_id: str, message: str):
        self.results.append({'rule': rule_id, 'status': 'FAIL', 'message': message})
        self.errors.append(f"{rule_id}: {message}")

    def _warn(self, rule_id: str, message: str):
        self.results.append({'rule': rule_id, 'status': 'WARN', 'message': message})
        self.warnings.append(f"{rule_id}: {message}")

    def _skip(self, rule_id: str, message: str):
        self.results.append({'rule': rule_id, 'status': 'SKIP', 'message': message})

    def _load_json(self, path: Path) -> Optional[dict]:
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return None

    # ── Structure Rules ─────────────────────────────────────
    def check_vids_marker(self):
        if (self.dataset_path / '.vids').exists():
            self._pass('S001', '.vids marker file present')
        else:
            self._fail('S001', '.vids marker file missing')

    def check_dataset_description(self):
        p = self.dataset_path / 'dataset_description.json'
        if not p.exists():
            self._fail('S002', 'dataset_description.json missing')
            return
        data = self._load_json(p)
        if data is None:
            self._fail('S002', 'dataset_description.json is not valid JSON')
            return
        # Spec-aligned required fields (VIDS v1.0)
        required = ['Name', 'VIDSVersion', 'DatasetVersion', 'License', 'Description', 'Authors']
        missing = [f for f in required if f not in data]
        if missing:
            self._fail('S002', f"dataset_description.json missing fields: {', '.join(missing)}")
        else:
            self._pass('S002', 'dataset_description.json valid')

    def check_participants_file(self):
        has_json = (self.dataset_path / 'participants.json').exists()
        has_tsv = (self.dataset_path / 'participants.tsv').exists()
        if has_json or has_tsv:
            self._pass('S003', f"Participants file present ({'json' if has_json else 'tsv'})")
        else:
            self._fail('S003', 'No participants.json or participants.tsv')

    def check_readme_exists(self):
        if (self.dataset_path / 'README.md').exists():
            self._pass('S004', 'README.md present')
        else:
            self._fail('S004', 'README.md missing')

    def check_subject_directories(self):
        self.subjects = sorted([d for d in self.dataset_path.glob('sub-*') if d.is_dir()])
        if self.subjects:
            self._pass('S005', f'{len(self.subjects)} subject directories found')
        else:
            self._fail('S005', 'No subject directories (sub-*) found')

    def check_session_directories(self):
        if not self.subjects:
            self._skip('S006', 'No subjects to check')
            return
        bad = []
        for subj in self.subjects:
            sessions = [d for d in subj.glob('ses-*') if d.is_dir()]
            if not sessions:
                bad.append(subj.name)
        if bad:
            self._fail('S006', f"{len(bad)} subjects missing session dirs: {', '.join(bad[:5])}")
        else:
            self._pass('S006', 'All subjects have session directories')

    # ── Imaging Rules ───────────────────────────────────────
    def check_imaging_files(self):
        if not self.subjects:
            self._skip('I001', 'No subjects')
            return
        missing = []
        for subj in self.subjects:
            nifti = list(subj.rglob('*_img.nii.gz')) + list(subj.rglob('*_img.nii'))
            if not nifti:
                missing.append(subj.name)
        if missing:
            self._fail('I001', f"{len(missing)} subjects missing imaging files: {', '.join(missing[:5])}")
        else:
            self._pass('I001', 'All subjects have imaging files')

    def check_imaging_sidecars(self):
        if not self.subjects:
            self._skip('I002', 'No subjects')
            return
        missing = []
        for subj in self.subjects:
            jsons = list(subj.rglob('*_img.json'))
            if not jsons:
                missing.append(subj.name)
        if missing:
            self._fail('I002', f"{len(missing)} subjects missing imaging sidecar JSONs")
        else:
            self._pass('I002', 'All subjects have imaging sidecar JSONs')

    def check_imaging_json_valid(self):
        all_jsons = []
        for subj in self.subjects:
            all_jsons.extend(subj.rglob('*_img.json'))
        if not all_jsons:
            self._skip('I003', 'No imaging JSONs to validate')
            return
        invalid = []
        for jf in all_jsons:
            if self._load_json(jf) is None:
                invalid.append(str(jf.relative_to(self.dataset_path)))
        if invalid:
            self._fail('I003', f"{len(invalid)} invalid imaging JSONs: {', '.join(invalid[:3])}")
        else:
            self._pass('I003', f'{len(all_jsons)} imaging JSONs valid')

    def check_filename_convention(self):
        if not self.subjects:
            self._skip('I004', 'No subjects')
            return
        bad = []
        for subj in self.subjects:
            for nifti in subj.rglob('*.nii.gz'):
                name = nifti.stem.replace('.nii', '')
                if not name.startswith('sub-'):
                    bad.append(str(nifti.relative_to(self.dataset_path)))
        if bad:
            self._warn('I004', f"{len(bad)} files don't follow naming convention: {', '.join(bad[:3])}")
        else:
            self._pass('I004', 'All files follow VIDS naming convention')

    # ── Annotation Rules ────────────────────────────────────
    def check_annotation_directory(self):
        if (self.dataset_path / 'derivatives' / 'annotations').is_dir():
            self._pass('A001', 'derivatives/annotations/ exists')
        else:
            self._fail('A001', 'derivatives/annotations/ missing')

    def check_annotation_files(self):
        annot_root = self.dataset_path / 'derivatives' / 'annotations'
        if not annot_root.is_dir():
            self._skip('A002', 'No annotations directory')
            return
        segs = list(annot_root.rglob('*_seg.nii.gz')) + list(annot_root.rglob('*_seg.nii'))
        if segs:
            self._pass('A002', f'{len(segs)} segmentation files found')
        else:
            self._fail('A002', 'No segmentation files in derivatives/annotations/')

    def check_annotation_sidecars(self):
        annot_root = self.dataset_path / 'derivatives' / 'annotations'
        if not annot_root.is_dir():
            self._skip('A003', 'No annotations directory')
            return
        jsons = list(annot_root.rglob('*_seg.json'))
        if jsons:
            self._pass('A003', f'{len(jsons)} annotation sidecar JSONs found')
        else:
            self._fail('A003', 'No annotation sidecar JSONs found')

    def check_annotation_json_valid(self):
        annot_root = self.dataset_path / 'derivatives' / 'annotations'
        if not annot_root.is_dir():
            self._skip('A004', 'No annotations directory')
            return
        jsons = list(annot_root.rglob('*_seg.json'))
        invalid = []
        missing_fields = []
        for jf in jsons:
            data = self._load_json(jf)
            if data is None:
                invalid.append(jf.name)
            elif 'VIDSVersion' not in data:
                missing_fields.append(jf.name)
        if invalid:
            self._fail('A004', f"{len(invalid)} invalid annotation JSONs")
        elif missing_fields:
            self._fail('A004', f"{len(missing_fields)} JSONs missing VIDSVersion")
        elif jsons:
            self._pass('A004', f'{len(jsons)} annotation JSONs valid')
        else:
            self._skip('A004', 'No annotation JSONs to check')

    def check_provenance_complete(self):
        annot_root = self.dataset_path / 'derivatives' / 'annotations'
        if not annot_root.is_dir():
            self._skip('A005', 'No annotations directory')
            return
        jsons = list(annot_root.rglob('*_seg.json'))
        incomplete = []
        for jf in jsons:
            data = self._load_json(jf)
            if data is None:
                continue
            prov = data.get('Provenance', {})
            if not isinstance(prov, dict):
                incomplete.append(jf.name)
                continue
            annotator = prov.get('Annotator', {})
            process = prov.get('AnnotationProcess', {})
            if not annotator.get('ID') and not annotator.get('Name'):
                incomplete.append(jf.name)
            elif not process.get('Date') and not process.get('Tool'):
                incomplete.append(jf.name)
        if incomplete:
            self._fail('A005', f"{len(incomplete)} files with incomplete provenance: {', '.join(incomplete[:3])}")
        elif jsons:
            self._pass('A005', 'All annotations have complete provenance')
        else:
            self._skip('A005', 'No annotations to check')

    # ── Quality Rules (Full profile only) ───────────────────
    def check_quality_directory(self):
        if self.profile != 'full':
            self._skip('Q001', 'POC profile — quality/ optional')
            return
        if (self.dataset_path / 'quality').is_dir():
            self._pass('Q001', 'quality/ directory exists')
        else:
            self._fail('Q001', 'quality/ directory missing (required for Full profile)')

    def check_quality_summary(self):
        if self.profile != 'full':
            self._skip('Q002', 'POC profile — quality_summary optional')
            return
        if (self.dataset_path / 'quality' / 'quality_summary.json').exists():
            self._pass('Q002', 'quality_summary.json present')
        else:
            self._fail('Q002', 'quality/quality_summary.json missing')

    def check_annotation_agreement(self):
        if self.profile != 'full':
            self._skip('Q003', 'POC profile — annotation_agreement optional')
            return
        if (self.dataset_path / 'quality' / 'annotation_agreement.json').exists():
            self._pass('Q003', 'annotation_agreement.json present')
        else:
            self._fail('Q003', 'quality/annotation_agreement.json missing')

    # ── ML Rules (Full profile only) ────────────────────────
    def check_ml_directory(self):
        if self.profile != 'full':
            self._skip('M001', 'POC profile — ml/ optional')
            return
        if (self.dataset_path / 'ml').is_dir():
            self._pass('M001', 'ml/ directory exists')
        else:
            self._fail('M001', 'ml/ directory missing (required for Full profile)')

    def check_ml_splits(self):
        if self.profile != 'full':
            self._skip('M002', 'POC profile — splits optional')
            return
        if (self.dataset_path / 'ml' / 'splits.json').exists():
            self._pass('M002', 'ml/splits.json present')
        else:
            self._fail('M002', 'ml/splits.json missing')

    # ── Metadata Rules ──────────────────────────────────────
    def check_changes_file(self):
        if (self.dataset_path / 'CHANGES.md').exists():
            self._pass('D001', 'CHANGES.md present')
        else:
            self._warn('D001', 'CHANGES.md missing (recommended)')

    # ── Runner ──────────────────────────────────────────────
    def validate(self) -> Dict:
        """Run all 21 validation rules."""
        if self.profile == 'auto':
            self.profile = self.detect_profile()

        for rule_id, method_name, description in self.RULES:
            method = getattr(self, f'check_{method_name}', None)
            if method:
                try:
                    method()
                except Exception as e:
                    self._fail(rule_id, f'Validator error: {e}')

        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        warned = sum(1 for r in self.results if r['status'] == 'WARN')
        skipped = sum(1 for r in self.results if r['status'] == 'SKIP')

        return {
            'VIDSVersion': '1.0',
            'ValidatorVersion': '1.1',
            'DatasetPath': str(self.dataset_path),
            'Profile': self.profile,
            'ValidationDate': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'Summary': {
                'TotalRules': len(self.RULES),
                'Passed': passed,
                'Failed': failed,
                'Warnings': warned,
                'Skipped': skipped,
                'Status': 'PASS' if failed == 0 else 'FAIL'
            },
            'Results': self.results,
            'Errors': self.errors,
            'Warnings': self.warnings
        }


def print_report(report: Dict):
    """Print formatted validation report."""
    summary = report['Summary']
    status = summary['Status']

    print(f"\n{'='*60}")
    print(f"VIDS Validation Report")
    print(f"Profile: {report['Profile'].upper()}")
    print(f"Dataset: {report['DatasetPath']}")
    print(f"{'='*60}\n")

    status_icons = {'PASS': '✅', 'FAIL': '❌', 'WARN': '⚠️ ', 'SKIP': '⏭ '}

    for r in report['Results']:
        icon = status_icons.get(r['status'], '?')
        print(f"  {icon} {r['rule']}: {r['message']}")

    print(f"\n{'-'*60}")
    print(f"  Passed:   {summary['Passed']}")
    print(f"  Failed:   {summary['Failed']}")
    print(f"  Warnings: {summary['Warnings']}")
    print(f"  Skipped:  {summary['Skipped']}")
    print(f"{'-'*60}")

    if status == 'PASS':
        print(f"\n✅ VALIDATION PASSED ({summary['Passed']}/{summary['TotalRules']} rules)\n")
    else:
        print(f"\n❌ VALIDATION FAILED ({summary['Failed']} errors)\n")


def main():
    parser = argparse.ArgumentParser(description='VIDS 21-Rule Compliance Validator')
    parser.add_argument('dataset_root', help='Path to dataset root')
    parser.add_argument('--profile', choices=['poc', 'full', 'auto'], default='auto',
                        help='Validation profile (default: auto-detect)')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    parser.add_argument('--output', help='Write JSON report to file')
    args = parser.parse_args()

    dataset_root = Path(args.dataset_root)
    if not dataset_root.exists():
        print(f"Error: {dataset_root} not found", file=sys.stderr)
        sys.exit(1)

    validator = VIDSValidator(str(dataset_root), profile=args.profile)
    report = validator.validate()

    if args.json:
        print(json.dumps(report, indent=2))
    elif args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"✅ Report written to {args.output}")
        print_report(report)
    else:
        print_report(report)

    sys.exit(0 if report['Summary']['Status'] == 'PASS' else 1)


if __name__ == '__main__':
    main()
