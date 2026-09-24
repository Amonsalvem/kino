/* Kino · Sistema de marca · navegación.
   Rutas por ancla simple: #plataforma, #plataforma.problema, #glosario.pase.
   Solo se muestra una sección a la vez; las demás no pintan ni animan. */
(function(){
  'use strict';
  var vistas=[].slice.call(document.querySelectorAll('.vista'));
  var porId={}; vistas.forEach(function(v){porId[v.id]=v;});
  var orden=vistas.filter(function(v){return v.dataset.num;});
  var nav=document.getElementById('nav'), res=document.getElementById('resultados'), q=document.getElementById('q');
  var indice=document.getElementById('indice'), donde=document.getElementById('donde');
  var guardar=function(k,v){try{localStorage.setItem(k,v);}catch(e){}};
  var leer=function(k){try{return localStorage.getItem(k);}catch(e){return null;}};

  /* Tema: oscuro canónico. El claro solo por elección. */
  var raiz=document.documentElement;
  function tema(t){raiz.setAttribute('data-tema',t);var b=document.getElementById('tema');if(b){b.setAttribute('aria-pressed',t==='claro');b.lastChild.textContent=t==='claro'?' Tema oscuro':' Tema claro';}}
  tema(leer('kino-tema')||(raiz.getAttribute('data-theme')==='light'?'claro':'oscuro'));
  document.getElementById('tema').addEventListener('click',function(){var t=raiz.getAttribute('data-tema')==='claro'?'oscuro':'claro';tema(t);guardar('kino-tema',t);});

  /* Índice: grupos, secciones y subsecciones, construido desde el contenido. */
  var grupos={};
  orden.forEach(function(v){(grupos[v.dataset.grupo]=grupos[v.dataset.grupo]||[]).push(v);});
  var h='<ol><li><a href="#inicio" data-v="inicio"><span class="n">·</span>Inicio</a></li><li><a href="#conocer" data-v="conocer"><span class="n">·</span>Conocer Kino</a></li><li><a href="#usar" data-v="usar"><span class="n">·</span>Usar la marca</a></li></ol>';
  Object.keys(grupos).forEach(function(g){
    h+='<p class="nav-grupo">'+g+'</p><ol>';
    grupos[g].forEach(function(v){
      var subs=[].slice.call(v.querySelectorAll('.sub[id]'));
      var obra=v.querySelector('.obra')?'<span class="estado" title="En construcción">en obra</span>':'';
      h+='<li><a href="#'+v.id+'" data-v="'+v.id+'"><span class="n">'+v.dataset.num+'</span>'+v.dataset.titulo+obra+'</a>';
      if(subs.length){h+='<ol class="sub-nav" data-de="'+v.id+'" hidden>'+subs.map(function(s){return '<li><a href="#'+s.id+'" data-s="'+s.id+'">'+s.dataset.titulo+'</a></li>';}).join('')+'</ol>';}
      h+='</li>';
    });
    h+='</ol>';
  });
  h+='<p class="nav-grupo">Consulta</p><ol><li><a href="#glosario" data-v="glosario"><span class="n">A–Z</span>Glosario</a></li></ol>';
  nav.innerHTML=h;

  /* Mapa de «Usar la marca». */
  var mapa=document.querySelector('[data-mapa]');
  if(mapa){mapa.innerHTML=orden.map(function(v){var que=v.querySelector('.lector dd');return '<a href="#'+v.id+'"><span class="n">'+v.dataset.num+' · '+v.dataset.grupo+'</span><strong>'+v.dataset.titulo+'</strong><p>'+(que?que.textContent:'')+'</p></a>';}).join('');}

  /* Anterior y siguiente. */
  orden.forEach(function(v,i){
    var a=orden[i-1],s=orden[i+1],p=document.createElement('nav');p.className='pasar';p.setAttribute('aria-label','Secciones vecinas');
    p.innerHTML=(a?'<a href="#'+a.id+'"><small>Anterior</small><strong>'+a.dataset.num+' '+a.dataset.titulo+'</strong></a>':'')+(s?'<a class="sig" href="#'+s.id+'"><small>Siguiente</small><strong>'+s.dataset.num+' '+s.dataset.titulo+'</strong></a>':'<a class="sig" href="#glosario"><small>Siguiente</small><strong>Glosario</strong></a>');
    v.appendChild(p);
  });

  /* Cascada: índice de cada pieza para el escalonado. */
  vistas.forEach(function(v){['.abre','.puerta','.evi','.ruta li','.mapa-sitio a'].forEach(function(sel){[].forEach.call(v.querySelectorAll(sel),function(el,i){el.style.setProperty('--i',Math.min(i,8));});});});

  /* Router. */
  var actual=null;
  function ir(hash,desplazar){
    var id=(hash||'').replace(/^#/,'')||'inicio';
    var vid=id.split('.')[0]; if(!porId[vid]){vid='inicio';id='inicio';}
    var v=porId[vid];
    if(actual!==v){
      if(actual){actual.hidden=true;actual.classList.remove('entra');}
      v.hidden=false; void v.offsetWidth; v.classList.add('entra'); actual=v;
      document.title=(vid==='inicio'?'':v.dataset.titulo+' · ')+'Kino · Sistema de marca';
      [].forEach.call(nav.querySelectorAll('[data-v]'),function(a){if(a.dataset.v===vid)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
      [].forEach.call(nav.querySelectorAll('.sub-nav'),function(o){o.hidden=o.dataset.de!==vid;});
      if(donde)donde.textContent=(v.dataset.num?v.dataset.num+' ':'')+v.dataset.titulo;
    }
    var destino=id!==vid?document.getElementById(id):null;
    if(destino){destino.scrollIntoView({block:'start'});}
    else if(desplazar!==false){window.scrollTo(0,0);var h1=v.querySelector('h1');if(h1){h1.setAttribute('tabindex','-1');h1.focus({preventScroll:true});}}
    cerrarIndice(); marcarSub(); avance();
  }
  window.addEventListener('hashchange',function(){ir(location.hash);});

  /* Subsección activa y barra de progreso de lectura. */
  function marcarSub(){
    if(!actual)return; var subs=actual.querySelectorAll('.sub[id]'),act=null;
    [].forEach.call(subs,function(s){if(s.getBoundingClientRect().top<window.innerHeight*.35)act=s;});
    [].forEach.call(nav.querySelectorAll('[data-s]'),function(a){if(act&&a.dataset.s===act.id)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
  }
  var bar=document.querySelector('.progreso i');
  function avance(){var d=document.documentElement,m=d.scrollHeight-window.innerHeight;bar.style.setProperty('--p',m>0?Math.min(1,window.scrollY/m):1);}
  var pend=false; window.addEventListener('scroll',function(){if(pend)return;pend=true;requestAnimationFrame(function(){pend=false;avance();marcarSub();});},{passive:true});

  /* Índice en pantallas angostas. */
  var btn=document.getElementById('abrir-indice');
  function cerrarIndice(){if(indice.dataset.abierto==='true'){indice.dataset.abierto='false';btn.setAttribute('aria-expanded','false');}}
  btn.addEventListener('click',function(){var a=indice.dataset.abierto!=='true';indice.dataset.abierto=a;btn.setAttribute('aria-expanded',a);if(a)q.focus();});

  /* Búsqueda sobre títulos de sección, subsección y glosario. */
  var fuente=[];
  vistas.forEach(function(v){fuente.push({t:v.dataset.titulo,d:v.dataset.num?'Sección '+v.dataset.num:'Página',h:v.id});
    [].forEach.call(v.querySelectorAll('.sub[id]'),function(s){fuente.push({t:s.dataset.titulo,d:v.dataset.titulo,h:s.id});});});
  [].forEach.call(document.querySelectorAll('[data-glosario]'),function(g){fuente.push({t:g.dataset.titulo,d:'Glosario · '+g.querySelector('dd').textContent,h:g.id});});
  var norm=function(s){return s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();};
  var sel=-1,vis=[];
  function buscar(){
    var t=norm(q.value.trim()); sel=-1;
    if(!t){res.innerHTML='';res.hidden=true;return;}
    vis=fuente.filter(function(f){return norm(f.t+' '+f.d).indexOf(t)>-1;}).sort(function(a,b){return (norm(a.t).indexOf(t)===0?0:1)-(norm(b.t).indexOf(t)===0?0:1);}).slice(0,8);
    res.hidden=false;
    res.innerHTML=vis.length?vis.map(function(f,i){return '<li><a id="r'+i+'" href="#'+f.h+'">'+f.t+'<small>'+f.d.slice(0,70)+'</small></a></li>';}).join(''):'<li class="vacio">Sin resultados para «'+q.value.replace(/</g,'')+'». Prueba con «Pase» o «color».</li>';
  }
  q.addEventListener('input',buscar);
  q.addEventListener('keydown',function(e){
    var as=res.querySelectorAll('a');
    if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();if(!as.length)return;sel=(sel+(e.key==='ArrowDown'?1:-1)+as.length)%as.length;[].forEach.call(as,function(a,i){a.setAttribute('aria-selected',i===sel);});q.setAttribute('aria-activedescendant','r'+sel);}
    else if(e.key==='Enter'){var a=as[sel<0?0:sel];if(a){location.hash=a.getAttribute('href');q.value='';buscar();}}
    else if(e.key==='Escape'){q.value='';buscar();q.blur();}
  });
  res.addEventListener('click',function(){q.value='';buscar();});
  document.addEventListener('keydown',function(e){
    if(e.key==='/'&&document.activeElement!==q&&!/input|textarea/i.test(document.activeElement.tagName)){e.preventDefault();if(window.matchMedia('(max-width:60rem)').matches){indice.dataset.abierto='true';btn.setAttribute('aria-expanded','true');}q.focus();}
    if(e.key==='Escape')cerrarIndice();
  });

  /* Demos de movimiento: corren al mostrar la sección y con «Repetir». Las secciones ocultas no animan. */
  function correr(fig){fig.classList.remove('corre');void fig.offsetWidth;fig.classList.add('corre');}
  function correrEn(v){[].forEach.call(v.querySelectorAll('[data-demo]'),correr);}
  document.addEventListener('click',function(e){
    var r=e.target.closest('[data-repetir]');if(r){var f=r.closest('[data-demo]');if(f)correr(f);}
    var m=e.target.closest('[data-mov-reducido]');
    if(m){var on=raiz.getAttribute('data-mov')!=='reducido';if(on)raiz.setAttribute('data-mov','reducido');else raiz.removeAttribute('data-mov');
      [].forEach.call(document.querySelectorAll('[data-mov-reducido]'),function(b){b.setAttribute('aria-pressed',on);b.textContent=on?'Ver con movimiento completo':'Ver en movimiento reducido';});
      if(actual)correrEn(actual);}
    /* PNG a partir del SVG descargable. */
    var p=e.target.closest('[data-png]');
    if(p){var img=new Image(),w=+p.dataset.ancho,h=+p.dataset.alto;img.onload=function(){var c=document.createElement('canvas');c.width=w;c.height=h;
      c.getContext('2d').drawImage(img,0,0,w,h);c.toBlob(function(b){var a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=p.dataset.png;document.body.appendChild(a);a.click();
      setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},500);},'image/png');};img.src=p.dataset.src;}
  });
  window.addEventListener('hashchange',function(){if(actual)correrEn(actual);});

  ir(location.hash,false);
  if(actual)correrEn(actual);
})();
