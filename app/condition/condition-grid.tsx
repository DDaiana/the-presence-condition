"use client";
import Link from "next/link";
import {useMemo,useState} from "react";

type Entry={archive_id:string;public_date:string|null};

export default function ConditionGrid({entries}:{entries:Entry[]}){
  const base=process.env.NEXT_PUBLIC_BASE_PATH??"";
  const [sort,setSort]=useState<"oldest"|"latest">("oldest");
  const ordered=useMemo(()=>[...entries].sort((a,b)=>{
    const dateOrder=(a.public_date??"").localeCompare(b.public_date??"");
    const stable=dateOrder||a.archive_id.localeCompare(b.archive_id);
    return sort==="oldest"?stable:-stable;
  }),[entries,sort]);
  return <><div className="archive-tools"><button onClick={()=>setSort(sort==="oldest"?"latest":"oldest")}>SORT {sort.toUpperCase()} {sort==="oldest"?"↑":"↓"}</button></div><div className="archive-grid">{ordered.map(p=><Link href={`/archive/${p.archive_id}`} key={p.archive_id}><img src={`${base}/archive/${p.archive_id}.jpg`} alt={`Archive entry ${p.archive_id}`} loading="lazy" draggable={false}/></Link>)}</div></>;
}
