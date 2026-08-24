import { mkdir, readFile } from "node:fs/promises"; import { execFileSync } from "node:child_process";
const records=JSON.parse(await readFile("data/photo-inventory.json","utf8")); await mkdir("public/archive",{recursive:true}); let count=0;
for(const record of records){if(record.exact_duplicate_of) continue; execFileSync("sips",["-s","format","jpeg","-s","formatOptions","68","-Z","1200",record.source_path,"--out",`public/archive/${record.archive_id}.jpg`],{stdio:"ignore"}); count++;}
console.log(`Built ${count} stripped, web-resolution derivatives.`);
