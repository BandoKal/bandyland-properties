# Project visibility investigation

Historical investigation of project 5. The user subsequently created project 7, which returns all 43 issues and is now the active project. The observations below concern the retired project 5.

## Observed evidence

- Private project: https://github.com/users/BandoKal/projects/5
- Private repository: https://github.com/BandoKal/bandyland-properties
- Repository issue search returns all 43 issues.
- Direct issue-side project membership reads expose all 43 saved items with their dates, priorities and workstreams (verified during setup).
- Project-side `items` returns `totalCount: 0`, including queries covering both archive states and an explicit issue query.
- Chrome's By target date view visibly shows zero matching items.
- Re-adding existing issue 1 resolves to the same item ID, without duplication.
- Archiving and immediately restoring that membership preserved its ID and fields but did not repair visibility.
- Repositioning the first membership during setup also did not resolve the problem.
- A native-browser attempt to add the existing issue did not produce a verified change; computer control then failed. No successful browser-side repair is claimed.

## Minimal reproduction for GitHub Support

Project node ID: `PVT_kwHOACOc9c4BoS7q`

Example saved item ID: `PVTI_lAHOACOc9c4BoS7qzhC02RU`

```graphql
query {
  user(login: "BandoKal") {
    projectV2(number: 5) {
      items(first: 100) { totalCount nodes { id } }
    }
  }
  node(id: "PVTI_lAHOACOc9c4BoS7qzhC02RU") {
    ... on ProjectV2Item {
      id
      isArchived
      project { id number }
      content { ... on Issue { number } }
    }
  }
}
```

The project collection returns no items, while the direct node resolves to an unarchived item in project 5 for issue 1. Request investigation of the inconsistent project collection/index. This report has not been sent to GitHub Support.

## Related firsthand reports

- https://github.com/orgs/community/discussions/188487
- https://github.com/orgs/community/discussions/208682

These describe matching symptoms. One reported spontaneous recovery; others reported persistent failure. They do not establish a recovery deadline or prove the exact cause for this account.

## Working access

Use `TASKS.md` for dates and linked issues. `scripts/daily_todo.py` reads live issue-side memberships as well as the project collection. Do not delete or recreate the issue backlog to work around the empty board.
