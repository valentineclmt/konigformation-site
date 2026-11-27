/* Konig Formation — interactions légères, sans dépendance */
(function(){
  var d=document;
  function $(s,c){return (c||d).querySelector(s)}
  function $$(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))}

  /* Méga-menu Formations */
  var mb=$('[data-mega-btn]'), mega=$('[data-mega]');
  if(mb&&mega){
    var setMega=function(o){mega.classList.toggle('open',o);mb.setAttribute('aria-expanded',o)};
    mb.addEventListener('click',function(e){e.stopPropagation();setMega(!mega.classList.contains('open'))});
    d.addEventListener('click',function(e){if(!mega.contains(e.target))setMega(false)});
    d.addEventListener('keydown',function(e){if(e.key==='Escape')setMega(false)});
  }

  /* Menu mobile */
  var bg=$('[data-burger]'), mn=$('[data-mnav]');
  if(bg&&mn){
    bg.addEventListener('click',function(){var o=!mn.classList.contains('open');mn.classList.toggle('open',o);bg.setAttribute('aria-expanded',o);d.body.style.overflow=o?'hidden':''});
    $$('a',mn).forEach(function(a){a.addEventListener('click',function(){mn.classList.remove('open');bg.setAttribute('aria-expanded',false);d.body.style.overflow=''})});
  }

  /* Apparition au défilement + sommaire latéral actif */
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
    $$('.rv').forEach(function(el){io.observe(el)});
    var links=$$('.toc-side a[href^="#"]');
    if(links.length){
      var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
      var so=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.remove('on')});var a=map[e.target.id];if(a)a.classList.add('on')}})},{rootMargin:'-40% 0px -55% 0px'});
      Object.keys(map).forEach(function(id){var s=d.getElementById(id);if(s)so.observe(s)});
    }
  } else { $$('.rv').forEach(function(el){el.classList.add('in')}); }

  /* Tout déplier / replier les modules */
  $$('[data-toggle-modules]').forEach(function(b){b.addEventListener('click',function(){
    var ds=$$('details',b.closest('.block')), open=!ds.every(function(x){return x.open});
    ds.forEach(function(x){x.open=open});b.textContent=open?'Tout replier':'Tout déplier';
  })});
})();
/* Vidéos : pas d'animation si l'utilisateur préfère réduire les mouvements */
(function(){
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches){
    document.querySelectorAll('video[autoplay]').forEach(function(v){v.removeAttribute('autoplay');v.pause();v.setAttribute('controls','')});
  }
})();
