for(let i=0;i<50;i++){
    let s=document.createElement("div");
    s.innerText="❄";
    s.style.position="fixed";
    s.style.left=Math.random()*100+"vw";
    s.style.top="-10px";
    s.style.fontSize=(10+Math.random()*10)+"px";
    s.style.animation=`fall ${3+Math.random()*5}s linear infinite`;
    document.body.appendChild(s);
}

let style=document.createElement("style");
style.innerHTML=`@keyframes fall{to{transform:translateY(110vh)}}`;
document.head.appendChild(style);
