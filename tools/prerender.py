"""Riempie index.html con il contenuto gia' calcolato dai dati salvati,
cosi' la pagina e' leggibile anche dove JavaScript non gira (anteprima file su iPhone).
Uso: python3 tools/prerender.py   (richiede node)
"""
import re,subprocess,json,sys,os,tempfile
TMP=os.path.join(tempfile.gettempdir(),'aurora_prerender.js')
path=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(__file__),'..','index.html')
s=open(path).read()
js=re.search(r'<script>(.*)</script>',s,re.S).group(1).split('const PANELS=')[0]
shim="""
const _els={};function _el(id){return _els[id]||(_els[id]={id,innerHTML:'',className:'',textContent:'',hidden:false,addEventListener(){},querySelectorAll(){return []},querySelector(){return null},setAttribute(){}})}
globalThis.document={getElementById:_el,querySelectorAll:()=>[],querySelector:()=>null,documentElement:{classList:{add(){}}},body:{appendChild(){}}};
globalThis.window=globalThis;globalThis.location={hash:''};
"""
tail="""
renderAll();
console.log(JSON.stringify(Object.fromEntries(['stats','srctext','p-aurora','p-gironi','p-gen','p-fin'].map(k=>[k,_el(k).innerHTML]))));
"""
open(TMP,'w').write(shim+js+tail)
out=json.loads(subprocess.check_output(['node',TMP]))
# replace inner content of known containers (they are emptied/filled each build)
s=re.sub(r'(<div class="stats" id="stats">).*?(</div>\s*<div class="src">)',lambda m:m.group(1)+out['stats']+m.group(2),s,count=1,flags=re.S)
s=re.sub(r'(<span id="srctext">).*?(</span>)',lambda m:m.group(1)+out['srctext']+m.group(2),s,count=1,flags=re.S)
for k in ['p-aurora','p-gironi','p-gen','p-fin']:
    s=re.sub(r'(<section class="panel" id="'+k+r'")[^>]*>.*?(</section>)',lambda m:m.group(1)+' data-static>'+out[k]+m.group(2),s,count=1,flags=re.S)
open(path,'w').write(s)
print({k:len(v) for k,v in out.items()})
