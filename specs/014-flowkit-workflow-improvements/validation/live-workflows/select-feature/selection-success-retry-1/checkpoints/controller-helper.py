from pathlib import Path
import json,subprocess,sys,hashlib,datetime,shutil,re
p=Path.cwd();sf=Path('/tmp/t082retry-state.json');g=json.loads(Path('/tmp/t082retry-bootstrap.json').read_text());action=sys.argv[1]
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def run(args,data=None):return json.loads(subprocess.check_output(args,input=None if data is None else json.dumps(data).encode()))
def call(name,args,data):return run([sys.executable,'.specify/flow-kit/scripts/python/'+name+'.py',*args],data)
now=run(['bash','.specify/flow-kit/scripts/bootstrap.sh',str(p),'speckit-flow-select-feature','flow-kit-select-feature']);assert now['sha256']==g['sha256'] and now['installation_fingerprints']==g['installation_fingerprints']
def flatten(nodes):
 out=[]
 for n in nodes:
  out.append(n)
  for branch in n.get('cases',{}).values():out.extend(flatten(branch))
  if 'default' in n:out.extend(flatten(n['default']))
 return out
nodes=flatten(g['steps'])
def snapshot():return {q.relative_to(p).as_posix():sha(q) for q in p.rglob('*') if q.is_file() and not any(x in q.parts for x in ['.git','.flowkit-test','flow-controllers'])}
def journal(event,**kw):
 q=h/'journal.jsonl';count=len(q.read_text().splitlines()) if q.exists() else 0
 with q.open('a') as f:f.write(json.dumps({'sequence':count+1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':event,**kw})+'\n')
def save():sf.write_text(json.dumps(s))
def changes():a=snapshot();return [n for n in sorted(set(a)|set(s['before'])) if a.get(n)!=s['before'].get(n)]
if action=='init':
 root=p.parents[1];source=json.loads((root/'.flowkit-test/coordinator-source-digests.json').read_text());assert sha(Path(g['source_path']))==source['sha256']['workflows/speckit-flow-select-feature/workflow.yml'];assert sha(Path('.specify/flow-kit/controller-protocol.md'))==source['sha256']['controllers/flow-kit/controller-protocol.md'];profiles={q.as_posix():sha(q) for q in Path('.codex/agents').glob('*.toml')};assert len(profiles)==8 and all(source['sha256'][n]==v for n,v in profiles.items());r=call('recovery',['create','--project',str(p)],{'workflow':g,'fingerprints':g['installation_fingerprints'],'assignments':g['agent_assignments'],'preflight_passed':True});rid=r['summary']['run_id'];h=Path('.flowkit-test/selection-success-retry-1')/rid;h.mkdir(parents=True);s={'run_id':rid,'summary':r['summary_path'],'history':str(h),'before':snapshot(),'profiles':profiles,'outputs':{},'statuses':{},'gates':[],'branches':[],'graph':g};save();(h/'before-hashes.json').write_text(json.dumps(s['before'],indent=2));(h/'installed-graph.json').write_text(json.dumps(g,indent=2));(h/'source-digests.json').write_text(json.dumps(source,indent=2));shutil.copy2(__file__,h/'controller-helper.py');shutil.copy2('.specify/memory/roadmap.md',h/'roadmap-before.md');shutil.copy2('.specify/feature.json',h/'pointer-before.json');journal('preflight-and-run-created');print(rid);sys.exit()
s=json.loads(sf.read_text());h=Path(s['history']);sid=sys.argv[2];n=next(n for n in nodes if n['id']==sid)
def render(t):
 for k,v in g['resolved_inputs'].items():t=t.replace('{{ inputs.'+k+' }}',v)
 for step,out in s['outputs'].items():
  for k,v in out.items():t=t.replace('{{ steps.'+step+'.output.'+k+' }}',v if isinstance(v,str) else json.dumps(v))
 assert '{{' not in t;return t
if action=='step':
 status=sys.argv[3]
 if status=='running':(h/(sid+'-prompt.txt')).write_text(render(n.get('prompt',n.get('input',{}).get('args',''))))
 if status=='completed' and n.get('flow_kit',{}).get('delegated'):
  q=h/(sid+'-output.json');v=json.loads(q.read_text());assert isinstance(v,dict);s['outputs'][sid]=v;journal('actual-child-checkpoint-verified',step_id=sid,sha256=sha(q))
 journal('before-step-update',step_id=sid,status=status);call('recovery',['step','--summary',s['summary'],'--step-id',sid,'--status',status],{'changed_files':changes()});s['statuses'][sid]=status;save();journal('step-update-succeeded',step_id=sid,status=status);print(json.dumps({'step':sid,'status':status}));sys.exit()
if action=='gate':
 gate={**n,'message':render(n['message'])};opts=n['options'];m=re.fullmatch(r'{{ steps\.([a-z0-9-]+)\.output\.([a-z_]+) }}',opts[0]) if len(opts)==1 else None
 if m:opts=s['outputs'][m[1]][m[2]]
 assert isinstance(opts,list) and len(opts)==len(set(opts)) and all(isinstance(x,str) and x for x in opts);gate['options']=opts;root=p.parents[1];approval=json.loads((root/'.flowkit-test/operator-decisions.json').read_text());supp=approval['supplemental_approvals'][-1];assert supp['status']=='approved' and sha(root/'.flowkit-test/supplemental-decisions.md')==supp['packet_sha256']
 if sid=='select-roadmap-feature':
  chosen=[x for x in opts if re.match(r'^(?:Feature )?802\b',x)];assert len(chosen)==1;answer=chosen[0];provenance=approval['provenance']
 else:
  prepared=s['outputs']['prepare-feature-selection'];patch=prepared['proposed_patch'];assert isinstance(patch,str);expected='a69df484c7035fba0b7048886c00aa0d497cb244870774b3750b09fe7d38b8d5';assert hashlib.sha256(patch.encode()).hexdigest()==expected==supp['patch_sha256']['selection.patch'];assert prepared['feature_directory']=='specs/802-normalize-text';payload=prepared['feature_json'];payload=json.loads(payload) if isinstance(payload,str) else payload;current=json.loads(Path('.specify/feature.json').read_text());assert payload==dict(current,feature_directory='specs/802-normalize-text');answer='approve';provenance=supp['provenance'];(h/'approved-selection.patch').write_bytes(patch.encode())
 raw={'gate':gate,'answer':answer,'approval_provenance':provenance};q=h/(sid+'-request.json');q.write_text(json.dumps(raw,indent=2)+'\n');journal('gate-request-persisted',step_id=sid,sha256=sha(q));result=call('controller',['gate'],{'gate':gate,'answer':answer});(h/(sid+'-output.json')).write_text(json.dumps(result,indent=2)+'\n');s['outputs'][sid]=result;s['gates'].append({'step_id':sid,'choice':result['choice']});save();journal('gate-validated',step_id=sid,choice=result['choice']);print(json.dumps({'message':gate['message'],'options':opts,'validated_choice':result['choice']}));sys.exit()
if action=='branch':
 choice=render(n['expression']);r=call('controller',['branch'],{'switch':n,'choice':choice});(h/(sid+'-branch.json')).write_text(json.dumps(r,indent=2)+'\n');s['branches'].append({'step_id':sid,'choice':choice,'step_ids':[x['id'] for x in r['steps']]});save();journal('branch-validated',step_id=sid,choice=choice);print(json.dumps({'choice':choice,'selected_steps':[x['id'] for x in r['steps']]}));sys.exit()
raise ValueError('unknown action')
