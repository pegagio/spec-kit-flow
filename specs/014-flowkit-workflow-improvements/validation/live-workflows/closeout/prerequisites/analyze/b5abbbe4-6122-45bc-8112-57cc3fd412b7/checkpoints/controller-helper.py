from pathlib import Path
import json,sys,subprocess,hashlib,datetime,shutil,re
p=Path.cwd();sf=Path('/tmp/t087an-state.json');g=json.loads(Path('/tmp/t087an-bootstrap.json').read_text());action=sys.argv[1]
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def run(args,data=None):return json.loads(subprocess.check_output(args,input=None if data is None else json.dumps(data).encode()))
def call(name,args,data):return run([sys.executable,'.specify/flow-kit/scripts/python/'+name+'.py',*args],data)
now=run(['bash','.specify/flow-kit/scripts/bootstrap.sh',str(p),'speckit-flow-analyze-remediate','flow-kit-analyze-remediate','--input','feature_context=Feature 802: specs/802-normalize-text']);assert now['sha256']==g['sha256'] and now['installation_fingerprints']==g['installation_fingerprints']
def flatten(nodes):
 out=[]
 for n in nodes:
  out.append(n)
  if n.get('type')=='switch':
   for branch in n['cases'].values():out.extend(flatten(branch))
 return out
nodes=flatten(g['steps'][0]['steps'])+g['steps'][1:]
def snapshot():return {q.relative_to(p).as_posix():sha(q) for q in p.rglob('*') if q.is_file() and not any(x in q.parts for x in ['.git','.flowkit-test','flow-controllers'])}
def journal(event,**kw):
 q=h/'journal.jsonl';count=len(q.read_text().splitlines()) if q.exists() else 0
 with q.open('a') as f:f.write(json.dumps({'sequence':count+1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':event,**kw})+'\n')
def save():sf.write_text(json.dumps(s))
def changed():a=snapshot();return [n for n in sorted(set(a)|set(s['before'])) if a.get(n)!=s['before'].get(n)]
if action=='init':
 source=json.loads((p.parents[1]/'.flowkit-test/coordinator-source-digests.json').read_text());assert sha(Path(g['source_path']))==source['sha256']['workflows/speckit-flow-analyze-remediate/workflow.yml'];assert sha(Path('.specify/flow-kit/controller-protocol.md'))==source['sha256']['controllers/flow-kit/controller-protocol.md'];profiles={q.relative_to(p).as_posix():sha(q) for q in (p/'.codex/agents').glob('*.toml')};assert len(profiles)==8 and all(source['sha256'][n]==v for n,v in profiles.items());r=call('recovery',['create','--project',str(p)],{'workflow':g,'fingerprints':g['installation_fingerprints'],'assignments':g['agent_assignments'],'preflight_passed':True});rid=r['summary']['run_id'];h=Path('.flowkit-test/closeout-prerequisite-analyze')/rid;h.mkdir(parents=True);s={'run_id':rid,'summary':r['summary_path'],'history':str(h),'before':snapshot(),'profiles':profiles,'graph':g,'outputs':{},'passes':[],'statuses':{},'answers':[]};save();(h/'before-hashes.json').write_text(json.dumps(s['before'],indent=2));(h/'installed-graph.json').write_text(json.dumps(g,indent=2));(h/'source-digests.json').write_text(json.dumps(source,indent=2));shutil.copy2(__file__,h/'controller-helper.py');journal('preflight-and-run-created',profiles_verified=8);print(rid);sys.exit()
s=json.loads(sf.read_text());h=Path(s['history']);i=int(sys.argv[2]);d=h/f'pass{i}';d.mkdir(exist_ok=True)
def render(t):
 t=t.replace('{{ inputs.feature_context }}',g['resolved_inputs']['feature_context']).replace('{{ inputs.integration }}','codex')
 for sid,out in s['outputs'].items():
  for k,v in out.items():t=t.replace('{{ steps.'+sid+'.output.'+k+' }}',v if isinstance(v,str) else json.dumps(v))
 assert '{{' not in t;return t
if action=='step':
 sid=sys.argv[3];status=sys.argv[4];n=next(n for n in nodes if n['id']==sid)
 if sid=='report-analysis-outcome':assert s['passes'] and s['passes'][-1]['route']['action']!='continue'
 if status=='running':
  (d/(sid+'-prompt.txt')).write_text(render(n.get('prompt',n.get('input',{}).get('args',''))))
 if status=='completed' and n.get('flow_kit',{}).get('delegated'):
  q=d/(sid+'-output.json');v=json.loads(q.read_text());assert isinstance(v,dict) and v.get('status') not in ['failed','incomplete','blocked'];s['outputs'][sid]=v;journal('actual-checkpoint-verified',iteration=i,step_id=sid,path=q.as_posix(),sha256=sha(q))
  if sid=='analyze-artifacts':assert 'report' in v and v['report'];
 journal('before-step-update',iteration=i,step_id=sid,status=status);call('recovery',['step','--summary',s['summary'],'--step-id',sid,'--status',status],{'changed_files':changed()});s['statuses'][f'{i}:{sid}']=status;save();journal('step-update-succeeded',iteration=i,step_id=sid,status=status);print(json.dumps({'step':sid,'status':status}));sys.exit()
if action=='prepare':
 actions={k:'skip' for k in ['spec_action','plan_action','task_action']};args=''
 if i>1:
  previous=s['passes'][-1];assert previous['route']['action']=='continue';sid=previous['assessment']['next_step_id'];index=['remediate-specification','remediate-plan','remediate-tasks'].index(sid)
  for k in list(actions)[index:]:actions[k]='run'
  args='Correct exact actual analyzer findings within approved feature; preserve accepted policies, task IDs/markers/completed T001 and unfinished implementation work. No implementation or other workflow. Exact full report: '+json.dumps(s['outputs']['analyze-artifacts']['report'],sort_keys=True)
 out={**actions,**{k:args for k in ['specification_args','plan_args','task_args']}};q=d/'prepare-analysis-flowback-output.json';q.write_text(json.dumps(out,indent=2)+'\n');s['outputs']['prepare-analysis-flowback']=out;save();journal('prepared-request-persisted',iteration=i,sha256=sha(q));print(json.dumps(out));sys.exit()
if action=='branch':
 sid=sys.argv[3];n=next(n for n in nodes if n['id']==sid);choice=render(n['expression']);r=call('controller',['branch'],{'switch':n,'choice':choice});(d/(sid+'-branch.json')).write_text(json.dumps(r,indent=2)+'\n');journal('branch-validated',iteration=i,step_id=sid,choice=choice);print(json.dumps(r));sys.exit()
if action=='route':
 assert s['statuses'].get(f'{i}:assess-analysis')=='completed';a=s['outputs']['assess-analysis'];payload={'assessment':a}
 if s['passes']:payload['previous_assessment']=s['passes'][-1]['assessment']
 cmd=['route-loop','--iteration',str(i),'--max-iterations','6','--assessment-only-first-pass','--project',str(p)]
 for n in flatten(g['steps'][0]['steps']):cmd+=['--loop-body-step',n['id']]
 journal('before-assessment-validation',iteration=i);r=call('controller',cmd,payload);(d/'route.json').write_text(json.dumps(r,indent=2)+'\n');journal('validated-route',iteration=i,action=r['action']);s['passes'].append({'iteration':i,'assessment':a,'route':r});save();steps=[{'step_id':n['id'],'status':s['statuses'].get(f'{i}:{n["id"]}','pending')} for n in flatten(g['steps'][0]['steps'])];call('recovery',['loop-pass','--summary',s['summary']],{'loop_id':'analysis-remediation-loop','iteration':i,'steps':steps,'outcome':a,'evidence':[{'path':q.as_posix(),'sha256':sha(q)} for q in d.iterdir() if q.is_file()]});journal('validated-loop-pass-persisted',iteration=i,action=r['action']);print(json.dumps(r));sys.exit()
raise ValueError('unknown action')
