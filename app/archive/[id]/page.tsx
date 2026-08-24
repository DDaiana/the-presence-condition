import Link from "next/link";
import metadata from "../../../data/public-metadata.json";
import publicArchive from "../../../data/public-archive.json";
import conditions from "../../../data/conditions.json";
import {Shell} from "../../components";
import ShareButton from "./share-button";

export function generateStaticParams(){return publicArchive.map(p=>({id:p.archive_id}))}

export default async function Photo({params}:{params:Promise<{id:string}>}){
  const base=process.env.NEXT_PUBLIC_BASE_PATH??"";
  const {id}=await params;
  const index=publicArchive.findIndex(p=>p.archive_id===id);
  const entry=publicArchive[index];
  const p=metadata.find(x=>x.archive_id===id);
  if(!p||!entry)return <Shell>Photograph not found.</Shell>;
  const next=publicArchive[(index+1)%publicArchive.length];
  const condition=conditions.find(c=>c.slug===entry.condition);
  return <Shell><div className="detail-nav"><Link href="/archive">← BACK</Link><Link href={`/archive/${next.archive_id}`}>NEXT →</Link></div><div className="detail"><img src={`${base}/archive/${p.archive_id}.jpg`} alt={`Archive photograph ${p.archive_id}`} draggable={false}/><div className="detail-id"><h1>{p.archive_id}</h1><ShareButton/></div>{p.public_date&&<p>{p.public_date}</p>}<hr/><dl><dt>CONDITION</dt><dd>{condition?.title??"THE PRESENCE ARCHIVE"}</dd><dt>LOCATION</dt><dd>NOT PUBLISHED</dd><dt>NOTES</dt><dd>—</dd></dl></div></Shell>;
}
