from pathlib import Path
from PIL import Image,ImageOps,ImageStat,ImageFilter
import csv,json,html,math,re
from datetime import datetime
from photo_selection import Evidence,classify
from condition_classifier import Context,classify_condition

REPO=Path(__file__).resolve().parents[1]
SOURCE=Path("/Users/daiana-melaniadobre/Library/Mobile Documents/com~apple~CloudDocs/001_Jimmy's business/System Feythic Live/01_ACTIVE/TPC-20260515-21/content/visual/photography-portfolio")
REPORTS=REPO/'reports';THUMBS=REPORTS/'reclassification-thumbnails'
RECOVERED_FROM_CONCEPTUAL={
 '20240913_151004.jpg','20241011_144452.jpg','20241120_102425.jpg','20250721_184641.jpg',
 '20250724_154355.jpg','20250810_094813.jpg','20250811_200604.jpg','20260815_104901.jpg',
 '20260820_161912.jpg','20260820_161948.jpg','20260823_104746.jpg'
}

def metrics(path):
    with Image.open(path) as im:
        im=ImageOps.exif_transpose(im).convert('RGB');w,h=im.size;small=im.copy();small.thumbnail((320,320))
        stat=ImageStat.Stat(small);mean=sum(stat.mean)/3;contrast=sum(stat.stddev)/3
        hsv=small.convert('HSV');sat=ImageStat.Stat(hsv).mean[1];edges=small.convert('L').filter(ImageFilter.FIND_EDGES);edge=ImageStat.Stat(edges).mean[0]
        extrema=small.convert('L').getextrema();blank_black=1 if extrema[1]<8 else 0;blank_white=1 if extrema[0]>247 else 0
        return dict(width=w,height=h,mean=mean,contrast=contrast,saturation=sat,edge=edge,black=blank_black,white=blank_white,rgb=stat.mean)

def semantics(m):
    tags=['observational','documentary','everyday-life'];series=['Everyday Observations'];notes=[]
    if m['width']>m['height']*1.2:tags+=['landscape-orientation','sense-of-place'];series+=['Places and Passage']
    elif m['height']>m['width']*1.2:tags+=['portrait-orientation','details'];series+=['Fragments and Details']
    if m['mean']<75:tags+=['night','atmosphere','light'];series+=['After Dark']
    if m['saturation']>80:tags+=['colour'];series+=['Colour Encounters']
    if m['edge']>22:tags+=['geometry','architecture'];series+=['Built Geometry']
    r,g,b=m['rgb']
    if g>r*1.05 and g>b*1.05:tags+=['nature','green'];series+=['Green / Urban Nature']
    if m['contrast']>65:notes+=['strong contrast or clipping may be expressive']
    if m['mean']<55:notes+=['dark exposure retained as an atmospheric characteristic']
    if m['saturation']>105:notes+=['strong artificial or saturated colour']
    return tags,series,notes

def subject_metadata(tags):
    # Pixel statistics cannot responsibly identify a photograph's subject.
    # Keep this field conservative until supplied by a human or a dedicated
    # visual review; it must never leak into Condition classification.
    return 'Other','visual subject requires human confirmation',.2

def normalise_condition(value):
    v=(value or '').upper().strip()
    mapping={'NOTHING HAPPENED HERE':'ABSENCE','BETWEEN PLACES':'CROSSING','THE THINGS THAT STOPPED ME':'ATTENTION',
      'THE WAY THINGS WERE ARRANGED':'ARRANGEMENT','TWO THINGS CAN BE TRUE':'CONTRADICTION','ONE PERSON, STILL HERE':'SOLITARY PRESENCE',
      'I HAPPENED TO BE THERE':'OCCURRENCE / WITNESS','I SAW IT HAPPEN':'OCCURRENCE / WITNESS','SOMEONE LOST THIS':'FOUND',
      'I CAME BACK':'RETURN','I WAS HERE':'UNKNOWN','THINGS THAT EXISTED FOR ME':'ATTENTION'}
    if v in {'ABSENCE','TRACE','CONSUMPTION','CO-PRESENCE','SOLITARY PRESENCE','CROSSING','ATTENTION','CONTRADICTION','ARRANGEMENT','FOUND','OCCURRENCE / WITNESS','RETURN','UNKNOWN'}:return v
    return mapping.get(v,'UNKNOWN')

def capture_time(filename):
    m=re.match(r'^(\d{8})_(\d{6})',filename)
    return datetime.strptime(''.join(m.groups()),'%Y%m%d%H%M%S') if m else None

def axes(m,strength,selected):
    # Pixel measurements describe characteristics, not artistic quality. They
    # only nudge the human/curatorial strength estimate; saturated colour,
    # high contrast or abundant edges cannot promote a frame by themselves.
    colour=max(3,min(9,strength+(m['saturation']-70)/90));texture=max(3,min(9,strength+(m['edge']-18)/35));light=max(3,min(9,strength+(m['contrast']-45)/70))
    series=8 if selected else 7 if strength>=7 else 6.3 if strength>=6 else 5.5
    return {'composition':strength,'light':round(light,1),'colour':round(colour,1),'atmosphere':round(max(light,colour)-.3,1),
      'documentary_value':5.8,'sense_of_place':5.8,'geometry':round(texture,1),'texture':round(texture,1),
      'narrative_potential':5.7,'sequencing_potential':series,'series_potential':series,
      'curated_selection':strength if selected else min(7,strength)}

def main():
    REPORTS.mkdir(exist_ok=True);THUMBS.mkdir(exist_ok=True)
    rename=list(csv.DictReader((SOURCE/'TPC_CORRECTIVE_RECURATION_RENAME_MAP.csv').open()))
    selected=list(csv.DictReader((SOURCE/'TPC_SELECTED_PHOTOGRAPHS.csv').open()))
    by_original={r['Original Filename']:r for r in rename};selected_names={r['Original Filename'] for r in selected}
    current={r['Original Filename']:(SOURCE/r['Original Filename'] if (SOURCE/r['Original Filename']).exists() else SOURCE/r['New Filename']) for r in rename}|{n:SOURCE/n for n in selected_names}
    all_rows=[]
    for idx,(original,path) in enumerate(sorted(current.items())):
        previous='CONCEPTUAL_REJECT' if original in RECOVERED_FROM_CONCEPTUAL else ('SELECTED' if original in selected_names else by_original[original]['Previous Classification'])
        try:
            m=metrics(path);decode=True
        except Exception:
            m={'width':0,'height':0,'mean':0,'contrast':0,'saturation':0,'edge':0,'black':0,'white':0,'rgb':[0,0,0]};decode=False
        tags,series,notes=semantics(m)
        if original in selected_names:
            pos=next(i for i,r in enumerate(selected) if r['Original Filename']==original);selected_row=selected[pos];strength=float(selected_row.get('Photographic Strength') or 8)
            confidence=.88;override='FEATURE' if strength>=9 or pos<10 else 'SUPPORTING'
            primary=normalise_condition(selected_row.get('Primary Condition'));secondary=[normalise_condition(x.strip()) for x in (selected_row.get('Secondary Conditions') or '').split(',') if x.strip()][:2]
            condition_data={'primary_condition':primary,'secondary_conditions':[x for x in secondary if x!='UNKNOWN'],'confidence':.9 if primary!='UNKNOWN' else .4,'reason':'Preserved human-curated relational classification.' if primary!='UNKNOWN' else 'Existing record does not support a more specific relationship than certain Presence.','human_review_required':primary=='UNKNOWN'}
        else:
            strength=float(by_original[original]['Photographic Strength']);confidence=.78 if strength>=7 else .68 if strength>=6 else .6;override=None
            if strength<=5 and (m['mean']<48 or m['mean']>210 or m['edge']<6):confidence=.5
            condition_data=classify_condition(Context())
        e=Evidence(decode_ok=decode,confidence=confidence,axes=axes(m,strength,original in selected_names),tags=tags,possible_series=series,technical_notes=notes,
          near_black_ratio=m['black'],near_white_ratio=m['white'],accidental_blank_confidence=.4,manual_override=override)
        subject,subtype,subject_confidence=subject_metadata(tags)
        preservation=classify(e)
        out={**condition_data,'subject':subject,'subject_subtype':subtype,'subject_confidence':subject_confidence,'subject_review_required':True,
          'sequence_id':None,'sequence_position':None,'sequence_neighbours':[],**preservation,
          'filename':path.name,'original_filename':original,'previous_classification':previous,'metrics':m}
        all_rows.append(out)
        if previous=='CONCEPTUAL_REJECT':
            with Image.open(path) as im:
                im=ImageOps.exif_transpose(im).convert('RGB');im.thumbnail((240,180));canvas=Image.new('RGB',(240,180),(20,20,20));canvas.paste(im,((240-im.width)//2,(180-im.height)//2));canvas.save(THUMBS/f'{original}.jpg',quality=78)
    # Sequence awareness is mandatory but conservative: close timestamps create
    # candidates/context, never a fabricated Condition.
    timed=sorted([(capture_time(r['original_filename']),r) for r in all_rows if capture_time(r['original_filename'])],key=lambda x:x[0]);groups=[];current=[]
    for timestamp,row in timed:
        if current and (timestamp-current[-1][0]).total_seconds()>900:
            if len(current)>1:groups.append(current)
            current=[]
        current.append((timestamp,row))
    if len(current)>1:groups.append(current)
    for number,group in enumerate(groups,1):
        sequence_id=f'SEQ-CANDIDATE-{number:03d}';names=[r['original_filename'] for _,r in group]
        for position,(_,row) in enumerate(group,1):row.update({'sequence_id':sequence_id,'sequence_position':position,'sequence_neighbours':[n for n in names if n!=row['original_filename']]})
    # Final preservation classification happens only after the Condition and
    # sequence layers exist. A photograph previously landing in ARCHIVE can
    # legitimately become SUPPORTING when an actual neighbouring sequence
    # gives it series value; UNKNOWN Condition never counts against it.
    for row in all_rows:
        if row['classification']=='ARCHIVE' and row['sequence_id']:
            revised_axes=dict(row['axes'])
            revised_axes['series_potential']=max(6.5,revised_axes.get('series_potential',0))
            revised_axes['sequencing_potential']=max(6.5,revised_axes.get('sequencing_potential',0))
            revised=classify(Evidence(decode_ok=True,confidence=row['confidence'],axes=revised_axes,
              tags=row['tags'],possible_series=row['possible_series'],technical_notes=row['technical_notes']))
            row.update(revised)
            row['reason']='Supporting through documented neighbouring-sequence potential; Condition was assigned first and did not operate as a quality score.'
        row['layer_order_applied']=['CONDITION','PRESERVATION','PUBLIC_DISPLAY']
    rejected=[r for r in all_rows if r['previous_classification']=='CONCEPTUAL_REJECT']
    (REPORTS/'library-classification.json').write_text(json.dumps({'version':3,'layer_order':['CONDITION','PRESERVATION','PUBLIC_DISPLAY'],'doctrine':'relationship Condition first; ingestion permissive; curation selective; rejection exceptional','records':all_rows},indent=2))
    (REPORTS/'reclassification-report.json').write_text(json.dumps({'previous_rejections_reassessed':len(rejected),'records':rejected},indent=2))
    cards=[]
    for r in rejected:
        tags=' '.join(f'<span>{html.escape(t)}</span>' for t in r['tags']);series=', '.join(r['possible_series'])
        cards.append(f'''<article><img loading="lazy" src="reclassification-thumbnails/{html.escape(r['original_filename'])}.jpg"><h2>{html.escape(r['original_filename'])}</h2><p><b>{r['previous_classification']} → {r['classification']}</b> · confidence {r['confidence']:.2f}</p><p>Primary Condition: <b>{html.escape(r['primary_condition'])}</b></p><p>Subject: {html.escape(r['subject'])}</p><p>{html.escape(r['reason'])}</p><div>{tags}</div><p><small>Potential series: {html.escape(series)}</small></p></article>''')
    counts={c:sum(r['classification']==c for r in all_rows) for c in ['FEATURE','SUPPORTING','ARCHIVE','REVIEW','REJECT']}
    page=f'''<!doctype html><meta charset="utf-8"><title>TPC reclassification report</title><style>body{{font:13px Courier New;background:#f3f0eb;margin:24px}}header{{max-width:900px;margin-bottom:30px}}main{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}}article{{border:1px solid #bbb;padding:10px}}img{{width:100%;aspect-ratio:4/3;object-fit:contain;background:#111}}h2{{font-size:12px}}span{{display:inline-block;border:1px solid #bbb;padding:3px;margin:2px}}</style><header><h1>TPC PRESERVATION-FIRST RECLASSIFICATION</h1><p>Former conceptual rejects: {len(rejected)}. New distribution: {html.escape(str(counts))}. Originals preserved.</p></header><main>{''.join(cards)}</main>'''
    (REPORTS/'reclassification-report.html').write_text(page)
    print(json.dumps({'total':len(all_rows),**counts,'rejection_percentage':round(counts['REJECT']/len(all_rows)*100,2)},indent=2))

if __name__=='__main__':main()
