"use client";
import Link from "next/link";
import {useMemo,useState} from "react";

type Entry={archive_id:string;condition:string|null;public_date:string|null};

export default function ArchiveGrid({entries}:{entries:Entry[]}){
  const base=process.env.NEXT_PUBLIC_BASE_PATH??"";
  const [sort,setSort]=useState<"latest"|"oldest">("latest");
  const [condition,setCondition]=useState("all");
  const [limit,setLimit]=useState(16);
  const shown=useMemo(()=>{const filtered=condition==="all"?entries:entries.filter(e=>e.condition===condition);return sort==="latest"?filtered:[...filtered].reverse()},[entries,sort,condition]);
  return <><p className="archive-count">CURATED ENTRIES · {shown.length?1:0} — {Math.min(limit,shown.length)} OF {shown.length}</p><div className="archive-tools"><label>CONDITION <select value={condition} onChange={e=>{setCondition(e.target.value);setLimit(16)}}><option value="all">ALL</option><option value="i-was-here">I WAS HERE</option><option value="nothing-happened-here">NOTHING HAPPENED HERE</option><option value="between-places">BETWEEN PLACES</option><option value="the-things-i-didnt-go-looking-for">THE THINGS I DIDN&apos;T GO LOOKING FOR</option><option value="things-that-existed-for-me">THINGS THAT EXISTED FOR ME</option></select></label><button onClick={()=>setSort(sort==="latest"?"oldest":"latest")}>SORT {sort.toUpperCase()} {sort==="latest"?"↓":"↑"}</button></div><div className="archive-grid">{shown.slice(0,limit).map(p=><Link key={p.archive_id} href={`/archive/${p.archive_id}`}><img src={`${base}/archive/${p.archive_id}.jpg`} alt={`Archive entry ${p.archive_id}`} loading="lazy" draggable={false}/></Link>)}</div>{limit<shown.length&&<button className="load-more" onClick={()=>setLimit(v=>v+12)}>LOAD MORE</button>}</>;
}
