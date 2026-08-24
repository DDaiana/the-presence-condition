import {readFile,mkdir,rm} from "node:fs/promises";
import {execFileSync} from "node:child_process";
import {tmpdir} from "node:os";
import {join} from "node:path";

const records=JSON.parse(await readFile("data/photo-inventory.json","utf8"));
await mkdir("public/archive",{recursive:true});let count=0;
for(const record of records){
  if(record.exact_duplicate_of)continue;
  const temporary=join(tmpdir(),`${record.archive_id}-scaled.jpg`);const output=`public/archive/${record.archive_id}.jpg`;
  execFileSync("sips",["-s","format","jpeg","-s","formatOptions","74","-Z","1600",record.source_path,"--out",temporary],{stdio:"ignore"});
  execFileSync("ffmpeg",["-loglevel","error","-y","-i",temporary,"-map_metadata","-1","-q:v","3",output],{stdio:"ignore"});
  await rm(temporary,{force:true});count++;
}
console.log(`Built ${count} privacy-safe web derivatives; originals unchanged.`);
