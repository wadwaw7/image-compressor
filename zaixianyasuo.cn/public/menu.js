// 移动端折叠菜单
document.addEventListener('DOMContentLoaded',()=>{
  const nav=document.querySelector('.nav-links');
  if(!nav) return;
  if(document.getElementById('nav-toggle')) return;
  const btn=document.createElement('button');
  btn.id='nav-toggle';
  btn.className='nav-toggle';
  btn.setAttribute('aria-label','菜单');
  btn.setAttribute('aria-expanded','false');
  btn.textContent='☰';
  nav.parentElement.insertBefore(btn,nav.nextSibling);

  const isOpen = ()=>nav.classList.contains('open');
  const openMenu = ()=>{ nav.classList.add('open'); btn.textContent='✕'; btn.setAttribute('aria-expanded','true'); };
  const closeMenu= ()=>{ nav.classList.remove('open'); btn.textContent='☰'; btn.setAttribute('aria-expanded','false'); };

  btn.addEventListener('click',(e)=>{
    e.stopPropagation();
    isOpen() ? closeMenu() : openMenu();
  });

  // 点击菜单外部关闭
  document.addEventListener('click',(ev)=>{
    if(isOpen() && !nav.contains(ev.target) && ev.target!==btn){
      closeMenu();
    }
  });

  // 点击菜单内链接后自动关闭
  nav.addEventListener('click',(ev)=>{
    if(ev.target.tagName==='A') closeMenu();
  });

  // ESC 关闭
  document.addEventListener('keydown',(ev)=>{
    if(ev.key==='Escape' && isOpen()) closeMenu();
  });

  function sync(){
    if(window.innerWidth<=640){
      if(!isOpen()) closeMenu();
    }else{
      closeMenu();
    }
  }
  window.addEventListener('resize',sync); sync();
});