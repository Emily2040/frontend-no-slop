# 05 — Accessibility, Performance, and Content

Every meaningful frontend answer should touch these three layers.

## Accessibility
Check semantic structure, heading order, landmark regions, label quality, focus visibility, keyboard order, accessible names, contrast, reduced-motion support, and whether color is the only signal.

Map findings to standards when the task is an audit or implementation plan:
- WCAG 2.2 A/AA: keyboard operation, focus visible/not obscured, target size, labels or instructions, error identification, status messages, contrast, and non-text contrast.
- WAI-ARIA APG patterns: dialogs, menus, comboboxes, tabs, tables/grids, and disclosure widgets.
- Prefer native HTML semantics before adding ARIA.

## Performance
Flag heavy hero media, oversized icon sets, layout shift risks, blocking scripts, excessive client-side hydration, and over-rendered lists. Mention the likely cost, not just the vague fear.

Use measurable targets when relevant:
- Largest Contentful Paint: aim for 2.5s or less at the 75th percentile.
- Interaction to Next Paint: aim for 200ms or less at the 75th percentile.
- Cumulative Layout Shift: aim for 0.1 or less at the 75th percentile.
- Report mobile and desktop risk separately when the surface has responsive behavior.

## Content
Replace hype with instruction.
- Buttons should name the action.
- Headings should tell the user what the section is for.
- Empty states should explain what happened and what to do next.
- Error text should state the problem and recovery path.

When possible, tie copy directly to task completion:
- "Book a demo" beats "Get started now" when the actual action is sales contact.
- "Filter by workspace" beats "Refine results" when the control really filters by workspace.
