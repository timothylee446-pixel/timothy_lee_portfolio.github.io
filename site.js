(function(){
var root=document.documentElement;

// Draft mode: placeholders for missing files and [bracketed] notes show when previewing locally or with ?drafts in the URL.
// On the live site they stay hidden so visitors only see finished content.
var drafts=/[?&]drafts\b/.test(location.search)||location.protocol==='file:'||/^(localhost|127\.0\.0\.1)$/.test(location.hostname);
if(drafts) root.classList.add('show-drafts');

// Shows a labeled placeholder when an image or video file has not been added yet.
function missing(el){
  var fig=el.closest('figure');
  if(el.dataset.pending){
    var p=document.createElement('div');
    p.className='missing pending';
    p.innerHTML='<span class="pending-icon" aria-hidden="true"></span><strong></strong>';
    p.querySelector('strong').textContent=el.dataset.pending;
    if(drafts) p.appendChild(document.createTextNode('Add file: '+el.dataset.name));
    el.replaceWith(p);
    return;
  }
  if(!drafts){
    if(fig){ fig.hidden=true; var g=fig.parentElement; if(g.classList.contains('gallery')&&!g.querySelector('figure:not([hidden])')) g.hidden=true; }
    else el.hidden=true;
    return;
  }
  var d=document.createElement('div');
  d.className='missing';
  d.innerHTML='<strong>Image coming soon</strong>';
  d.appendChild(document.createTextNode('Add file: '+el.dataset.name));
  el.replaceWith(d);
}
document.querySelectorAll('img[data-name]').forEach(function(img){
  img.addEventListener('error',function(){missing(img)});
  if(img.complete && img.naturalWidth===0) missing(img);
});
document.querySelectorAll('video[data-name]').forEach(function(v){
  v.addEventListener('error',function(){missing(v)});
});

// Looping product clips stay still for visitors who prefer reduced motion.
if(matchMedia('(prefers-reduced-motion: reduce)').matches){
  document.querySelectorAll('.loop video').forEach(function(v){ v.removeAttribute('autoplay'); v.pause(); v.controls=true; });
}

// Card and hero thumbnails fall back to the patterned panel behind them.
document.querySelectorAll('img[data-thumb]').forEach(function(img){
  function gone(){ img.remove(); }
  img.addEventListener('error',gone);
  if(img.complete && img.naturalWidth===0) gone();
});

// Header border once the page scrolls; reading progress bar on case-study pages.
var top=document.querySelector('.top');
var bar=null;
if(document.querySelector('.project')){
  bar=document.createElement('div'); bar.className='progress'; bar.setAttribute('aria-hidden','true');
  document.body.appendChild(bar);
}
var ticking=false;
function onScroll(){
  ticking=false;
  var y=window.scrollY;
  if(top) top.classList.toggle('scrolled',y>8);
  if(bar){ var h=document.documentElement.scrollHeight-innerHeight; bar.style.transform='scaleX('+(h>0?Math.min(1,y/h):0)+')'; }
}
addEventListener('scroll',function(){ if(!ticking){ ticking=true; requestAnimationFrame(onScroll); } },{passive:true});
onScroll();

// Highlight the current section in the table of contents.
var tocLinks=[].slice.call(document.querySelectorAll('.toc a'));
if(tocLinks.length && 'IntersectionObserver' in window){
  var heads=tocLinks.map(function(a){ return document.getElementById(a.hash.slice(1)); });
  function setActive(){
    var cur=0;
    heads.forEach(function(h,i){ if(h && h.getBoundingClientRect().top<innerHeight*.35) cur=i; });
    tocLinks.forEach(function(a,i){ a.classList.toggle('active',i===cur); });
  }
  addEventListener('scroll',function(){ requestAnimationFrame(setActive); },{passive:true});
  setActive();
}

// Fade content in as it scrolls into view. The class is removed afterwards so hover effects keep working.
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
if(!reduce && 'IntersectionObserver' in window){
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(!e.isIntersecting) return;
      var el=e.target; io.unobserve(el);
      el.classList.add('in');
      setTimeout(function(){ el.classList.remove('reveal','in'); },900);
    });
  },{rootMargin:'0px 0px -8% 0px'});
  document.querySelectorAll('.card,.xp,.stat,.pager a,.prose>figure,.prose>.gallery,.cover,.about-body,.hero-text').forEach(function(el,i){
    el.classList.add('reveal');
    el.style.transitionDelay=(el.matches('.card,.stat')?(i%3)*70:0)+'ms';
    io.observe(el);
  });
}

// Lightbox for figures on case-study pages.
var imgs=function(){ return [].slice.call(document.querySelectorAll('.prose figure:not([hidden]) img, .cover img')).filter(function(i){ return i.isConnected && i.naturalWidth>0; }); };
if(document.querySelector('.prose') && window.HTMLDialogElement){
  var dlg=document.createElement('dialog'); dlg.className='lb'; dlg.setAttribute('aria-label','Image viewer');
  dlg.innerHTML='<div class="lb-in"><img alt=""><p></p><span class="lb-count"></span></div>'+
    '<button class="lb-close" aria-label="Close">✕</button><button class="lb-prev" aria-label="Previous image">←</button><button class="lb-next" aria-label="Next image">→</button>';
  document.body.appendChild(dlg);
  var big=dlg.querySelector('img'), cap=dlg.querySelector('p'), count=dlg.querySelector('.lb-count'), list=[], idx=0;
  function show(i){
    idx=(i+list.length)%list.length;
    var src=list[idx], fc=src.closest('figure').querySelector('figcaption');
    big.src=src.currentSrc||src.src; big.alt=src.alt;
    cap.textContent=fc?fc.textContent:''; cap.hidden=!fc;
    count.textContent=(idx+1)+' / '+list.length;
    var multi=list.length>1;
    dlg.querySelector('.lb-prev').hidden=!multi; dlg.querySelector('.lb-next').hidden=!multi;
  }
  document.addEventListener('click',function(e){
    var t=e.target;
    if(t.tagName==='IMG' && t.closest('.prose figure, .cover')){
      list=imgs(); var i=list.indexOf(t); if(i<0) return;
      show(i); dlg.showModal();
    }
  });
  dlg.addEventListener('click',function(e){
    if(e.target.closest('.lb-close')||e.target===dlg||e.target.classList.contains('lb-in')) dlg.close();
    else if(e.target.closest('.lb-prev')) show(idx-1);
    else if(e.target.closest('.lb-next')) show(idx+1);
  });
  dlg.addEventListener('keydown',function(e){
    if(e.key==='ArrowLeft') show(idx-1);
    if(e.key==='ArrowRight') show(idx+1);
  });
}
})();
