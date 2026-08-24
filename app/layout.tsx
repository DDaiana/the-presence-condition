import type { Metadata } from "next";
import "./globals.css";
import "./refinements.css";

export const metadata: Metadata = {metadataBase:new URL("https://ddaiana.github.io/the-presence-condition/"),title:{default:"The Presence Condition",template:"%s — The Presence Condition"},description:"Photographs as evidence of presence.",openGraph:{title:"The Presence Condition",description:"Photographs as evidence of presence.",type:"website"},twitter:{card:"summary",title:"The Presence Condition",description:"Photographs as evidence of presence."}};
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="en"><body>{children}</body></html>}
