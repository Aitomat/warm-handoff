# Evidence Scope

<!-- rule:EV-01 -->
## Evidence classes

- **Source fact:** exact user text, repository content, or official documentation.
- **Observed state:** current command, tool, UI, or test result with date and environment.
- **Inference:** a conclusion derived from source facts or observations.
- **Unknown:** a value the available evidence does not establish.

Label inference explicitly. Prefer primary documentation for changing platform claims.

<!-- rule:EV-02 -->
## Time and product boundaries

Add a verification date to model, caching, pricing, quota, and product-capability claims. Name the product surface: API, desktop client, CLI, subscription plan, or current host session. A fact from one surface does not automatically apply to another.

<!-- rule:EV-03 -->
## Completion evidence

Match the claim to the check. A renderer test proves generated RTF structure; an AppKit continuation test proves save/reload style behavior; a manual target-app test proves paste behavior. File existence does not prove content, and a worker report does not replace integration verification.

When evidence is incomplete, state the exact open check instead of weakening the wording with vague confidence.
