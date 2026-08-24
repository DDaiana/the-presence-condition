"use client";
export default function ShareButton(){async function share(){if(navigator.share)await navigator.share({title:document.title,url:location.href});else await navigator.clipboard.writeText(location.href)}return <button className="text-button" onClick={share}>SHARE ↗</button>}
