import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from photo_selection import Evidence,classify
from condition_classifier import Context,classify_condition

class PreservationFirstTests(unittest.TestCase):
    def test_subjects_never_trigger_rejection(self):
        subjects=['building','person','car','commercial-interior','food','landmark','signage','artificial-colour','night','window-frame','mundane-object','unconventional-composition','imperfect-exposure','visible-brand','tourists','strangers']
        for subject in subjects:
            with self.subTest(subject=subject):
                r=classify(Evidence(tags=[subject],axes={'documentary_value':6.5,'series_potential':7},technical_notes=['imperfection retained']))
                self.assertIn(r['classification'],{'FEATURE','SUPPORTING','ARCHIVE','REVIEW'})
    def test_corrupt_file_can_be_recommended_for_exclusion(self):self.assertEqual(classify(Evidence(decode_ok=False))['classification'],'REJECT')
    def test_blank_requires_strong_accidental_evidence(self):
        self.assertNotEqual(classify(Evidence(near_black_ratio=.999,accidental_blank_confidence=.4))['classification'],'REJECT')
        self.assertEqual(classify(Evidence(near_black_ratio=.999,accidental_blank_confidence=.99))['classification'],'REJECT')
    def test_duplicates_are_conservative(self):
        self.assertNotEqual(classify(Evidence(exact_duplicate_of='x',superior_duplicate_confirmed=False))['classification'],'REJECT')
        self.assertEqual(classify(Evidence(exact_duplicate_of='x',superior_duplicate_confirmed=True))['classification'],'REJECT')
    def test_low_confidence_becomes_review(self):self.assertEqual(classify(Evidence(confidence=.4))['classification'],'REVIEW')
    def test_meaningful_imperfection_survives(self):
        r=classify(Evidence(technical_notes=['blur','grain','strong colour cast'],axes={'atmosphere':8,'documentary_value':7}))
        self.assertNotEqual(r['classification'],'REJECT')
        self.assertTrue(r['original_preserved'])
    def test_reject_never_deletes(self):self.assertTrue(classify(Evidence(decode_ok=False))['original_preserved'])
    def test_object_alone_never_determines_condition(self):
        for subject in ['Food','People','Architecture','Nature','Transport','Object']:
            with self.subTest(subject=subject):self.assertEqual(classify_condition(Context(subject=subject))['primary_condition'],'UNKNOWN')
    def test_relational_note_can_support_condition(self):
        self.assertEqual(classify_condition(Context(subject='Food',note='The meal had been eaten and the empty plate remained.'))['primary_condition'],'CONSUMPTION')
        self.assertEqual(classify_condition(Context(subject='Place',note='I came back to the same place again.'))['primary_condition'],'RETURN')
    def test_ambiguity_becomes_unknown_review(self):
        r=classify_condition(Context(subject='Object',note='Found empty and abandoned.'))
        self.assertEqual(r['primary_condition'],'UNKNOWN');self.assertTrue(r['human_review_required'])
    def test_neighbouring_sequence_context_is_used(self):
        r=classify_condition(Context(subject='Food',neighbouring_notes=['The meal had been eaten.','Only traces remained.'],sequence_id='SEQ-1'))
        self.assertEqual(r['primary_condition'],'CONSUMPTION')
    def test_series_value_can_make_a_frame_supporting(self):
        r=classify(Evidence(axes={'composition':5.5,'series_potential':6.5,'sequencing_potential':6.5},confidence=.7))
        self.assertEqual(r['classification'],'SUPPORTING')

if __name__=='__main__':unittest.main()
