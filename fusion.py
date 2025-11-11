class ConditionalFusion:
    def __init__(self, t_high=0.85, t_low=0.50, theta_rule=2.0, w_phobert=0.15, w_rule=0.85):
        # lower DL weight and increase rule weight to favor rule-based neutrality in conflicts
        self.t_high = t_high
        self.t_low = t_low
        self.theta_rule = theta_rule
        self.w_phobert = w_phobert
        self.w_rule = w_rule

    def fuse(self, l_phobert, c_phobert, s_rule, mixed_flag=False, neutral_flag=False):
        """Conditional Fusion Algorithm with improved neutral handling.

        Args:
            l_phobert: label from PhoBERT
            c_phobert: confidence from PhoBERT
            s_rule: score from rule-based analyzer
            mixed_flag: boolean, True if rule-based detected mixed/contrastive sentiment
        """
        # If rule-based explicitly flagged mixed sentiment, prefer NEUTRAL
        if mixed_flag:
            return "NEUTRAL", 0.90

        # If rule indicates neutral context (short descriptive/question/filler) and rule score is weak, force NEUTRAL
        if neutral_flag and abs(s_rule) < 1.0:
            return "NEUTRAL", 0.85
        # Special veto for very negative rule-based (toxic words)
        if s_rule <= -4.0:
            return "NEGATIVE", abs(s_rule) / 5.0

        # Case II: Rule-based Veto (prioritize over DL)
        if abs(s_rule) >= self.theta_rule:
            label = "POSITIVE" if s_rule > 0 else "NEGATIVE"
            return label, abs(s_rule) / 5.0  # Normalize confidence

        # Case 0: Neutral priority for low rule scores and medium PhoBERT confidence
        if abs(s_rule) < 1.0 and 0.60 <= c_phobert < self.t_high:
            return "NEUTRAL", 0.7

        # Case I: High DL Confidence
        if c_phobert >= self.t_high:
            return l_phobert, c_phobert  # Use PhoBERT

        # Case III: Conflict Resolution with Weighted Combination
        if self.t_low <= c_phobert < self.t_high:
            # Compute scores for each label
            scores = {}
            for label in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
                c_l = c_phobert if label == l_phobert else (1 - c_phobert) / 2  # Approximate
                s_rule_l = s_rule if (label == "POSITIVE" and s_rule > 0) or (label == "NEGATIVE" and s_rule < 0) else 0
                scores[label] = self.w_phobert * c_l + self.w_rule * abs(s_rule_l)
            final_label = max(scores, key=scores.get)
            final_conf = scores[final_label]
            return final_label, final_conf

        # Case IV: Low Confidence Ambiguity
        if c_phobert < self.t_low and abs(s_rule) < self.theta_rule:
            return "NEUTRAL", 0.5

        # Default fallback
        return l_phobert, c_phobert