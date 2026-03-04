## Local Development with Docker

```
docker compose -f docker-compose.dev.yml up --build
```

## GitHub Actions Deploy to AWS Elastic Beanstalk (OIDC)

If your workflow fails with:

`Could not assume role with OIDC: Not authorized to perform sts:AssumeRoleWithWebIdentity`

the issue is AWS IAM trust configuration (not workflow syntax).

This repo's workflow maps branches to GitHub Environments:

- `dev` branch -> `dev` environment
- `staging` branch -> `staging` environment
- `main` branch -> `prod` environment

Because of that, your IAM role trust policy must allow `sub` claims in this format:

- `repo:<ORG>/<REPO>:environment:dev`
- `repo:<ORG>/<REPO>:environment:staging`
- `repo:<ORG>/<REPO>:environment:prod`

Use this trust policy for the role in `AWS_GITHUB_ACTIONS_ROLE_ARN`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<AWS_ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": [
            "repo:<ORG>/<REPO>:environment:dev",
            "repo:<ORG>/<REPO>:environment:staging",
            "repo:<ORG>/<REPO>:environment:prod"
          ]
        }
      }
    }
  ]
}
```

Also verify:

- IAM OIDC provider exists: `token.actions.githubusercontent.com`
- `AWS_GITHUB_ACTIONS_ROLE_ARN` is a full IAM role ARN
- GitHub Environments (`dev`, `staging`, `prod`) include:
  - `AWS_REGION`
  - `EB_APPLICATION_NAME`
  - `EB_ENV_NAME`

After updating trust policy, re-run the failed workflow.
