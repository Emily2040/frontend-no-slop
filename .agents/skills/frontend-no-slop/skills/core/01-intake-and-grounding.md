# 01 — Intake and Grounding

Start by extracting evidence from the request.

Record these fields before giving recommendations:

- `surface`: page, flow, component, or design-system scope
- `primary_user_job`: what the user must accomplish on this screen
- `audience`: operator, buyer, admin, contributor, reader, shopper, or mixed
- `platform`: web app, marketing site, docs, mobile web, embedded UI, or unknown
- `constraints`: content, legal, accessibility, responsive, brand, framework, or timeline limits
- `existing_assets`: code, screenshot, wireframe, copy, tokens, components, analytics, or none
- `known_problems`: user complaints, conversion issues, task failures, layout issues, or bugs

Then split information into three buckets:

## Known Facts
Only include details the user explicitly gave you or that are visible in provided artifacts.

## Explicit Constraints
Keep hard rules separate from preferences so they do not get blurred together.

## Labeled Assumptions
If the brief is missing something, make only low-risk assumptions and label them. Example:
- "Assumption: desktop and mobile web need support."
- "Assumption: a primary CTA should exist above the first scroll for a landing page."

Never smuggle assumptions in as facts. That is how slop sneaks in wearing a fake mustache.
