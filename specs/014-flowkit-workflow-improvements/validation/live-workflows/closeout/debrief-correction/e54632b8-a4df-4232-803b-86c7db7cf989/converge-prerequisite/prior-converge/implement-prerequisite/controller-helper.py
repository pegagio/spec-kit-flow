from pathlib import Path
import json,subprocess,sys,hashlib,datetime,shutil
p=Path.cwd();sf=Path('/tmp/t087impl-state.json');g=json.loads(Path('/tmp/t087impl-bootstrap.json').read_text());action=sys.argv[1]
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def run(args,data=None):return json.loads(subprocess.check_output(args,input=None if data is None else json.dumps(data).encode()))
def call(name,args,data):return run([sys.executable,'.specify/flow-kit/scripts/python/'+name+'.py',*args],data)
now=run(['bash','.specify/flow-kit/scripts/bootstrap.sh',str(p),'speckit-flow-implement','flow-kit-implement','--input','feature_context=Feature 802: specs/802-normalize-text']);assert now['sha256']==g['sha256'] and now['installation_fingerprints']==g['installation_fingerprints']
nodes=[g['steps'][0],*g['steps'][1]['steps'],*g['steps'][2:]];body=[n['id'] for n in g['steps'][1]['steps']]
def snapshot():return {q.relative_to(p).as_posix():sha(q) for q in p.rglob('*') if q.is_file() and not any(x in q.parts for x in ['.git','.flowkit-test','flow-controllers','__pycache__'])}
def journal(event,**kw):
 q=h/'journal.jsonl';count=len(q.read_text().splitlines()) if q.exists() else 0
 with q.open('a') as f:f.write(json.dumps({'sequence':count+1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':event,**kw})+'\n')
def save():sf.write_text(json.dumps(s))
def changes():a=snapshot();return [n for n in sorted(set(a)|set(s['before'])) if a.get(n)!=s['before'].get(n)]
if action=='init':
 root=p.parents[1];src=json.loads((root/'.flowkit-test/coordinator-source-digests.json').read_text());assert sha(Path(g['source_path']))==src['sha256']['workflows/speckit-flow-implement/workflow.yml'];assert sha(Path('.specify/flow-kit/controller-protocol.md'))==src['sha256']['controllers/flow-kit/controller-protocol.md'];profiles={q.as_posix():sha(q) for q in Path('.codex/agents').glob('*.toml')};assert len(profiles)==8 and all(src['sha256'][n]==v for n,v in profiles.items());baseline=json.loads(Path('.flowkit-test/implement-preflight/validation.json').read_text());assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==baseline['baseline_oid'];r=call('recovery',['create','--project',str(p)],{'workflow':g,'fingerprints':g['installation_fingerprints'],'assignments':g['agent_assignments'],'preflight_passed':True});rid=r['summary']['run_id'];h=Path('.flowkit-test/closeout-prerequisite-implement')/rid;h.mkdir(parents=True);s={'run_id':rid,'summary':r['summary_path'],'history':str(h),'graph':g,'before':snapshot(),'profiles':profiles,'baseline':baseline,'outputs':{},'passes':[],'statuses':{},'initial_assessment':None,'answers':[]};save();(h/'before-hashes.json').write_text(json.dumps(s['before'],indent=2));(h/'installed-graph.json').write_text(json.dumps(g,indent=2));(h/'source-digests.json').write_text(json.dumps(src,indent=2));shutil.copy2(__file__,h/'controller-helper.py');journal('preflight-and-run-created');print(rid);sys.exit()
s=json.loads(sf.read_text());h=Path(s['history']);i=int(sys.argv[2]);d=h/('initial' if i==0 else f'pass{i}');d.mkdir(exist_ok=True)
if action=='step':
 sid=sys.argv[3];status=sys.argv[4];n=next(n for n in nodes if n['id']==sid)
 if sid=='implement-eligible-work' and status=='running':assert (s['passes'][-1]['route']['action'] if s['passes'] else s['initial_route']['route']['action'])=='continue'
 if sid=='assess-implementation-after-pass' and status=='running':assert s['statuses'].get(f'{i}:implement-eligible-work')=='completed'
 if sid=='report-implementation-outcome':assert (s['passes'][-1]['route']['action'] if s['passes'] else s['initial_route']['route']['action'])!='continue'
 if status=='running':
  t=n.get('prompt',n.get('input',{}).get('args','')).replace('{{ inputs.feature_context }}',g['resolved_inputs']['feature_context']);assert '{{' not in t
  if sid=='implement-eligible-work' and i>1:
   f=json.loads((h/f'pass{i-1}/review-findings.json').read_text());t+=' Exact unchanged previous independent review findings: '+json.dumps(f,sort_keys=True)
  (d/(sid+'-prompt.txt')).write_text(t)
 if status=='completed' and n.get('flow_kit',{}).get('delegated'):
  q=d/(sid+'-output.json');v=json.loads(q.read_text());assert isinstance(v,dict);s['outputs'][sid]=v;journal('actual-checkpoint-persistence-verified',iteration=i,step_id=sid,sha256=sha(q))
  if sid=='assess-implementation-after-pass':
   q2=d/'review-findings.json';f=json.loads(q2.read_text());assert isinstance(f.get('findings'),list);journal('separate-review-findings-persistence-verified',iteration=i,sha256=sha(q2))
 journal('before-step-update',iteration=i,step_id=sid,status=status);call('recovery',['step','--summary',s['summary'],'--step-id',sid,'--status',status],{'changed_files':changes()});s['statuses'][f'{i}:{sid}']=status;save();journal('step-update-succeeded',iteration=i,step_id=sid,status=status);print(json.dumps({'iteration':i,'step':sid,'status':status}));sys.exit()
if action=='route-initial':
 assert s['statuses'].get('0:assess-implementation-state')=='completed';a=s['outputs']['assess-implementation-state'];cmd=['assessment','--project',str(p)]
 for sid in body:cmd+=['--loop-body-step',sid]
 journal('before-initial-assessment-validation');r=call('controller',cmd,a);(d/'validated-route.json').write_text(json.dumps(r,indent=2)+'\n');s['initial_assessment']=a;s['initial_route']=r;save();journal('initial-assessment-validated',action=r['route']['action']);print(json.dumps(r));sys.exit()
if action=='route':
 assert s['statuses'].get(f'{i}:assess-implementation-after-pass')=='completed';a=s['outputs']['assess-implementation-after-pass'];payload={'assessment':a,'previous_assessment':s['passes'][-1]['assessment'] if s['passes'] else s['initial_assessment']};cmd=['route-loop','--project',str(p),'--iteration',str(i),'--max-iterations','5']
 for sid in body:cmd+=['--loop-body-step',sid]
 journal('before-post-assessment-validation',iteration=i);r=call('controller',cmd,payload);(d/'validated-route.json').write_text(json.dumps(r,indent=2)+'\n');journal('post-assessment-route-validated',iteration=i,action=r['action']);s['passes'].append({'iteration':i,'assessment':a,'route':r});save();call('recovery',['loop-pass','--summary',s['summary']],{'loop_id':'implementation-continuation-loop','iteration':i,'steps':[{'step_id':sid,'status':'completed'} for sid in body],'outcome':a,'evidence':[{'path':q.as_posix(),'sha256':sha(q)} for q in d.iterdir() if q.is_file()]});journal('validated-loop-pass-persisted',iteration=i);print(json.dumps(r));sys.exit()
raise ValueError('unknown action')
