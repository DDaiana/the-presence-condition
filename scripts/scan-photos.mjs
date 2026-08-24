import {createHash} from "node:crypto";
import {readdir,readFile,writeFile} from "node:fs/promises";
import {basename,extname,join} from "node:path";
import {execFileSync} from "node:child_process";

const root=process.env.TPC_PHOTO_SOURCE;
if(!root) throw new Error("Set TPC_PHOTO_SOURCE to the authoritative photography-portfolio directory.");
const supported=new Set([".jpg",".jpeg",".png",".heic",".webp",".tif",".tiff"]);
async function walk(dir){const out=[];for(const entry of await readdir(dir,{withFileTypes:true})){const p=join(dir,entry.name);if(entry.isDirectory())out.push(...await walk(p));else if(!entry.name.startsWith("TPC_")&&supported.has(extname(entry.name).toLowerCase()))out.push(p)}return out}
async function optionalJson(path,fallback){try{return JSON.parse(await readFile(path,"utf8"))}catch{return fallback}}

const previousRegistry=await optionalJson("data/archive-registry.json",{});
const curation=await optionalJson("data/curation.json",{overrides:{}});
const files=(await walk(root)).sort();
const seenHashes=new Map();const records=[];let nextId=Math.max(0,...Object.values(previousRegistry).map(v=>Number(String(v).replace(/\D/g,""))||0))+1;
for(const path of files){
  const bytes=await readFile(path);const hash=createHash("sha256").update(bytes).digest("hex");
  const archiveId=previousRegistry[hash]??`TPC-${String(nextId++).padStart(5,"0")}`;
  const exactDuplicateOf=seenHashes.get(hash)??null;if(!exactDuplicateOf)seenHashes.set(hash,archiveId);
  let decoded=true,info="";try{info=execFileSync("sips",["-g","pixelWidth","-g","pixelHeight","-g","orientation",path],{encoding:"utf8"})}catch{decoded=false}
  const read=key=>info.match(new RegExp(`${key}: (.+)`))?.[1]??null;const filename=basename(path);
  const stamp=filename.match(/^(\d{4})(\d{2})(\d{2})[_-]?(\d{2})?(\d{2})?(\d{2})?/);const capture=stamp?`${stamp[1]}-${stamp[2]}-${stamp[3]}${stamp[4]?`T${stamp[4]}:${stamp[5]??"00"}:${stamp[6]??"00"}`:""}`:null;
  const manual=curation.overrides?.[archiveId]??{};
  records.push({source_file:filename,source_path:path,filename,extension:extname(path).toLowerCase(),original_date:capture,capture_datetime:capture,
    width:Number(read("pixelWidth"))||null,height:Number(read("pixelHeight"))||null,orientation:Number(read("orientation"))||null,
    GPS:null,city:null,neighbourhood:null,country:null,camera:null,duplicate_hash:hash,exact_duplicate_of:exactDuplicateOf,
    derivative_status:"pending",archive_status:"retained",
    primary_condition:manual.primary_condition??"UNKNOWN",secondary_conditions:manual.secondary_conditions??[],condition_confidence:manual.condition_confidence??.35,condition_review_required:manual.primary_condition==null,
    subject:manual.subject??"Other",subject_subtype:manual.subject_subtype??null,sequence_id:manual.sequence_id??null,
    classification:manual.classification??(decoded?"REVIEW":"REJECT"),
    classification_confidence:manual.confidence??(decoded?.5:.99),classification_reason:manual.reason??(decoded?"New photograph retained for human or assisted review.":"File could not be decoded; exclusion recommendation is reversible."),
    tags:manual.tags??[],possible_series:manual.possible_series??[],technical_notes:decoded?[]:["decode failure"],manual_review_required:decoded,
    public_display_eligible:["FEATURE","SUPPORTING"].includes(manual.classification),condition_candidates:[],selected_condition:null,
    public_title:null,archive_id:archiveId,public_location:null,public_date:capture?.slice(0,10)??null,notes:null});
}
const registry={...previousRegistry,...Object.fromEntries(records.map(r=>[r.duplicate_hash,r.archive_id]))};
await writeFile("data/photo-inventory.json",JSON.stringify(records,null,2)+"\n");
await writeFile("data/archive-registry.json",JSON.stringify(registry,null,2)+"\n");
console.log(`Inventoried ${records.length} photographs; retained ${records.filter(r=>r.archive_status==="retained").length}; decode failures ${records.filter(r=>r.classification==="REJECT").length}.`);
