from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
inventory=json.loads((ROOT/'data/photo-inventory.json').read_text())
classified=json.loads((ROOT/'reports/library-classification.json').read_text())['records']
editorial_assignments=json.loads((ROOT/'data/condition-assignments.json').read_text())
curation_path=ROOT/'data/photograph-curation.json'
curation_records=json.loads(curation_path.read_text())['records'] if curation_path.exists() else []
curation_by_id={r['photo_id']:r for r in curation_records}
by_file={r['original_filename']:r for r in classified}
assigned={archive_id:slug for slug,archive_ids in editorial_assignments.items() for archive_id in archive_ids}

def public_condition(record,archive_id):
    # Public editorial language is separate from the stored Primary Condition.
    # Do not use subject, tags or Secondary Conditions for this mapping.
    if archive_id in assigned:return assigned[archive_id]
    # Every remaining Condition-pool image was visually reviewed as an object,
    # place, façade, animal, found encounter or other act of attention.
    return 'things-that-existed-for-me'

gallery=[];metadata=[]
for item in inventory:
    c=by_file[item['source_file']];classification=c['classification']
    curatorial=curation_by_id.get(item['archive_id'])
    promoted=item['archive_id'] in assigned
    condition_selected=promoted and curatorial and curatorial['curation_status'] in {'CURATED','SEQUENCE_MEMBER'}
    # The public Condition pages contain only the last approved curated edit.
    # Every other retained photograph belongs to The Presence Archive,
    # regardless of its internal preservation class or taxonomy label.
    content_pool='CONDITION' if condition_selected else 'ARCHIVE'
    condition=public_condition(c,item['archive_id']) if content_pool=='CONDITION' else None
    gallery.append({'archive_id':item['archive_id'],'classification':classification,'content_pool':content_pool,
      'condition':condition,'display_condition':condition,'condition_promotion':promoted and classification=='ARCHIVE',
      'primary_condition':c['primary_condition'],'secondary_conditions':c['secondary_conditions'],
      'subject':c['subject'],'subject_subtype':c['subject_subtype'],'sequence_id':c['sequence_id'],
      'featured':classification=='FEATURE','tags':c['tags'],'possible_series':c['possible_series'],
      'curation_status':curatorial['curation_status'] if curatorial else None,
      'overall_curatorial_score':curatorial['overall_curatorial_score'] if curatorial else None,
      'curatorial_confidence':curatorial['curatorial_confidence'] if curatorial else None,
      'home_featured':curatorial['home_featured'] if curatorial else False})
    metadata.append({'archive_id':item['archive_id'],'public_date':item.get('public_date')})

(ROOT/'data/public-archive.json').write_text(json.dumps(gallery,indent=2)+'\n')
(ROOT/'data/public-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
counts={k:sum(x['classification']==k for x in gallery) for k in ['FEATURE','SUPPORTING','ARCHIVE','REVIEW','REJECT']}
print(json.dumps({'records':len(gallery),**counts},indent=2))
