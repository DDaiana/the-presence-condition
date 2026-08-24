import Link from "next/link";
import conditions from "../../data/conditions.json";
import archive from "../../data/public-archive.json";
import {Shell} from "../components";

export default function Conditions(){
  const base=process.env.NEXT_PUBLIC_BASE_PATH??"";
  return <Shell><h1>THE CONDITION</h1><p className="condition-intro">Conditions describe the relationship between presence and the photograph — not simply what appears in the frame.</p><div className="condition-list">{conditions.map(c=>{const entries=archive.filter(p=>p.content_pool==="CONDITION"&&p.condition===c.slug);const image=entries[0]?.archive_id??"TPC-00145";return <Link href={`/condition/${c.slug}`} key={c.slug}><img src={`${base}/archive/${image}.jpg`} alt=""/><span><b>{c.title}</b><small>{c.definition}<br/>{entries.length} {entries.length===1?"entry":"entries"}.</small></span><i>→</i></Link>})}</div></Shell>;
}
