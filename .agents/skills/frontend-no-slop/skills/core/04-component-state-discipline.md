# 04 — Component State Discipline

Do not describe components as if they only exist in the happy path.

For each interactive component, list relevant states:

- default
- hover
- focus
- active or selected
- disabled
- loading
- empty
- error
- success
- overflow or long-content
- mobile or narrow-width adaptation

Component-specific reminders:

## Buttons and Links
Label the action precisely. Distinguish destructive, secondary, ghost, and text actions.

## Forms
Cover labels, helper text, validation timing, inline errors, success confirmation, disabled submit, and keyboard flow.

## Tables and Data Views
Cover sorting, filtering, density, truncation, sticky headers, row actions, empty results, loading, pagination, and mobile fallback.

## Menus, Popovers, and Dialogs
Cover trigger behavior, focus trap, escape key, outside click, accessible name, and stacked interaction edge cases.

## Navigation
Show current location, hover and focus treatment, collapsed mobile behavior, and keyboard reachability.

If a recommendation skips states, it is still half-baked dough.
