"use client";
import Link from "next/link";
import {useMemo,useState} from "react";

type Entry={archive_id:string;condition:string|null;public_date:string|null};

export default function ArchiveGrid({entries}:{entries:Entry[]}){
  const base=process.env.NEXT_PUBLIC_BASE_PATH??"";
  const [sort,setSort]=useState<"latest"|"oldest">("latest");
  const [limit,setLimit]=useState(16);
  const shown=useMemo(()=>[...entries].sort((a,b)=>{const dateOrder=(a.public_date??"").localeCompare(b.public_date??"");const stable=dateOrder||a.archive_id.localeCompare(b.archive_id);return sort==="latest"?-stable:stable}),[entries,sort]);
  return <><p className="archive-count">CURATED ENTRIES · {shown.length?1:0} — {Math.min(limit,shown.length)} OF {shown.length}</p><div className="archive-tools"><button onClick={()=>setSort(sort==="latest"?"oldest":"latest")}>SORT {sort.toUpperCase()} {sort==="latest"?"↓":"↑"}</button></div><div className="archive-grid">{shown.slice(0,limit).map(p=><Link key={p.archive_id} href={`/archive/${p.archive_id}`}><img src={`${base}/archive/${p.archive_id}.jpg`} alt={`Archive entry ${p.archive_id}`} loading="lazy" draggable={false}/></Link>)}</div>{limit<shown.length&&<button className="load-more" onClick={()=>setLimit(v=>v+12)}>LOAD MORE</button>}</>;
}
