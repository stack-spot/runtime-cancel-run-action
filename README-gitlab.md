# GitLab CI/CD Workflow for Runtime Cancel Run Action

This GitLab CI/CD workflow runs the Runtime Cancel Run Action with the specified parameters.

## Inputs

The following environment variables must be configured in your GitLab CI/CD settings:

- `CLIENT_ID`: Account client id (required)
- `CLIENT_KEY`: Account client secret key (required)
- `CLIENT_REALM`: Account client realm (required)
- `RUN_ID`: RUN_ID to cancel (required)
- `FORCE_CANCEL`: Forces the cancel (optional, default: `true`)

## Usage

To use this workflow, add the above environment variables to your GitLab CI/CD settings and include the `.gitlab-ci.yml` file in your repository.

```yaml
include:
  - local: '.gitlab-ci.yml'