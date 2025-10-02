from multi_agent_trust.trust_sim import TrustManager

def test_trust_update():
    tm = TrustManager()
    a = tm.register('t1')
    tm.observe('t1', 'request_info:general')
    assert tm.get_trust('t1') >= 0.0
