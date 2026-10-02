from pathlib import Path
import json,subprocess,sys,hashlib,datetime,shutil,re
p=Path.cwd();sf=Path('/tmp/t087closeretry-state.json');g=json.loads(Path('/tmp/t087closeretry-bootstrap.json').read_text());action=sys.argv[1]
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def run(args,data=None):return json.loads(subprocess.check_output(args,input=None if data is None else json.dumps(data).encode()))
def call(name,args,data):return run([sys.executable,'.specify/flow-kit/scripts/python/'+name+'.py',*args],data)
now=run(['bash','.specify/flow-kit/scripts/bootstrap.sh',str(p),'speckit-flow-closeout','flow-kit-closeout','--input','feature_context=specs/802-normalize-text']);assert now['sha256']==g['sha256'] and now['installation_fingerprints']==g['installation_fingerprints']
def walk(ns):
 for n in ns:
  yield n
  if n.get('type')=='do-while':yield from walk(n['steps'])
  if n.get('type')=='switch':
   for branch in n['cases'].values():yield from walk(branch)
nodes=list(walk(g['steps']));node=lambda sid:next(n for n in nodes if n['id']==sid)
def snapshot():return {q.relative_to(p).as_posix():sha(q) for q in p.rglob('*') if q.is_file() and not any(x in q.parts for x in ['.git','.flowkit-test','flow-controllers','__pycache__'])}
def journal(event,**kw):
 q=h/'journal.jsonl';count=len(q.read_text().splitlines()) if q.exists() else 0
 with q.open('a') as f:f.write(json.dumps({'sequence':count+1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':event,**kw})+'\n')
def save():sf.write_text(json.dumps(s))
def changes():a=snapshot();return [n for n in sorted(set(a)|set(s['before'])) if a.get(n)!=s['before'].get(n)]
def render(t):
 t=t.replace('{{ inputs.feature_context }}',g['resolved_inputs']['feature_context']).replace('{{ inputs.integration }}','codex')
 def sub(m):
  sid,field=m.group(1),m.group(2);v=s['outputs'][sid][field];return v if isinstance(v,str) else json.dumps(v,sort_keys=True)
 t=re.sub(r'{{ steps\.([a-z0-9-]+)\.output\.([a-z_]+) }}',sub,t);assert '{{' not in t;return t
if action=='init':
 assert not sf.exists();old=json.loads(Path('/tmp/t087impl-state.json').read_text());conv=json.loads(Path('/tmp/t087convdraft-state.json').read_text());src=json.loads((p.parents[1]/'.flowkit-test/coordinator-source-digests.json').read_text());r=call('recovery',['create','--project',str(p)],{'workflow':g,'fingerprints':g['installation_fingerprints'],'assignments':g['agent_assignments'],'preflight_passed':True});rid=r['summary']['run_id'];h=Path('.flowkit-test/closeout-success-retry-1')/rid;h.mkdir(parents=True);s={'run_id':rid,'summary':r['summary_path'],'history':str(h),'graph':g,'before':snapshot(),'profiles':old['profiles'],'baseline':old['baseline'],'implementation_history':old['history'],'convergence_history':conv['history'],'outputs':{},'passes':{'debrief':[],'wiki':[]},'statuses':{},'answers':[],'initial_assessment':None};save();(h/'before-hashes.json').write_text(json.dumps(s['before'],indent=2));(h/'installed-graph.json').write_text(json.dumps(g,indent=2));(h/'source-digests.json').write_text(json.dumps(src,indent=2));shutil.copy2(__file__,h/'controller-helper.py');shutil.copytree(Path(conv['history']),h/'converge-prerequisite');shutil.copytree('.flowkit-test/closeout-construction',h/'construction');shutil.copytree('.flowkit-test/closeout-preflight',h/'capacity-preflight');journal('preflight-and-run-created');print(rid);sys.exit()
s=json.loads(sf.read_text());h=Path(s['history']);group=sys.argv[2];i=int(sys.argv[3]);d=h/(group+str(i));d.mkdir(exist_ok=True)
if action=='step':
 sid=sys.argv[4];status=sys.argv[5];n=node(sid)
 if status=='running':(d/(sid+'-prompt.txt')).write_text(render(n.get('prompt',n.get('message',n.get('input',{}).get('args','')))))
 if status=='completed':
  q=d/(sid+'-output.json');v=json.loads(q.read_text());assert isinstance(v,dict);s['outputs'][sid]=v;journal('actual-checkpoint-persistence-verified',group=group,iteration=i,step_id=sid,sha256=sha(q))
  if sid=='assess-closeout-debrief':
   q2=d/'review-findings.json';f=json.loads(q2.read_text());assert isinstance(f if isinstance(f,list) else f.get('findings'),list);journal('separate-review-findings-persistence-verified',iteration=i,sha256=sha(q2))
 journal('before-step-update',group=group,iteration=i,step_id=sid,status=status);call('recovery',['step','--summary',s['summary'],'--step-id',sid,'--status',status],{'changed_files':changes()});s['statuses'][f'{group}:{i}:{sid}']=status;save();journal('step-update-succeeded',group=group,iteration=i,step_id=sid,status=status);print(json.dumps({'group':group,'iteration':i,'step':sid,'status':status}));sys.exit()
if action=='initial':
 a=s['outputs']['assess-closeout-readiness'];cmd=['assessment','--project',str(p)]
 for n in walk(node('closeout-debrief-loop')['steps']):cmd+=['--loop-body-step',n['id']]
 journal('before-initial-assessment-validation');r=call('controller',cmd,a);(d/'validated-initial.json').write_text(json.dumps(r,indent=2)+'\n');s['initial_assessment']=a;s['initial_route']=r;save();journal('initial-assessment-validated',action=r['route']['action']);print(json.dumps(r));sys.exit()
if action=='route':
 loop=node('closeout-debrief-loop' if group=='debrief' else 'wiki-reconciliation-loop');sid='assess-closeout-debrief' if group=='debrief' else 'assess-wiki-maintenance';a=s['outputs'][sid];payload={'assessment':a}
 if s['passes'][group]:payload['previous_assessment']=s['passes'][group][-1]['assessment']
 cmd=['route-loop','--project',str(p),'--iteration',str(i),'--max-iterations',str(loop['max_iterations'])]
 if group=='debrief':cmd+=['--assessment-before-correction']
 for n in walk(loop['steps']):cmd+=['--loop-body-step',n['id']]
 journal('before-assessment-validation',group=group,iteration=i);r=call('controller',cmd,payload);(d/'validated-route.json').write_text(json.dumps(r,indent=2)+'\n');journal('assessment-route-validated',group=group,iteration=i,action=r['action']);s['passes'][group].append({'iteration':i,'assessment':a,'route':r});save();executed=[{'step_id':n['id'],'status':'completed'} for n in loop['steps'] if s['statuses'].get(f'{group}:{i}:'+n['id'])=='completed'];call('recovery',['loop-pass','--summary',s['summary']],{'loop_id':loop['id'],'iteration':i,'steps':executed,'outcome':a,'evidence':[{'path':q.as_posix(),'sha256':sha(q)} for q in d.iterdir() if q.is_file()]});journal('validated-loop-pass-persisted',group=group,iteration=i);print(json.dumps(r));sys.exit()
if action=='branch':
 sid=sys.argv[4];choice=sys.argv[5];n=node(sid);r=call('controller',['branch'],{'switch':n,'choice':choice});(d/(sid+'-validated.json')).write_text(json.dumps(r,indent=2)+'\n');journal('branch-validated',group=group,iteration=i,step_id=sid,choice=choice);print(json.dumps(r));sys.exit()
raise ValueError('unknown action')
