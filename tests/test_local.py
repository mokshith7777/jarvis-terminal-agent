from jarvis_agent.tools.local import LocalTools
def test_status(tmp_path):
    result=LocalTools(True,str(tmp_path)).status(); assert result['dry_run'] is True; assert result['workspace']==str(tmp_path.resolve())
