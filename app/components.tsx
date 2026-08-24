import Link from "next/link";
const Nav=()=> <><Link href="/condition">THE CONDITION</Link><Link href="/archive">THE PRESENCE ARCHIVE</Link><Link href="/about">ABOUT</Link><Link href="/info">INFO</Link></>;
export function Header(){return <header className="site-header"><Link className="mark" href="/">TPC</Link><Link href="/">THE PRESENCE CONDITION</Link><nav aria-label="Primary navigation"><Nav/></nav><details className="mobile-menu"><summary>MENU ☰</summary><div><Nav/></div></details></header>}
export function Footer(){return <footer><Link href="/copyright">© THE PRESENCE CONDITION</Link><Link href="/copyright">LEGAL / COPYRIGHT</Link><span>CONTACT</span><Link href="/copyright">PRIVACY</Link><Link href="/copyright">TERMS</Link></footer>}
export function Shell({children}:{children:React.ReactNode}){return <main><Header/><div className="page">{children}</div><Footer/></main>}
