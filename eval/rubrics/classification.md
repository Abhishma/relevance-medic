# Classification rubric

Score a diagnosis higher when:
1. the failure class matches the dominant incident pattern
2. evidence cited is explicitly present in the input
3. recommendations are low-risk and testable
4. regression checks are relevant to the failure mode
5. the system abstains when required evidence is missing

Downgrade when:
- the output invents evidence
- the failure class is overly specific without support
- recommendations are generic filler
- abstention should have happened but did not
