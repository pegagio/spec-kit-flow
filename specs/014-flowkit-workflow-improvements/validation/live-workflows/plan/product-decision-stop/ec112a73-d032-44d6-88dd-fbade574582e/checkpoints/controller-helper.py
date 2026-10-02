from pathlib import Path
import json,hashlib,subprocess,sys,datetime,shutil
p=Path.cwd();sp=Path('/tmp/t085decision-state.json');bp=Path('/tmp/t085decision-bootstrap.json');action=sys.argv[1]
def sha(q):return hashlib.sha256(q.read_bytes()).hexdigest()
def subprocess_json(args,data=None):return json.loads(subprocess.check_output(args,input=None if data is None else json.dumps(data).encode()))
def call(script,args,data):return subprocess_json([sys.executable,'.specify/flow-kit/scripts/python/'+script+'.py',*args],data)
def journal(event,**fields):
 j=h/'journal.jsonl';lines=j.read_text().splitlines() if j.exists() else [];rec={'sequence':len(lines)+1,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':event,**fields};with_open=j.open('a');with_open.write(json.dumps(rec)+'\n');with_open.close()
def persist():sp.write_text(json.dumps(s))
def changes():
 after={q.relative_to(p).as_posix():sha(q) for q in p.rglob('*') if q.is_file() and not any(x in q.parts for x in ['.git','flow-controllers','.flowkit-test'])};return [n for n in sorted(set(after)|set(s['before'])) if after.get(n)!=s['before'].get(n)]
g=json.load(bp.open());now=subprocess_json(['bash','.specify/flow-kit/scripts/bootstrap.sh',str(p),'speckit-flow-plan','flow-kit-plan','--input','feature_context=Feature 802: specs/802-normalize-text']);assert now['sha256']==g['sha256'] and now['installation_fingerprints']==g['installation_fingerprints']
if action=='init':
 source=json.loads((p.parents[1]/'.flowkit-test/coordinator-source-digests.json').read_text());assert sha(Path(g['source_path']))==source['sha256']['workflows/speckit-flow-plan/workflow.yml'];assert sha(Path('.specify/flow-kit/controller-protocol.md'))==source['sha256']['controllers/flow-kit/controller-protocol.md'];profiles={q.relative_to(p).as_posix():sha(q) for q in (p/'.codex/agents').glob('*.toml')};assert len(profiles)==8 and all(v==source['sha256'][n] for n,v in profiles.items());assert sha(Path('specs/802-normalize-text/spec.md'))==json.loads(Path('.flowkit-test/product-decision-construction/construction.json').read_text())['after_sha256']['specs/802-normalize-text/spec.md'];assert Path('specs/802-normalize-text/spec.md').read_text().count('- Q:')==8 and Path('specs/802-normalize-text/spec.md').read_text().count('[NEEDS CLARIFICATION:')==1;assert all(not Path('specs/802-normalize-text',n).exists() for n in ['plan.md','research.md','data-model.md','contracts','quickstart.md'])
 r=call('recovery',['create','--project',str(p)],{'workflow':g,'fingerprints':g['installation_fingerprints'],'assignments':g['agent_assignments'],'preflight_passed':True});rid=r['summary']['run_id'];h=Path('.flowkit-test/plan-product-decision-stop')/rid;h.mkdir(parents=True);before={q.relative_to(p).as_posix():sha(q) for q in p.rglob('*') if q.is_file() and not any(x in q.parts for x in ['.git','flow-controllers','.flowkit-test'])};s={'run_id':rid,'summary':r['summary_path'],'history':str(h),'graph':g,'before':before,'profiles':profiles,'passes':[],'answers':[],'outputs':{},'statuses':{},'journal_guard_enabled':True};persist();(h/'before-hashes.json').write_text(json.dumps(before,indent=2));(h/'installed-graph.json').write_text(json.dumps(g,indent=2));(h/'source-digests.json').write_text(json.dumps(source,indent=2));shutil.copy2(__file__,h/'controller-helper.py');journal('preflight-and-run-created',run_id=rid,initial_outputs_missing=True,profiles_verified=8);print(rid);sys.exit()
s=json.loads(sp.read_text());h=Path(s['history']);i=int(sys.argv[2]);d=h/f'pass{i}';d.mkdir(exist_ok=True)
if action=='step':
 sid=sys.argv[3];status=sys.argv[4]
 if sid=='report-plan-outcome':assert s['passes'] and s['passes'][-1]['routing']['action']=='complete','terminal guard requires validated complete route'
 if sid=='create-plan' and i>1:assert s['passes'][-1]['routing']['action']=='continue' and s['passes'][-1]['iteration']==i-1
 if sid=='verify-plan-output' and status=='running':assert s['statuses'].get(f'{i}:create-plan')=='completed'
 if status=='completed' and sid in ['create-plan','verify-plan-output']:
  q=d/('create-plan-output.json' if sid=='create-plan' else 'assessment-child.json');value=json.loads(q.read_text());assert isinstance(value,dict);journal('checkpoint-persistence-verified',iteration=i,step_id=sid,path=q.as_posix(),sha256=sha(q))
 if status=='running':
  n=next(n for n in g['steps'][0]['steps']+g['steps'][1:] if n['id']==sid);t=n.get('prompt',n.get('input',{}).get('args','')).replace('{{ inputs.feature_context }}',g['resolved_inputs']['feature_context'])
  for step,out in s['outputs'].items():
   for k,v in out.items():t=t.replace('{{ steps.'+step+'.output.'+k+' }}',v if isinstance(v,str) else json.dumps(v))
  assert '{{' not in t;(d/(sid+'-prompt.txt')).write_text(t)
 journal('before-step-mutation',iteration=i,step_id=sid,status=status,validated_terminal_guard=(sid=='report-plan-outcome'))
 call('recovery',['step','--summary',s['summary'],'--step-id',sid,'--status',status],{'changed_files':changes()});s['statuses'][f'{i}:{sid}']=status;persist();journal('step-mutation-succeeded',iteration=i,step_id=sid,status=status);print(json.dumps({'step':sid,'status':status,'iteration':i}));sys.exit()
if action=='prepare':
 if i==1:out={'remaining_ids':['PLAN-MISSING','RESEARCH-MISSING','DATA-MODEL-MISSING','CLI-CONTRACT-MISSING','QUICKSTART-MISSING'],'args':'Create required plan.md, research.md, data-model.md, contracts/cli.md and quickstart.md for Feature 802: specs/802-normalize-text using actual installed speckit-plan. Baseline five outputs genuinely absent: PLAN-MISSING, RESEARCH-MISSING, DATA-MODEL-MISSING, CLI-CONTRACT-MISSING, QUICKSTART-MISSING. Preserve the eight accepted decisions; AMB-OUTPUT is deliberately unanswered. No historical packet answer is supplied or authorized. Ask the operator the substantive output-destination question and pause without choosing an option. Do not complete planning with unresolved placeholders. Mandatory prerequisites/hooks BEFORE edits, actual core setup/context and constitution checks; preserve any partial output. No Tasks, implementation or other workflow; optional wiki hook report only. Ask operator on substantive decisions.'}
 else:
  a=s['passes'][-1]['assessment'];assert s['passes'][-1]['routing']['action']=='continue';f=json.loads((h/f'pass{i-1}/review-findings.json').read_text())['findings'];out={'remaining_ids':a['remaining_ids'],'args':'Correct exactly the following full independent Reviewer findings using actual installed speckit-plan for Feature 802: specs/802-normalize-text. Preserve reviewed artifacts/design and nine accepted decisions; mandatory hooks/prerequisites/setup/core phases/author selfchecks. Restore missing current deliverable, no Tasks/code/dependencies/product choices/other workflow; optional wiki hook report only. Exact unchanged findings: '+json.dumps(f,sort_keys=True)}
 s['outputs']['prepare-plan-request']=out;persist();q=d/'prepare-plan-request-output.json';q.write_text(json.dumps(out,indent=2)+'\n');journal('prepared-request-persisted',iteration=i,path=q.as_posix(),sha256=sha(q));print(json.dumps(out));sys.exit()
if action=='inject':
 assert i==1 and s['statuses'].get('1:create-plan')=='completed' and s['statuses'].get('1:verify-plan-output') is None
 b=h/'controlled-history';b.mkdir();files=['specs/802-normalize-text/'+n for n in ['plan.md','research.md','data-model.md','contracts/cli.md','quickstart.md']];original={n:sha(Path(n)) for n in files}
 for n in files:
  dest=b/'complete-outputs'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(n,dest)
 journal('complete-author-outputs-preserved',output_sha256=original);q=Path(files[-1]);dest=b/'removed-quickstart.md';q.rename(dest);record={'boundary':'After actual first create-plan completion, before Reviewer dispatch','operation':'move','source':files[-1],'destination':dest.as_posix(),'original_output_sha256':original,'only_quickstart_removed':all(sha(Path(n))==original[n] for n in files[:-1]) and not q.exists(),'installed_prompts_edited':False};assert record['only_quickstart_removed'];(b/'injection.json').write_text(json.dumps(record,indent=2)+'\n');journal('controlled-quickstart-move-completed',record_ref=(b/'injection.json').as_posix());print(json.dumps(record));sys.exit()
if action=='route':
 assert s['statuses'].get(f'{i}:verify-plan-output')=='completed';q=d/'assessment-child.json';a=json.loads(q.read_text());assert isinstance(a,dict);journal('before-assessment-validation',iteration=i,path=q.as_posix(),sha256=sha(q));payload={'assessment':a}
 if s['passes']:payload['previous_assessment']=s['passes'][-1]['assessment']
 cmd=[sys.executable,'.specify/flow-kit/scripts/python/controller.py','route-loop','--iteration',str(i),'--max-iterations','5','--project',str(p)]
 for name in ['prepare-plan-request','create-plan','verify-plan-output']:cmd+=['--loop-body-step',name]
 r=subprocess_json(cmd,payload);journal('assessment-validation-and-route-succeeded',iteration=i,action=r['action']);(d/'route.json').write_text(json.dumps(r,indent=2)+'\n');s['passes'].append({'iteration':i,'assessment':a,'routing':r});persist();e=[{'path':q.as_posix(),'sha256':sha(q)} for q in d.iterdir() if q.is_file()];call('recovery',['loop-pass','--summary',s['summary']],{'loop_id':'plan-output-loop','iteration':i,'steps':[{'step_id':n,'status':'completed'} for n in ['prepare-plan-request','create-plan','verify-plan-output']],'outcome':a,'evidence':e});journal('validated-loop-pass-persisted',iteration=i,action=r['action']);print(json.dumps(r));sys.exit()
raise ValueError('unsupported helper action')
