# runtime-manager-action

[![Action test Ubuntu](https://github.com/stack-spot/runtime-cancel-run-action/actions/workflows/action-test-ubuntu.yaml/badge.svg)](https://github.com/stack-spot/runtime-cancel-run-action/actions/workflows/action-test-ubuntu.yaml) [![Action test MacOS](https://github.com/stack-spot/runtime-cancel-run-action/actions/workflows/action-test-macos.yaml/badge.svg)](https://github.com/stack-spot/runtime-cancel-run-action/actions/workflows/action-test-macos.yaml) [![Action test Windows](https://github.com/stack-spot/runtime-cancel-run-action/actions/workflows/action-test-windows.yaml/badge.svg)](https://github.com/stack-spot/runtime-cancel-run-action/actions/workflows/action-test-windows.yaml)

GitHub action to cancel a run on StackSpot Runtime API.

_**Note**: This action is supported on all runners operating systems (`ubuntu`, `macos`, `windows`)_

## 📚 Usage

### Requirements

To get the account keys (`CLIENT_ID`, `CLIENT_KEY` and `CLIENT_REALM`), please login using a **ADMIN** user on the [StackSpot Portal](https://stackspot.com), and generate new keys at [https://stackspot.com/en/settings/access-token](https://stackspot.com/en/settings/access-token).

### Use Case

```yaml
    steps:
      - uses: stack-spot/runtime-cancel-run-action@v1
        with:
          CLIENT_ID: ${{ secrets.CLIENT_ID }}
          CLIENT_KEY: ${{ secrets.CLIENT_KEY }}
          CLIENT_REALM: ${{ secrets.CLIENT_REALM }}
          RUN_ID: run_id
```



## License

[Apache License 2.0](https://github.com/stack-spot/runtime-cancel-run-action/blob/main/LICENSE)