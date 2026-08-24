import Link from "next/link";
import conditions from "../../../data/conditions.json";
import archive from "../../../data/public-archive.json";
import {Shell} from "../../components";

export function generateStaticParams(){return conditions.map(c=>({slug:c.slug}))}

export default async function Condition({params}:{params:Promise<{slug:string}>}){
  const base=process.env.NEXT_PUBLIC_BASE_PATH??"";
  const {slug}=await params;
  const c=conditions.find(x=>x.slug===slug);
  const entries=archive.filter(p=>p.condition===slug);
  return <Shell><h1>{c?.title??"CONDITION"}</h1><p>{c?.definition}</p>{entries.length?<div className="archive-grid">{entries.map(p=><Link href={`/archive/${p.archive_id}`} key={p.archive_id}><img src={`${base}/archive/${p.archive_id}.jpg`} alt={`Archive entry ${p.archive_id}`}/></Link>)}</div>:<div className="empty">No photographs have been assigned to this Condition.</div>}</Shell>;
}
