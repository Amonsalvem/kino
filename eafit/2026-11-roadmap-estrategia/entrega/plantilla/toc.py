import uno,sys,time,subprocess,os
from com.sun.star.beans import PropertyValue
p=subprocess.Popen(['soffice','--headless','--invisible','--norestore','--accept=socket,host=localhost,port=2002;urp;'])
ctx=None
for i in range(40):
    try:
        local=uno.getComponentContext();res=local.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver',local)
        ctx=res.resolve('uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext');break
    except Exception: time.sleep(0.5)
smgr=ctx.ServiceManager;desk=smgr.createInstanceWithContext('com.sun.star.frame.Desktop',ctx)
def pv(n,v):
    x=PropertyValue();x.Name=n;x.Value=v;return x
src=os.path.abspath(sys.argv[1]);dst=os.path.abspath(sys.argv[2])
doc=desk.loadComponentFromURL(uno.systemPathToFileUrl(src),'_blank',0,(pv('Hidden',True),))
idx=doc.getDocumentIndexes();print('indexes',idx.getCount())
for i in range(idx.getCount()): idx.getByIndex(i).update()
doc.refresh()
doc.storeToURL(uno.systemPathToFileUrl(dst),(pv('FilterName','MS Word 2007 XML'),))
doc.storeToURL(uno.systemPathToFileUrl(dst.replace('.docx','.pdf')),(pv('FilterName','writer_pdf_Export'),))
doc.close(True)
try: desk.terminate()
except Exception: pass
p.wait(timeout=30);print('done')
