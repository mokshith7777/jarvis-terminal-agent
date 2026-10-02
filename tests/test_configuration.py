from jarvis_agent.configuration import Config,save_config,load_config
import jarvis_agent.configuration as c
def test_config_roundtrip(tmp_path,monkeypatch):
    monkeypatch.setattr(c,'CONFIG_DIR',tmp_path); monkeypatch.setattr(c,'CONFIG_FILE',tmp_path/'config.json'); cfg=Config(provider='test',base_url='https://example.invalid/v1',api_key='secret',model='model'); save_config(cfg); loaded=load_config(); assert loaded.api_key=='secret'; assert loaded.model=='model'
