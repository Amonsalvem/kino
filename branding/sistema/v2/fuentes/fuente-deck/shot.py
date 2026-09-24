import sys
from playwright.sync_api import sync_playwright
f=sys.argv[1]; tema=sys.argv[2] if len(sys.argv)>2 else 'oscuro'; W=int(sys.argv[3]) if len(sys.argv)>3 else 1440; H=int(sys.argv[4]) if len(sys.argv)>4 else 900
with sync_playwright() as p:
  b=p.chromium.launch(args=['--use-gl=swiftshader','--enable-unsafe-swiftshader']); pg=b.new_page(viewport={'width':W,'height':H})
  errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)[:300])); pg.on('console', lambda m: m.type=='error' and errs.append(m.text[:200]))
  pg.add_init_script(f"try{{localStorage.setItem('kino-tema','{tema}')}}catch(e){{}}")
  pg.goto('file://'+f); pg.wait_for_timeout(3200)
  n=pg.evaluate("document.querySelectorAll('section').length")
  for i in range(n):
    pg.evaluate(f"document.querySelectorAll('section')[{i}].scrollIntoView()"); pg.wait_for_timeout(2600)
    pg.screenshot(path=f'/tmp/k-{tema}-{W}-{i+1:02d}.png')
  ov=pg.evaluate("document.documentElement.scrollWidth - innerWidth")
  hs=pg.evaluate("[...document.querySelectorAll('section')].map((s,i)=>[i+1,Math.round(s.getBoundingClientRect().height)]).filter(x=>x[1]>innerHeight+60)")
  print('errores',errs[:10]); print('desborde horizontal',ov); print('láminas más altas que la pantalla',hs)
  b.close()
