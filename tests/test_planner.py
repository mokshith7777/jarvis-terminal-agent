from jarvis_agent.agent.planner import Planner
def planner(): return Planner.__new__(Planner)
def test_fallback_status(): assert planner().fallback('status')['action']=='status'
def test_fallback_disk(): assert planner().fallback('disk space')['args']['argv']==['df','-h']
