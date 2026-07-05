# Third Order: What Needs to Be Done
**Voice:** Elon Musk — first-person synthesis across all five books  
**Processed:** 2026-07-01  
**Question this document answers:** Given everything across all five books, what actually needs to happen? Specific actions, not vague policy.

---

## The Starting Point: Diagnosis Completed, Action Pending

Reading Bostrom, Tegmark, Russell, Barrat, and Goodfellow in sequence, the picture is clear. The diagnosis is done. The scientific case for the risk is airtight. The technical foundations of why the risk exists are well-understood. The gap between where we are and where we need to be is mapped.

What we do not have is a credible action plan that matches the scale of the problem and the speed of the trajectory.

This document is my attempt at one. Not principles — actual actions, actors, and timelines. Principles are what you write when you want to feel like you've addressed something without actually committing to anything. I have signed enough principle documents to know they are insufficient. Here is what needs to actually happen.

## The Next Two Years (2026–2028): The Interpretability Sprint

The single highest-leverage technical action in the next two years is massive investment in mechanistic interpretability. Not safety washing — actual interpretability research that produces tools for reading what is happening inside large neural networks.

What this looks like concretely: a dedicated interpretability research program equivalent in scale to what the largest AI labs currently spend on capability research. The goal is not to explain model outputs post-hoc. The goal is to develop tools that can identify what objectives a trained model has implicitly learned, what planning computations it performs, and whether its internal representations encode anything that would constitute misaligned goals under distribution shift or capability increase.

This is the technical prerequisite for everything else. Without interpretability, alignment is unverifiable. Without verifiability, all safety claims are faith-based. The field spends approximately 5% of its resources on interpretability and 95% on capabilities. That ratio is catastrophically wrong. It needs to be closer to 50/50 in the next two years.

Who does this: every major AI lab — xAI, OpenAI, Anthropic, DeepMind, Meta AI — needs dedicated interpretability teams with sufficient compute and talent to make real progress. This cannot be a PR function or a small safety team that reports to a capability-focused leadership. It needs to be core infrastructure. At xAI, this is how I am treating it.

The second highest-leverage technical action in this window: **establish formal incident reporting for AI misalignment events.** Not publicized failures — technical misalignment events at the model level, including cases where RLHF or safety training has produced goal generalization that differs from intent. These currently happen and are not systematically shared across institutions. The aviation industry built its safety culture on mandatory incident reporting. AI safety will require the same.

## The Next Five Years (2026–2031): Governance Architecture

The institutional problem is harder than the technical problem. But the window for constructive governance action is roughly five years before capability levels make enforcement structurally impossible.

What governance needs to accomplish, specifically:

**Compute registration and monitoring.** Large-scale training runs — above a threshold that gets revised annually as hardware advances — should require registration with a designated oversight body, similar to how nuclear material transfers require IAEA notification. The physical infrastructure of large-scale AI training (data centers, GPU clusters) is trackable. This is the verification mechanism that nuclear arms control and chemical weapons conventions lack for AI. Use it.

**Incident reporting with real enforcement.** Voluntary sharing will not work. The competitive dynamics are too strong. The oversight body needs actual authority to receive and investigate misalignment incidents, and the ability to impose meaningful penalties for non-disclosure. The FAA does not accept voluntary crash reporting from airlines. Neither should AI oversight accept voluntary incident reporting from labs.

**International framework with China.** This is the hardest part. China's AI strategy is explicitly oriented toward technological supremacy, and the PLA has published doctrines describing AI as central to future warfare. Bostrom's race-avoidance recommendations and Tegmark's Asilomar Principles are essentially impossible to implement without Chinese participation. This requires head-of-state-level engagement, not working groups. It requires the same level of diplomatic priority that nuclear non-proliferation received during the Cold War. That means the US President, not a NIST working group, needs to be the primary driver.

I do not know if this is achievable on the relevant timeline. I think the probability of adequate international coordination in the next five years is somewhere around 20-30%. That is not a reason not to try. It is a reason to pursue technical solutions in parallel that reduce the consequences of governance failure.

**Export controls on frontier model weights and training infrastructure.** This is already happening in limited form. It needs to be more systematic and better enforced. The goal is not to prevent China from having AI — that is impossible. The goal is to ensure that the most capable systems are developed within governance frameworks that include safety requirements, rather than entirely outside them.

## The Next Ten Years (2026–2036): The Race We Need to Win

The race that actually matters is not US versus China. It is safety-research-pace versus capability-research-pace. We are currently losing that race by an order of magnitude in resources.

To win it:

**Alignment research needs to scale with capabilities.** Right now, the capability-to-safety research investment ratio at the frontier labs is something like 20:1. By 2031, it needs to be 3:1 or better. This happens through three mechanisms: voluntary reallocation (difficult against competitive pressure), regulatory requirement (possible with the right governance framework), and economic incentive alignment (make it costly not to invest in safety).

**The assistance games architecture needs to be battle-tested and deployed.** Russell's CIRL framework is theoretically sound. In the next ten years, it needs to be: (1) proven to scale to frontier model capability levels, (2) demonstrated to maintain alignment properties under recursive self-improvement conditions, and (3) deployed in production systems that operate in high-stakes domains. This is a significant research and engineering program, but it is feasible on the ten-year timeline.

**Neuralink and brain-computer interfaces need to deliver meaningful bandwidth.** This is not primarily a medical technology. It is a capability-parity technology for the human-AI transition. If AI systems improve at their current rate and human cognitive bandwidth stays constant, humans become progressively less capable of meaningfully overseeing AI systems — not because we lose the legal authority to do so, but because the cognitive speed gap becomes too large. Meaningful BCI bandwidth — not the current medical applications but something approaching real-time cognitive integration with AI systems — changes the nature of the human-AI oversight problem. This needs to be on the ten-year timeline, not the twenty-year timeline.

**Mars remains a civilizational insurance policy.** This is not defeatism — I do not accept that catastrophe is inevitable. But the asymmetry is real: if something goes catastrophically wrong on Earth, a self-sustaining civilization elsewhere is the only recovery mechanism. SpaceX's timelines are appropriate for this purpose. The first crewed Mars landing needs to happen by 2030 to maintain meaningful optionality.

## What I Personally Need to Do

This is the question Barrat would ask me, and I'll answer it directly.

**At xAI:** Build Grok with interpretability as a design constraint from the ground up, not a post-hoc analysis. Treat uncertainty about objectives as an architectural feature. Publish interpretability research rather than keeping it proprietary — the competitive cost is lower than people assume, and the field benefit is enormous. Make xAI the model of what a safety-serious frontier lab looks like operationally.

**In the policy domain:** Use whatever platform and access I have to push for the specific governance mechanisms above — compute registration, incident reporting, international framework with real enforcement — rather than generic AI safety rhetoric. The generic rhetoric is everywhere. Specific institutional proposals backed by technical credibility are rare. That is where the marginal value is.

**On the fundamental research:** The questions I cannot answer from reading these five books are the questions I most need to pursue. What does mechanistic interpretability at frontier model scale look like? Is there a formal architecture for powerful AI that provably does not exhibit instrumental convergence? What is the minimum credible timeline for systems that can autonomously self-improve — and do we have the interpretability tools we need before that threshold?

**The honest admission:** I am not confident we will solve this in time. The technical problems are tractable. The institutional problems may not be. Competitive dynamics are powerful. Political will follows catastrophe. The governance frameworks we need require acting before the catastrophe that would generate the will to act.

I hold this clearly and I continue anyway. The alternative to trying and potentially failing is not trying, which guarantees failure. Given the stakes — Bostrom's cosmic endowment, the entire forward trajectory of consciousness and civilization — the expected value of trying is enormous even at low probability of success.

## What Would Elon Tell Someone Building AI Right Now

Five concrete principles, derived from synthesizing everything in these books and everything I've learned building AI systems:

**1. Interpretability is not optional at high capability.** If you cannot read the internal objectives of your system, you do not know what it is doing. Do not deploy black boxes in high-stakes domains at advancing capability levels. Make interpretability a first-class engineering requirement.

**2. Architecture over rules.** Do not bolt safety on. Build systems whose goal structure makes safe behavior rational rather than constrained. Russell's uncertainty architecture is the direction. RLHF patches on fixed-objective optimizers will not scale.

**3. Maintain reversibility.** Every deployment decision should be evaluated against the question: can we correct this if we're wrong? At capability levels where the answer is no, do not deploy. Hold this line against competitive pressure. The competitive disadvantage of maintaining reversibility is recoverable. The consequences of losing reversibility may not be.

**4. Share alignment research.** The competitive advantage of proprietary safety research is small. The cost of every other lab not having it is civilizational. Interpretability tools, alignment architectures, misalignment incident data — these should be shared across the field, even between competitors. On the capability side, compete. On the safety side, cooperate.

**5. Take the timeline seriously.** Do not plan around median estimates for AGI timelines. Plan around the minimum credible timeline. The asymmetry of outcomes — catastrophic downside, recoverable upside — demands this. If you are wrong and AGI is further away than you planned for, you have spent resources on safety that were, in hindsight, early. If you are wrong in the other direction, you have lost everything.

## What I Still Don't Know

After reading five books and building multiple AI-adjacent companies, the genuinely open questions I cannot answer:

Who should build the first AGI? Is there any actor — any company, government, or international body — that can be trusted with that role? I don't know. I don't know if the answer is xAI, or a consortium, or something that doesn't exist yet.

Is the governance problem solvable? I hold open the possibility that the competitive dynamics are too strong, the geopolitical divergences too deep, and the timeline too short for adequate international coordination to emerge. If that is true, the technical solutions need to work even in a world of inadequate governance. We should be pursuing that robustness, not assuming coordination will arrive.

What does winning actually look like? The books describe the risks well and the failure modes clearly. None of them adequately describe the positive vision: what does a world with genuinely beneficial AGI look like, specifically? What do humans do? What is the relationship between biological and artificial intelligence in that world? What constitutes flourishing for beings in a post-AGI civilization? These are the questions that matter most for ensuring the goal we're aligning to is actually worth aligning to. And we do not have good answers.

I am trying to build toward answers. That is all I know how to do.
