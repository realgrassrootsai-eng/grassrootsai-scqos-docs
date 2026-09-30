# Architecture Overview

SCQOS evaluates whether a proposed consequential action is admissible before the mechanism capable of producing that consequence is invoked.

A simplified public model is:

1. A proposal describes an intended state transition.
2. Relevant evidence and authority are resolved.
3. SCQOS evaluates the proposal against its invariants.
4. The decision is PERMIT or HOLD.
5. Only a permitted proposal may reach the consequential writer.
6. Evidence of the decision and observed consequence is captured in a receipt.

The central boundary is between reasoning about an action and causing the action. A model may generate text proposing a consequence without being permitted to execute that consequence.

SCQOS is designed so authority, scope, reference state, timing, causality, and observed effects can be examined as part of one governed event while still preserving clear interfaces between evidence producers and the SCQOS admissibility decision.
