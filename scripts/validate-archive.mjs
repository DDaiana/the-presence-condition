import { access, readFile } from "node:fs/promises";

const records=JSON.parse(await readFile("data/photo-inventory.json","utf8"));
const publicRecords=JSON.parse(await readFile("data/public-archive.json","utf8"));
const conditionAssignments=JSON.parse(await readFile("data/condition-assignments.json","utf8"));
let missing=0;
for(const r of records.filter(x=>!x.exact_duplicate_of)){
  try{await access(`public/archive/${r.archive_id}.jpg`)}catch{missing++}
}
if(missing) throw new Error(`${missing} derivatives missing`);

const assignedConditions=new Map();
for(const [condition,ids] of Object.entries(conditionAssignments)){
  for(const id of ids){
    if(assignedConditions.has(id)) throw new Error(`${id} is assigned to both ${assignedConditions.get(id)} and ${condition}`);
    assignedConditions.set(id,condition);
  }
}

const archiveIds=new Set(publicRecords.filter(x=>x.content_pool==="ARCHIVE").map(x=>x.archive_id));
const conditionIds=new Set(publicRecords.filter(x=>x.content_pool==="CONDITION").map(x=>x.archive_id));
const curatedConditionRecords=publicRecords.filter(x=>x.content_pool==="CONDITION"&&(x.curation_status==="CURATED"||x.curation_status==="SEQUENCE_MEMBER"));
const curatedPublicRecords=publicRecords.filter(x=>x.curation_status==="CURATED"||x.curation_status==="SEQUENCE_MEMBER");
const overlap=[...archiveIds].filter(id=>conditionIds.has(id));
if(overlap.length) throw new Error(`Archive/Condition content overlap: ${overlap.join(", ")}`);
for(const row of publicRecords){
  if(row.content_pool==="ARCHIVE"&&row.condition!==null) throw new Error(`${row.archive_id} has Archive ownership and a Condition route`);
  if(row.content_pool==="CONDITION"&&!row.condition) throw new Error(`${row.archive_id} has Condition ownership without a Condition route`);
}
const routedConditionIds=publicRecords.filter(x=>x.content_pool==="CONDITION").map(x=>x.archive_id);
if(new Set(routedConditionIds).size!==routedConditionIds.length) throw new Error("A photograph appears in more than one public Condition route");
for(const row of curatedPublicRecords){
  if(typeof row.overall_curatorial_score!=="number"||row.overall_curatorial_score<8) throw new Error(`${row.archive_id} is public below the 8.0 curatorial threshold`);
}
console.log(`Validated ${records.length} inventory records; Archive evidence ${archiveIds.size}, curated Archive ${curatedPublicRecords.length-curatedConditionRecords.length}, Condition evidence ${conditionIds.size}, curated Condition ${curatedConditionRecords.length}, Condition duplicates 0, overlap 0; all publishable derivatives present.`);
