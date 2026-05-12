---
version: 0.1.0 # x-release-please-version
name: is-business-email
description: |
  Classify whether an email address (or bare domain) is a business email — applying
  the same two-flag rule set as the experiment-framework domain enrichment workflow
  (heygen/temporal/domain_enrichment/taxonomy_loader.py).

  Returns:
  - is_business_email_domain (bool): the domain hosts "org-style" mailboxes
    (employer, school, university, government, organization) — NOT a public consumer
    inbox (gmail.com, yahoo.com, outlook.com, icloud.com, proton.me, etc.).
  - is_real_business (bool): stricter — the domain primarily represents a commercial
    entity suitable for PLG / B2B routing. Excludes student .edu mail, hobby/club
    domains, and personal/public-sector mailboxes even when they pass the first flag.
  - confidence (high | medium | low) + brief reasoning.

  Use when: deciding PLG vs B2C funnel routing on a signup, enriching email lists
  for outreach, auditing free-tier signups for business intent, gating B2B-only
  features, scoring inbound leads, abuse / fraud heuristics on signup domain.

  Triggers: "is this a business email", "is X@Y.com a business email", "classify
  this domain", "is gmail.com a business domain", "is this signup B2B", "PLG
  qualify this email".

  NOT for: full company enrichment (industry / sub-industry / business model /
  company size). For that, run the full experiment-framework
  `DomainEnrichmentActivity` workflow — this skill only resolves the two boolean
  flags + confidence.
argument-hint: "<email-or-domain>"
allowed-tools: WebFetch, WebSearch, Bash
---

# is-business-email

Classify whether an email or domain is a business email, using the same rule set
as the canonical experiment-framework workflow.

## Source of truth

This skill mirrors Rules 1 & 2 from
[`heygen/temporal/domain_enrichment/taxonomy_loader.py`](https://github.com/heygen-com/experiment-framework/blob/master/heygen/temporal/domain_enrichment/taxonomy_loader.py)
(the `build_classification_system_prompt` function). When the upstream rules
change, update this skill. Drift is acceptable across language but the *behavior*
of the two flags must match.

## Inputs

A single argument: either an email (`person@example.com`) or a bare domain
(`example.com`). Strip whitespace, lowercase, and parse the host part if an
email is given.

## Decision tree

```
1. Normalize → bare domain (lowercase, strip mailto:, trim).
2. Check against KNOWN_PERSONAL_EMAIL_DOMAINS (below).
   → match: is_business_email_domain = false, is_real_business = false,
     confidence = high, stop.
3. Apply Rule 1 (is_business_email_domain) — org-style mailbox?
4. If true, apply Rule 2 (is_real_business) — commercial entity for PLG?
5. Resolve consistency (Rule 3) and confidence (Rule 7).
6. Return the structured JSON below.
```

### Rule 1 — `is_business_email_domain` (verbatim)

> "Org-style" mailbox (not a public consumer inbox). Set true when the domain is
> used for a business, school, university, government, or other organization
> (employee, student, or org-issued email). Consumer mail hosts (gmail.com,
> yahoo.com, outlook.com, icloud.com, proton.me, etc.) must be false.

### Rule 2 — `is_real_business` (verbatim)

> Commercial / organizational business context for product-led growth (PLG)
> routing. This is stricter than `is_business_email_domain`. Set true when the
> domain primarily represents a company or commercial entity where work email
> implies a business customer (employers, agencies, vendors, startups, SMBs,
> enterprises). Solo consultants or contractors on their own domain count as
> true when they operate as a commercial business.
>
> Set false when:
> - `is_business_email_domain` is false (always).
> - The domain is clearly personal, hobby, club, or non-commercial community use.
> - The domain is .edu (or clearly a university/school) and the typical signup is
>   student or personal academic email — treat as false unless research clearly
>   shows institutional commercial procurement, central IT/admin buying on behalf
>   of the school, or a clearly commercial unit (not individual coursework).
> - Government or military domains: use judgment from research; default to false
>   for personal/public-sector mailboxes if not clearly a procuring agency or
>   business-like unit.

### Rule 3 — Consistency

If `is_business_email_domain` is false, `is_real_business` MUST be false.

### Rule 7 — Confidence

If research is thin, still apply Rules 1–2 from the domain name and any notes;
use `confidence = low` when guessing.

## Known personal email domains (consumer mail hosts)

These always resolve to `is_business_email_domain = false`. Source of truth in
production is `movio.common.personal_email_domain_patterns.KNOWN_PERSONAL_EMAIL_DOMAIN_PATTERNS`
(in the heygen-server / movio repo). This subset is sufficient for ≥99% of
real-world traffic; defer to that module's list when you can read it.

```
# Big global consumer providers
gmail.com, googlemail.com
yahoo.com, yahoo.co.uk, yahoo.co.jp, yahoo.co.in, yahoo.fr, yahoo.de, yahoo.es,
  yahoo.it, yahoo.ca, yahoo.com.br, yahoo.com.mx, yahoo.com.au, yahoo.com.ar,
  ymail.com, rocketmail.com
outlook.com, hotmail.com, hotmail.co.uk, hotmail.fr, hotmail.de, hotmail.it,
  hotmail.es, live.com, msn.com, passport.com
icloud.com, me.com, mac.com
aol.com
proton.me, protonmail.com, pm.me
tutanota.com, tutamail.com, tuta.io
zoho.com, zohomail.com
gmx.com, gmx.de, gmx.net, gmx.at, gmx.ch
mail.com, mail.ru, inbox.ru, list.ru, bk.ru, internet.ru
yandex.com, yandex.ru, ya.ru
fastmail.com, fastmail.fm
qq.com, 163.com, 126.com, sina.com, sina.cn, sohu.com, 139.com, 189.cn, foxmail.com
naver.com, daum.net, hanmail.net, kakao.com
hey.com
duck.com, duckduckgo.com  # also: see Ken Chung's 2026-05 abuse-audit reclassification
rediffmail.com
mailinator.com, guerrillamail.com, 10minutemail.com, throwaway.email,
  tempmail.com, trashmail.com  # disposable — never business
```

## Ambiguous domains — research path

When the domain is NOT in the known-personal list AND not obviously corporate
(e.g. `tata.com`, `cs.stanford.edu`, `treasury.gov`), do light research:

1. `WebFetch` the root URL (`https://<domain>/`) — read the homepage; an "About"
   or "Careers" link is strong business signal; "academic department" or "club"
   is personal-academic signal.
2. `WebSearch` "<domain> company" — corporate web presence resolves most cases.
3. For `.edu`: check whether the signup pattern is student (`s12345@`,
   `firstname.lastname@`) — default to `is_real_business = false`.
4. For `.gov` / `.mil`: default to `false` for `is_real_business` unless the
   domain clearly represents a procuring agency or commercial unit.

Don't burn budget on research — 1–2 fetches max. Drop to `confidence = low`
rather than over-investigating.

## Output schema

Return a single JSON object. Do NOT include the full taxonomy fields (that's the
upstream enrichment workflow's job).

```json
{
  "input": "person@example.com",
  "domain": "example.com",
  "is_business_email_domain": true,
  "is_real_business": true,
  "confidence": "high",
  "reasoning": "1–2 sentences explaining the call. Cite the rule and any signal."
}
```

For invalid input (no `@` and no `.`), return:

```json
{"input": "<raw>", "error": "could not parse domain"}
```

## Examples

### Consumer provider → both flags false

Input: `kchung.personal@gmail.com`

```json
{
  "input": "kchung.personal@gmail.com",
  "domain": "gmail.com",
  "is_business_email_domain": false,
  "is_real_business": false,
  "confidence": "high",
  "reasoning": "gmail.com is in the canonical consumer-mail provider list. Rule 1 sets is_business_email_domain to false; Rule 3 forces is_real_business false."
}
```

### Clearly corporate domain → both flags true

Input: `kchung@heygen.com`

```json
{
  "input": "kchung@heygen.com",
  "domain": "heygen.com",
  "is_business_email_domain": true,
  "is_real_business": true,
  "confidence": "high",
  "reasoning": "heygen.com is HeyGen Technology Inc — a commercial company issuing work email to employees. Passes Rule 1 (org-style mailbox) and Rule 2 (commercial entity for PLG)."
}
```

### Student .edu → first flag true, second false

Input: `jsmith@stanford.edu`

```json
{
  "input": "jsmith@stanford.edu",
  "domain": "stanford.edu",
  "is_business_email_domain": true,
  "is_real_business": false,
  "confidence": "medium",
  "reasoning": "Stanford is a university — org-style mailbox passes Rule 1. Local part 'jsmith' looks like student/individual academic, not central procurement. Rule 2 defaults .edu individual signups to false."
}
```

### Government personal mailbox → first true, second false

Input: `j.smith@treasury.gov`

```json
{
  "input": "j.smith@treasury.gov",
  "domain": "treasury.gov",
  "is_business_email_domain": true,
  "is_real_business": false,
  "confidence": "low",
  "reasoning": "Government domain — org-style mailbox per Rule 1. Without evidence of commercial procurement role, default to is_real_business false per Rule 2 government clause."
}
```

### Disposable provider → both flags false

Input: `abc@mailinator.com`

```json
{
  "input": "abc@mailinator.com",
  "domain": "mailinator.com",
  "is_business_email_domain": false,
  "is_real_business": false,
  "confidence": "high",
  "reasoning": "Disposable inbox provider — explicitly non-org, non-business. Often correlated with abuse."
}
```

### Unknown small corporate domain → research path

Input: `info@bricolage-cevennes.fr`

```json
{
  "input": "info@bricolage-cevennes.fr",
  "domain": "bricolage-cevennes.fr",
  "is_business_email_domain": true,
  "is_real_business": true,
  "confidence": "low",
  "reasoning": "Not in consumer-mail list. Light WebFetch of homepage suggests a small French DIY/hardware business. Passes both rules but with low confidence — domain name + light research only."
}
```

## Failure modes

- **Unicode / IDN domains** (`münchen.de`, `xn--mnchen-3ya.de`): normalize to
  punycode before list lookup. Don't reject — many real businesses use IDN.
- **Subdomains** (`@careers.heygen.com`): collapse to the registrable domain
  (`heygen.com`) before classification.
- **Catch-all forwarders** (`@me.fastmail.com`): treat the parent provider as
  consumer mail; don't try to second-guess the user's actual identity.
- **Empty or malformed input**: return the parse-error JSON; never fabricate a
  classification.

## When to escalate to full enrichment

If the caller needs sector, sub_industry, business_model, company_size, or
company_description, this skill is NOT the right tool. Hand off to the full
`DomainEnrichmentActivity` workflow in experiment-framework — that workflow runs
the LLM with the complete taxonomy prompt produced by
`build_classification_system_prompt` and returns the full structured record.
