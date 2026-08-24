import {notFound} from "next/navigation";
import conditions from "../../../data/conditions.json";
import archive from "../../../data/public-archive.json";
import metadata from "../../../data/public-metadata.json";
import {Shell} from "../../components";
import ConditionGrid from "../condition-grid";

export function generateStaticParams(){return conditions.map(c=>({slug:c.slug}))}

export default async function Condition({params}:{params:Promise<{slug:string}>}){
  const {slug}=await params;
  const c=conditions.find(x=>x.slug===slug);
  if(!c)notFound();
  const dates=new Map(metadata.map(p=>[p.archive_id,p.public_date]));
  const entries=archive.filter(p=>p.content_pool==="CONDITION"&&p.condition===slug).map(p=>({archive_id:p.archive_id,public_date:dates.get(p.archive_id)??null}));
  return <Shell><h1>{c.title}</h1><p>{c.definition}</p><p className="condition-intro">{c.paragraph}</p>{entries.length?<ConditionGrid entries={entries}/>:<div className="empty">No photographs have been assigned to this Condition.</div>}</Shell>;
}
