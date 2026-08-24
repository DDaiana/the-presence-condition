import Link from "next/link";

const base=process.env.NEXT_PUBLIC_BASE_PATH??"";
// Deliberately sequenced for light, scale, gesture, transition, stillness,
// geometry, colour, human presence, landscape, and enclosure.
const photos = ["TPC-00145","TPC-00135","TPC-00236","TPC-00178","TPC-00082","TPC-00067","TPC-00136","TPC-00218","TPC-00099","TPC-00143"].map(id=>`${base}/archive/${id}.jpg`);

export default function Home() {
  return <main>
    <header className="site-header"><Link className="mark" href="/">TPC</Link><Link href="/">THE PRESENCE CONDITION</Link><nav aria-label="Primary navigation"><Link href="/condition">THE CONDITION</Link><Link href="/archive">THE PRESENCE ARCHIVE</Link><Link href="/about">ABOUT</Link><Link href="/info">INFO</Link></nav><details className="mobile-menu"><summary>MENU ☰</summary><div><Link href="/condition">THE CONDITION</Link><Link href="/archive">THE PRESENCE ARCHIVE</Link><Link href="/about">ABOUT</Link><Link href="/info">INFO</Link></div></details></header>
    <section className="hero"><div className="hero-copy"><h1>THE PRESENCE<br/>CONDITION</h1><p>Photographs as evidence of presence.<br/><br/>Not what I saw.<br/>Proof that I was there.</p><Link className="hero-link" href="/archive">ENTER THE PRESENCE ARCHIVE →</Link></div><img src={photos[0]} alt="Light and shadow marking an ordinary moment"/></section>
    <section className="recent"><div className="section-heading"><h2>RECENT ENTRIES FROM THE ARCHIVE</h2><Link href="/archive">VIEW ALL ⠿</Link></div><div className="photo-strip">{photos.map(photo=>{const id=photo.split('/').pop()!.replace('.jpg','');return <Link href={`/archive/${id}`} key={photo}><img src={photo} alt="" draggable={false}/></Link>})}</div><div className="intro-grid"><p>A photograph can show almost anything.<br/><br/>But every photograph also contains something it cannot show directly:<br/><br/>the presence of the person who took it.</p><img src={photos[3]} alt="A quiet interior recorded in the archive" draggable={false}/><div><h2>THE PRESENCE CONDITION</h2><p>A long-term initiative documenting presence through photographs and written reflections.</p><Link href="/about">ABOUT THE CONDITION →</Link></div></div></section>
    <footer><Link href="/copyright">© THE PRESENCE CONDITION</Link><Link href="/copyright">LEGAL / COPYRIGHT</Link><span>CONTACT</span><Link href="/copyright">PRIVACY</Link><Link href="/copyright">TERMS</Link></footer>
  </main>;
}
