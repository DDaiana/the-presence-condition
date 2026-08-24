import Link from "next/link";
import {notFound} from "next/navigation";
import metadata from "../../../data/public-metadata.json";
import publicArchive from "../../../data/public-archive.json";
import conditions from "../../../data/conditions.json";
import {Shell} from "../../components";
import ShareButton from "./share-button";

const isPublic=(p:(typeof publicArchive)[number])=>p.curation_status==="CURATED"||p.curation_status==="SEQUENCE_MEMBER"||p.home_featured;
export function generateStaticParams(){return publicArchive.filter(isPublic).map(p=>({id:p.archive_id}))}

export default async function Photo({params}:{params:Promise<{id:string}>}){
  const base=process.env.NEXT_PUBLIC_BASE_PATH??"";
  const {id}=await params;
  const index=publicArchive.findIndex(p=>p.archive_id===id);
  const entry=publicArchive[index];
  const p=metadata.find(x=>x.archive_id===id);
  if(!p||!entry||!isPublic(entry))notFound();
  const collection=entry.content_pool==="ARCHIVE"?publicArchive.filter(x=>x.content_pool==="ARCHIVE"&&isPublic(x)):publicArchive.filter(x=>x.content_pool==="CONDITION"&&x.condition===entry.condition&&isPublic(x));
  const collectionIndex=collection.findIndex(x=>x.archive_id===id);
  const next=collection[(collectionIndex+1)%collection.length];
  const condition=conditions.find(c=>c.slug===entry.condition);
  const back=entry.content_pool==="ARCHIVE"?"/archive":`/condition/${entry.condition}`;
  return <Shell><div className="detail-nav"><Link href={back}>← BACK</Link><Link href={`/archive/${next.archive_id}`}>NEXT →</Link></div><div className="detail"><img src={`${base}/archive/${p.archive_id}.jpg`} alt={`Archive photograph ${p.archive_id}`} draggable={false}/><div className="detail-id"><h1>{p.archive_id}</h1><ShareButton/></div>{p.public_date&&<p>{p.public_date}</p>}<hr/><dl><dt>CONDITION</dt><dd>{condition?.title??"THE PRESENCE ARCHIVE"}</dd><dt>LOCATION</dt><dd>NOT PUBLISHED</dd><dt>NOTES</dt><dd>—</dd></dl></div></Shell>;
}
