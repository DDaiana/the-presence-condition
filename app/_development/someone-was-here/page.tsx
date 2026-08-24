import Link from "next/link";
import {Shell} from "../../components";

export default function Someone(){
  const base=process.env.NEXT_PUBLIC_BASE_PATH??"";
  const images=["TPC-00154","TPC-00219","TPC-00145","TPC-00051","TPC-00111","TPC-00135","TPC-00167","TPC-00236"];
  return <Shell><div className="title-row"><div><h1>SOMEONE WAS HERE</h1><p>Your presence can be part of the archive.</p><p>The archive begins with one idea:<br/>It was not here on its own.</p><p>Submit a photograph that exists<br/>because you were there to take it.</p></div><Link className="button" href="/submit">SUBMIT TO THE ARCHIVE</Link></div><div className="section-heading"><h2>THE FOUNDING ARCHIVE</h2><span>APPROVED CONTRIBUTIONS WILL APPEAR HERE</span></div><div className="archive-grid guest-grid">{images.map(id=><Link href={`/archive/${id}`} key={id}><img src={`${base}/archive/${id}.jpg`} alt={`Archive entry ${id}`}/></Link>)}</div></Shell>;
}
