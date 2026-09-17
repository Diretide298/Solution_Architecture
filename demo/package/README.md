# Greenleaf Demo - the ADAM demo package

A made-up library lending service, used to show ADAM end to end: a ticket in
OpenProject, pulled into a code folder with the contract it touches, built by
Claude Code, and the ticket updated from Claude. It shares nothing with TICVAI.

- `contracts/lending.yaml` - books and loans: `borrowBook`, `returnBook`,
  `listMemberLoans`, one demo ticket each.

The tickets are built in the .NET 10 backend ADAM setup creates for this
project (`greenleaf-demo-backend`). The walkthrough is in `../DEMO.md`.
