import importlib.util
from pathlib import Path

# load modules directly to avoid package import side-effects
spec_rb = importlib.util.spec_from_file_location("rbmod", Path("rule_based.py").resolve())
rbmod = importlib.util.module_from_spec(spec_rb)
spec_rb.loader.exec_module(rbmod)
RuleBasedSentiment = rbmod.RuleBasedSentiment

spec_fu = importlib.util.spec_from_file_location("fumod", Path("fusion.py").resolve())
fumod = importlib.util.module_from_spec(spec_fu)
spec_fu.loader.exec_module(fumod)
ConditionalFusion = fumod.ConditionalFusion

rb = RuleBasedSentiment()
fu = ConditionalFusion()

cases = [
    "Sản phẩm này có chất lượng tốt",
    "Giao hàng nhanh chóng",
    "Tôi sẽ mua lại sản phẩm này",
    "Dịch vụ được đấy",
    "Rất hài lòng và bất mãn",
]

for text in cases:
    s_rule = rb.analyze_sentiment(text)
    mixed = rb.detect_mixed_sentiment(text)
    neutral = rb.is_neutral_context(text)
    # Simulate phobert result favoring POSITIVE with high conf to check fusion behavior
    l_phobert, c_phobert = "POSITIVE", 0.9
    fused = fu.fuse(l_phobert, c_phobert, s_rule, mixed_flag=mixed, neutral_flag=neutral)
    print(f"TEXT: {text}")
    print(f"  rule_score={s_rule}, mixed={mixed}, neutral={neutral}")
    print(f"  phobert={(l_phobert, c_phobert)} -> fused={fused}\n")
