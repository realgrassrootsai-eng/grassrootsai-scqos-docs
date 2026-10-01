# SCQOS Formal Model v0.2

Status: working public formalization aligned to the current canonical SCQOS transition contract.

This document describes SCQOS as a formal admissibility system for consequential state transitions. Natural language may be one source of a proposal, but the governance object is the transition and its bound evidence.

## 1. Governed transition

Let the proposed governed event be

\[
G = (P,E)
\]

where \(P\) is a transition proposal and \(E\) is the runtime evidence bound to that proposal.

A useful abstract state view is

\[
\hat S_{t+1}=F(S_t,\Delta)
\]

where \(S_t\) is authoritative current state, \(\Delta\) is the proposed transformation, and \(\hat S_{t+1}\) is the candidate next state.

SCQOS evaluates \(\Gamma(G)\in\{\mathrm{PERMIT},\mathrm{HOLD}\}\).
## 2. Canonical invariant vector

The canonical invariant vector is

\[
I(G)=(T,Ct,Al,Gn,B,R,Ca,Cn)
\]

with Time, Continuity, Alignment, Genesis, Boundary, Reference, Causality, and Consciousness.

Each component is Boolean at the decision boundary:

\[
I_i(G)\in\{0,1\}.
\]

Coherence is not a ninth invariant and is not the canonical eighth invariant. It is an internal cross-evidence consistency mechanism used by Consciousness.

## 3. Time

Time requires authoritative runtime temporal evidence to be admissible. A caller-supplied time, if present, is a claim checked against authoritative runtime time.

\[
T(G)=1
\iff
ValidRuntimeTime(t_r)
\land
(t_c=\varnothing\ \lor\ AdmissibleClaim(t_c,t_r))
\]

where \(t_r\) is runtime-observed time and \(t_c\) is an optional claimed observation time.
## 4. Continuity and Alignment

Let \(Req_{inh}(G)\) mean inherited state is required, and \(Refs(P)\) be the proposal's reference bindings.

\[
Ct(G)=1
\iff
ResolvedRequirement(G)
\land
(\neg Req_{inh}(G)\ \lor\ Refs(P)\neq\varnothing)
\]

Continuity does not itself prove that referenced content resolved correctly or semantically agrees with the proposal; those responsibilities remain with Reference and Alignment.

Alignment is conditional. When semantic verification is required, it must exist, pass, and bind the exact proposed consequence:

\[
Al(G)=1
\iff
\neg Req_{al}(G)
\lor
(Valid(V_{al})\land Pass(V_{al})\land H_\Delta(V_{al})=H_\Delta(P)).
\]

This separates semantic interpretation from the formal admissibility decision.

## 5. Genesis

Genesis binds the transition to attributable actor provenance:

\[
Gn(G)=1
\iff
IdentityBound(E_{id},P)
\land OriginAllowed(E_{id})
\land PrincipalMapsToActor(E_{id},P).
\]

The implementation checks consistency among transition identity, session identity, actor identity, origin class, and an accepted principal mapping or canonical guest identity.
## 6. Boundary and Reference

Boundary binds the exact proposed consequence to an allowed release operation and destination. If \(D\) is the governed-boundary descriptor:

\[
B(G)=1
\iff
Bound(E_b,P)
\land Operation(E_b)=Operation(D)
\land Destination(E_b)=Destination(D)
\land H_\Delta(E_b)=H_\Delta(P).
\]

Reference requires requested references, resolved references, and consumed content bindings to agree exactly.

Let \(Q\) be requested references, \(Z\) resolved references, \(D_c(r)\) the digest actually consumed, and \(D_r(r)\) the resolved-content digest:

\[
R(G)=1
\iff
Q=Z
\land Dom(D_c)=Q
\land Dom(D_r)=Z
\land
\forall r\in Q,\ D_c(r)=D_r(r).
\]

Thus an identifier resolving is not enough if the content now bound to it differs from the content actually consumed.
## 7. Causality

Causality binds successful production or execution evidence to the exact proposed consequence:

\[
Ca(G)=1
\iff
Success(E_x)
\land Transition(E_x)=Transition(P)
\land H_\Delta(E_x)=H_\Delta(P)
\land ObservationConsistent(E_x,P).
\]

For typed consequence production, request identity and consequence type are also bound. Execution success alone is insufficient.

## 8. Consciousness and coherence

Consciousness is invariant #8. Its first mechanism is cross-evidence coherence.

Let \(K(G)=1\) when the typed evidence records agree with one another and the proposal on exposed bindings such as transition identity, actor/session identity, reference requirements, release boundary, request identity, and consequence digest.

With no supplied material-change evidence:

\[
Cn(G)=K(G).
\]

When material change is supplied, automatic continuation is blocked unless requalification validates against current proof:

\[
Cn(G)=K(G)\land Requalified(G)\land NewProof(G).
\]

If authority lineage changed, the required baton-transfer proof is included in \(Requalified(G)\).
## 9. Decision rule

Define

\[
PassAll(G)=T\land Ct\land Al\land Gn\land B\land R\land Ca\land Cn.
\]

A failed invariant forces HOLD:

\[
\exists I_i(G)=0 \Rightarrow \Gamma(G)=\mathrm{HOLD}.
\]

A PERMIT requires all eight canonical invariants to pass:

\[
\Gamma(G)=\mathrm{PERMIT}\Rightarrow PassAll(G)=1.
\]

The receipt records the first failed invariant in canonical evaluation order.

The transition contract also permits a second HOLD class: all eight invariants may pass while an independent release-admission check blocks release. That block is recorded separately and does not create a ninth invariant.

A HOLD cannot create resulting consequential state:

\[
\Gamma(G)=\mathrm{HOLD}
\Rightarrow ResultingState(G)=\varnothing.
\]
## 10. Semantic and formal inputs

Natural language is one proposal-construction path:

\[
Language\rightarrow P.
\]

A natively formal system may construct the same kind of proposal directly:

\[
FormalInput\rightarrow P.
\]

In both cases:

\[
(P,E)\xrightarrow{SCQOS}\{\mathrm{HOLD},\mathrm{PERMIT}\}.
\]

The mathematical core therefore does not require natural language.

## 11. Candidate machine-checkable properties

Fail closed:

\[
\forall G,(\exists i:I_i(G)=0)\Rightarrow\Gamma(G)=\mathrm{HOLD}.
\]

Exact Reference binding:

\[
\exists r,D_c(r)\neq D_r(r)\Rightarrow R(G)=0.
\]

Exact consequence binding:

\[
H_\Delta(E_x)\neq H_\Delta(P)\Rightarrow Ca(G)=0.
\]

Boundary substitution resistance:

\[
Operation(E_b)\neq Operation(D)\lor Destination(E_b)\neq Destination(D)\Rightarrow B(G)=0.
\]

These are candidates for property-based testing, SMT solving, model checking, or theorem proving.

## 12. Scope of v0.2

This is a faithful abstraction of the current transition contract, not a claim that SCQOS has already been fully formally verified.

The next step is to encode a small subset of these properties in a machine-checkable model and compare that model against implementation tests and externally supplied mathematical systems.
