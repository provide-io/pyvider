# Git Provider - Version Control as Infrastructure

A **meta** Terraform provider that manages git operations as infrastructure. This demonstrates using Terraform (which itself is version-controlled) to manage version control systems declaratively.

## Why This Is Meta

- **Terraform configs** are stored in **git**
- This provider **manages git** operations
- Creates a feedback loop: version control managing version control

## Components

**3 Resources:**
- `git_repository` - Repository management
- `git_branch` - Branch creation and protection
- `git_pull_request` - PR/MR workflow automation

**2 Data Sources:**
- `repository_info` - Query repository details
- `pull_requests` - List and filter PRs

**4 Functions:**
- `generate_branch_name` - Standardized naming
- `parse_commit_message` - Conventional commits parser
- `validate_branch_name` - Branch name validation
- `calculate_diff_stats` - Diff statistics

## Use Cases

1. **Repository Scaffolding**: Create and configure repos
2. **Branch Protection**: Enforce policies declaratively
3. **PR Automation**: Automated PR creation and management
4. **GitOps**: Git operations in CI/CD pipelines

## Quick Example

```hcl
resource "git_repository" "myproject" {
  name        = "my-terraform-project"
  description = "Infrastructure as Code"
  visibility  = "private"
  
  features = {
    issues   = true
    wiki     = false
    projects = true
  }
}

resource "git_branch" "development" {
  repository  = git_repository.myproject.name
  name        = "development"
  protected   = true
  
  protection_rules = {
    require_pull_request = "true"
    required_approvals   = "2"
  }
}
```

## License

Apache 2.0 - See [LICENSE](../../LICENSE) for details.
