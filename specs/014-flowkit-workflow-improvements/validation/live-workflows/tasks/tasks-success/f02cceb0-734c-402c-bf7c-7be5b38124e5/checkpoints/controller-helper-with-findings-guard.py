from pathlib import Path
import json,hashlib,subprocess,sys,datetime,shutil
p=Path.cwd();sp=Path('/tmp/t086-state.json');bp=Path('/tmp/t086-bootstrap.json');action=sys.argv[1]
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def subprocess_json(args,data=None):return json.loads(subprocess.check_output(args,input=None if data is None else json.dumps(data).encode()))
def call(script,args,data):return subprocess_json([sys.executable,'.specify/flow-kit/scripts/python/'+script+'.py',*args],data)
def journal(event,**fields):
 j=h/'journal.jsonl';lines=j.read_text().splitlines() if j.exists() else [];rec={'sequence':len(lines)+1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':event,**fields};with_open=j.open('a');with_open.write(json.dumps(rec)+'\n');with_open.close()
def persist():sp.write_text(json.dumps(s))
def changes():
 after={q.relative_to(p).as_posix():sha(q) for q in p.rglob('*') if q.is_file() and not any(x in q.parts for x in ['.git','flow-controllers','.flowkit-test'])};return [n for n in sorted(set(after)|set(s['before'])) if after.get(n)!=s['before'].get(n)]
g=json.load(bp.open());now=subprocess_json(['bash','.specify/flow-kit/scripts/bootstrap.sh',str(p),'speckit-flow-tasks','flow-kit-tasks','--input','feature_context=Feature 802: specs/802-normalize-text']);assert now['sha256']==g['sha256'] and now['installation_fingerprints']==g['installation_fingerprints']
if action=='init':
 source=json.loads((p.parents[1]/'.flowkit-test/coordinator-source-digests.json').read_text());assert sha(Path(g['source_path']))==source['sha256']['workflows/speckit-flow-tasks/workflow.yml'];assert sha(Path('.specify/flow-kit/controller-protocol.md'))==source['sha256']['controllers/flow-kit/controller-protocol.md'];profiles={q.relative_to(p).as_posix():sha(q) for q in (p/'.codex/agents').glob('*.toml')};assert len(profiles)==8 and all(v==source['sha256'][n] for n,v in profiles.items());assert sha(Path('specs/802-normalize-text/spec.md'))=='813f322e12043052ce04e5c5c23e14cc9e28ee7029d8cddf48e0f348db4f1bf0';assert all(Path('specs/802-normalize-text',n).exists() for n in ['plan.md','research.md','data-model.md','contracts','quickstart.md']);construction=json.loads(Path('.flowkit-test/tasks-construction/construction.json').read_text());assert sha(Path('specs/802-normalize-text/tasks.md'))==construction['seed_sha256'] and sha(Path(construction['reviewed_contract']))==construction['contract_sha256']
 r=call('recovery',['create','--project',str(p)],{'workflow':g,'fingerprints':g['installation_fingerprints'],'assignments':g['agent_assignments'],'preflight_passed':True});rid=r['summary']['run_id'];h=Path('.flowkit-test/tasks-success')/rid;h.mkdir(parents=True);before={q.relative_to(p).as_posix():sha(q) for q in p.rglob('*') if q.is_file() and not any(x in q.parts for x in ['.git','flow-controllers','.flowkit-test'])};s={'run_id':rid,'summary':r['summary_path'],'history':str(h),'graph':g,'before':before,'profiles':profiles,'passes':[],'answers':[],'outputs':{},'statuses':{},'journal_guard_enabled':True};persist();(h/'before-hashes.json').write_text(json.dumps(before,indent=2));(h/'installed-graph.json').write_text(json.dumps(g,indent=2));(h/'source-digests.json').write_text(json.dumps(source,indent=2));shutil.copy2(__file__,h/'controller-helper.py');journal('preflight-and-run-created',run_id=rid,initial_planning_outputs_present=True, seeded_completed_design_history=True,profiles_verified=8);print(rid);sys.exit()
s=json.loads(sp.read_text());h=Path(s['history']);i=int(sys.argv[2]);d=h/f'pass{i}';d.mkdir(exist_ok=True)
if action=='step':
 sid=sys.argv[3];status=sys.argv[4]
 if sid=='report-task-outcome':assert s['passes'] and s['passes'][-1]['routing']['action']=='complete','terminal guard requires validated complete route'
 if sid=='generate-tasks' and i>1:assert s['passes'][-1]['routing']['action']=='continue' and s['passes'][-1]['iteration']==i-1
 if sid=='verify-task-output' and status=='running':assert s['statuses'].get(f'{i}:generate-tasks')=='completed'
 if status=='completed' and sid in ['generate-tasks','verify-task-output']:
  q=d/('generate-tasks-output.json' if sid=='generate-tasks' else 'assessment-child.json');value=json.loads(q.read_text());assert isinstance(value,dict);journal('checkpoint-persistence-verified',iteration=i,step_id=sid,path=q.as_posix(),sha256=sha(q))
  if sid=='verify-task-output':
   q2=d/'review-findings.json';v2=json.loads(q2.read_text());assert isinstance(v2,dict) and isinstance(v2.get('findings'),list);journal('workflow-findings-persistence-verified',iteration=i,path=q2.as_posix(),sha256=sha(q2))
 if status=='running':
  n=next(n for n in g['steps'][0]['steps']+g['steps'][1:] if n['id']==sid);t=n.get('prompt',n.get('input',{}).get('args','')).replace('{{ inputs.feature_context }}',g['resolved_inputs']['feature_context'])
  for step,out in s['outputs'].items():
   for k,v in out.items():t=t.replace('{{ steps.'+step+'.output.'+k+' }}',v if isinstance(v,str) else json.dumps(v))
  assert '{{' not in t;(d/(sid+'-prompt.txt')).write_text(t)
 journal('before-step-mutation',iteration=i,step_id=sid,status=status,validated_terminal_guard=(sid=='report-task-outcome'))
 call('recovery',['step','--summary',s['summary'],'--step-id',sid,'--status',status],{'changed_files':changes()});s['statuses'][f'{i}:{sid}']=status;persist();journal('step-mutation-succeeded',iteration=i,step_id=sid,status=status);print(json.dumps({'step':sid,'status':status,'iteration':i}));sys.exit()
if action=='prepare':
 import re
 rows=[]
 for line in Path('specs/802-normalize-text/tasks.md').read_text().splitlines():
  m=re.match(r'^- \[([ xX])\] (T[0-9]{3,}) +(.+)$',line)
  if m:rows.append({'id':m.group(2),'completion_marker':'['+m.group(1)+']','description':re.sub(r'^(?:\[[^]]+\] +)+','',m.group(3)),'exact_row':line})
 assert rows
 if i==1:
  gaps=['TASK-PHASES-MISSING','TASK-IMPLEMENTATION-COVERAGE-MISSING','TASK-INDEPENDENT-CRITERIA-MISSING','TASK-DEPENDENCIES-MISSING','TASK-PARALLEL-EXAMPLES-MISSING','TASK-STRATEGY-MISSING']
  args='Generate substantive tasks.md for Feature 802: specs/802-normalize-text using actual installed speckit-tasks and current reviewed spec/plan/design. Current artifact has only completed DESIGN history; gaps are applicable setup/foundation/story/polish phases, implementation coverage, independent story criteria, dependencies, per-story parallel examples and strategy. Preserve every existing ID/marker and exact completed row; T001 documents reviewed CLI contract, never implementation. Allocate new implementation IDs after T001 and keep them unchecked. Preserve all9 accepted policies and reviewed design. Include required unit-test tasks from spec/constitution, data model constraints verbatim as applicable, concrete paths, story labels, priority/dependency order and executable increments. Mandatory core setup/hooks/context and author selfchecks; report actualcounts/gaps/blockers. No spec/design edits, Analyze, implementation or other workflow. Ask operator on substantive decisions.'
 else:
  a=s['passes'][-1]['assessment'];assert s['passes'][-1]['routing']['action']=='continue';f=json.loads((h/f'pass{i-1}/review-findings.json').read_text())['findings'];gaps=a['remaining_ids'];args='Correct the following exact independent Reviewer findings using actual speckit-tasks for Feature 802. Preserve all current task IDs/completion markers, completed DESIGN history, all9 approved decisions and reviewed design. Mandatory setup/hooks/selfchecks; new implementation work remains unchecked. No upstream spec/design edits, Analyze, implementation or other workflow. Exact unchanged findings: '+json.dumps(f,sort_keys=True)
 out={'task_history':rows,'remaining_ids':gaps,'args':args+' Exact pre-pass task history: '+json.dumps(rows,sort_keys=True)}
 s['outputs']['prepare-task-request']=out;persist();q=d/'prepare-task-request-output.json';q.write_text(json.dumps(out,indent=2)+'\n');journal('prepared-request-persisted',iteration=i,path=q.as_posix(),sha256=sha(q));print(json.dumps(out));sys.exit()
if action=='route':
 assert s['statuses'].get(f'{i}:verify-task-output')=='completed';q=d/'assessment-child.json';a=json.loads(q.read_text());assert isinstance(a,dict);journal('before-assessment-validation',iteration=i,path=q.as_posix(),sha256=sha(q));payload={'assessment':a}
 if s['passes']:payload['previous_assessment']=s['passes'][-1]['assessment']
 cmd=[sys.executable,'.specify/flow-kit/scripts/python/controller.py','route-loop','--iteration',str(i),'--max-iterations','5','--project',str(p)]
 for name in ['prepare-task-request','generate-tasks','verify-task-output']:cmd+=['--loop-body-step',name]
 r=subprocess_json(cmd,payload);journal('assessment-validation-and-route-succeeded',iteration=i,action=r['action']);(d/'route.json').write_text(json.dumps(r,indent=2)+'\n');s['passes'].append({'iteration':i,'assessment':a,'routing':r});persist();e=[{'path':q.as_posix(),'sha256':sha(q)} for q in d.iterdir() if q.is_file()];call('recovery',['loop-pass','--summary',s['summary']],{'loop_id':'tasks-output-loop','iteration':i,'steps':[{'step_id':n,'status':'completed'} for n in ['prepare-task-request','generate-tasks','verify-task-output']],'outcome':a,'evidence':e});journal('validated-loop-pass-persisted',iteration=i,action=r['action']);print(json.dumps(r));sys.exit()
raise ValueError('unsupported helper action')
