"""
Git Provider for Pyvider

This provider demonstrates managing git operations as infrastructure, including
repositories, branches, commits, pull requests, and workflows.

Novel aspects:
- Version control as infrastructure
- Declarative git operations
- Repository lifecycle management
- Collaborative workflows via Terraform
- Git automation as IaC

This is meta: Using Terraform (which is version-controlled) to manage version control systems.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any

from attrs import define, field
from pyvider.data_sources import BaseDataSource, register_data_source
from pyvider.functions import BaseFunction, register_function
from pyvider.providers import BaseProvider, register_provider
from pyvider.resources import BaseResource, register_resource
from pyvider.schema import (
    PvsSchema,
    a_bool,
    a_list,
    a_map,
    a_num,
    a_str,
    s_block,
    s_data_source,
    s_function,
    s_provider,
    s_resource,
)


# ============================================================================
# Provider
# ============================================================================


@register_provider()
class GitProvider(BaseProvider):
    """Git version control provider."""

    @define
    class Config:
        """Provider configuration."""

        api_endpoint: str = field(default="https://api.github.com")
        api_token: str = field(default="")
        default_branch: str = field(default="main")
        organization: str = field(default="")
        auto_init: bool = field(default=True)

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_provider(
            {
                "api_endpoint": a_str(
                    optional=True,
                    description="Git service API endpoint (GitHub, GitLab, etc.)",
                ),
                "api_token": a_str(
                    optional=True,
                    sensitive=True,
                    description="API authentication token",
                ),
                "default_branch": a_str(
                    optional=True,
                    description="Default branch name for new repositories",
                ),
                "organization": a_str(
                    optional=True,
                    description="Default organization/owner",
                ),
                "auto_init": a_bool(
                    optional=True,
                    description="Auto-initialize repositories with README",
                ),
            }
        )

    async def configure(self, config: Config) -> None:
        """Configure the git provider."""
        self.config = config
        # In real implementation, would initialize git API client


# ============================================================================
# Resources
# ============================================================================


@register_resource("repository")
class GitRepository(BaseResource):
    """Git repository with configuration and settings."""

    @define
    class Config:
        """Repository configuration."""

        name: str
        description: str = field(default="")
        visibility: str = field(default="private")
        default_branch: str = field(default="main")
        features: dict[str, bool] = field(factory=dict)
        topics: list[str] = field(factory=list)
        homepage: str = field(default="")
        license: str = field(default="")
        gitignore_template: str = field(default="")
        auto_init: bool = field(default=True)
        branch_protection: dict[str, Any] = field(factory=dict)
        tags: dict[str, str] = field(factory=dict)

    @define
    class State:
        """Repository state."""

        name: str
        description: str
        visibility: str
        default_branch: str
        features: dict[str, bool]
        topics: list[str]
        homepage: str
        license: str
        gitignore_template: str
        auto_init: bool
        branch_protection: dict[str, Any]
        tags: dict[str, str]
        # Computed
        repo_id: str = ""
        full_name: str = ""
        clone_url: str = ""
        ssh_url: str = ""
        html_url: str = ""
        size_kb: int = 0
        language: str = ""
        stargazers_count: int = 0
        watchers_count: int = 0
        forks_count: int = 0
        open_issues_count: int = 0
        created_at: str = ""
        updated_at: str = ""
        pushed_at: str = ""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "name": a_str(required=True, description="Repository name"),
                "description": a_str(optional=True, description="Repository description"),
                "visibility": a_str(
                    optional=True,
                    description="Visibility (private, public, internal)",
                ),
                "default_branch": a_str(optional=True, description="Default branch name"),
                "features": a_map(
                    a_bool(),
                    optional=True,
                    description="Repository features (issues, wiki, projects, etc.)",
                ),
                "topics": a_list(a_str(), optional=True, description="Repository topics/tags"),
                "homepage": a_str(optional=True, description="Project homepage URL"),
                "license": a_str(optional=True, description="License type (MIT, Apache-2.0, etc.)"),
                "gitignore_template": a_str(
                    optional=True,
                    description="Gitignore template (Python, Node, etc.)",
                ),
                "auto_init": a_bool(
                    optional=True,
                    description="Initialize with README.md",
                ),
                "branch_protection": a_map(
                    a_str(),
                    optional=True,
                    description="Branch protection rules (as JSON strings)",
                ),
                "tags": a_map(a_str(), optional=True, description="Repository tags"),
                # Computed
                "repo_id": a_str(computed=True, description="Repository ID"),
                "full_name": a_str(computed=True, description="Full repo name (owner/name)"),
                "clone_url": a_str(computed=True, description="HTTPS clone URL"),
                "ssh_url": a_str(computed=True, description="SSH clone URL"),
                "html_url": a_str(computed=True, description="Web URL"),
                "size_kb": a_num(computed=True, description="Repository size in KB"),
                "language": a_str(computed=True, description="Primary language"),
                "stargazers_count": a_num(computed=True, description="Number of stars"),
                "watchers_count": a_num(computed=True, description="Number of watchers"),
                "forks_count": a_num(computed=True, description="Number of forks"),
                "open_issues_count": a_num(computed=True, description="Open issues count"),
                "created_at": a_str(computed=True, description="Creation timestamp"),
                "updated_at": a_str(computed=True, description="Last update timestamp"),
                "pushed_at": a_str(computed=True, description="Last push timestamp"),
            }
        )

    async def _create(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Create repository."""
        config = self.Config(**base_plan)

        # Generate repository ID
        repo_id = f"repo-{hashlib.md5(config.name.encode()).hexdigest()[:12]}"

        # Simulate repository creation
        owner = "example-org"
        full_name = f"{owner}/{config.name}"

        state = {
            **base_plan,
            "repo_id": repo_id,
            "full_name": full_name,
            "clone_url": f"https://github.com/{full_name}.git",
            "ssh_url": f"git@github.com:{full_name}.git",
            "html_url": f"https://github.com/{full_name}",
            "size_kb": 0,  # New repo
            "language": "",
            "stargazers_count": 0,
            "watchers_count": 0,
            "forks_count": 0,
            "open_issues_count": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "pushed_at": "",
        }

        return state, None

    async def read(self, ctx: Any) -> State | None:
        """Read repository state."""
        return self.State(**ctx.state.model_dump())

    async def _update(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Update repository settings."""
        updated_state = {
            **base_plan,
            "repo_id": ctx.state.repo_id,
            "full_name": ctx.state.full_name,
            "clone_url": ctx.state.clone_url,
            "ssh_url": ctx.state.ssh_url,
            "html_url": ctx.state.html_url,
            "size_kb": ctx.state.size_kb,
            "language": ctx.state.language,
            "stargazers_count": ctx.state.stargazers_count,
            "watchers_count": ctx.state.watchers_count,
            "forks_count": ctx.state.forks_count,
            "open_issues_count": ctx.state.open_issues_count,
            "created_at": ctx.state.created_at,
            "updated_at": datetime.now().isoformat(),
            "pushed_at": ctx.state.pushed_at,
        }

        return updated_state, None

    async def _delete(self, ctx: Any) -> None:
        """Delete repository."""
        # In real implementation, would delete repo
        pass


@register_resource("branch")
class GitBranch(BaseResource):
    """Git branch with protection rules."""

    @define
    class Config:
        """Branch configuration."""

        repository: str
        name: str
        source_branch: str = field(default="main")
        protected: bool = field(default=False)
        protection_rules: dict[str, Any] = field(factory=dict)

    @define
    class State:
        """Branch state."""

        repository: str
        name: str
        source_branch: str
        protected: bool
        protection_rules: dict[str, Any]
        # Computed
        branch_id: str = ""
        commit_sha: str = ""
        commit_message: str = ""
        commit_author: str = ""
        commit_date: str = ""
        ahead_by: int = 0
        behind_by: int = 0
        created_at: str = ""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "repository": a_str(required=True, description="Repository name"),
                "name": a_str(required=True, description="Branch name"),
                "source_branch": a_str(
                    optional=True,
                    description="Source branch to branch from",
                ),
                "protected": a_bool(optional=True, description="Enable branch protection"),
                "protection_rules": a_map(
                    a_str(),
                    optional=True,
                    description="Protection rules (as JSON strings)",
                ),
                # Computed
                "branch_id": a_str(computed=True, description="Branch ID"),
                "commit_sha": a_str(computed=True, description="Latest commit SHA"),
                "commit_message": a_str(computed=True, description="Latest commit message"),
                "commit_author": a_str(computed=True, description="Latest commit author"),
                "commit_date": a_str(computed=True, description="Latest commit date"),
                "ahead_by": a_num(
                    computed=True,
                    description="Commits ahead of source branch",
                ),
                "behind_by": a_num(
                    computed=True,
                    description="Commits behind source branch",
                ),
                "created_at": a_str(computed=True, description="Branch creation time"),
            }
        )

    async def _create(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Create branch."""
        config = self.Config(**base_plan)

        # Generate branch ID
        branch_id = f"branch-{hashlib.md5(config.name.encode()).hexdigest()[:8]}"

        # Simulate branch creation
        commit_sha = hashlib.sha1(f"{config.repository}-{config.name}".encode()).hexdigest()

        state = {
            **base_plan,
            "branch_id": branch_id,
            "commit_sha": commit_sha,
            "commit_message": "Initial commit",
            "commit_author": "terraform",
            "commit_date": datetime.now().isoformat(),
            "ahead_by": 0,
            "behind_by": 0,
            "created_at": datetime.now().isoformat(),
        }

        return state, None

    async def read(self, ctx: Any) -> State | None:
        """Read branch state."""
        return self.State(**ctx.state.model_dump())

    async def _update(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Update branch (e.g., protection rules)."""
        updated_state = {
            **base_plan,
            "branch_id": ctx.state.branch_id,
            "commit_sha": ctx.state.commit_sha,
            "commit_message": ctx.state.commit_message,
            "commit_author": ctx.state.commit_author,
            "commit_date": ctx.state.commit_date,
            "ahead_by": ctx.state.ahead_by,
            "behind_by": ctx.state.behind_by,
            "created_at": ctx.state.created_at,
        }

        return updated_state, None

    async def _delete(self, ctx: Any) -> None:
        """Delete branch."""
        pass


@register_resource("pull_request")
class GitPullRequest(BaseResource):
    """Git pull request / merge request."""

    @define
    class Config:
        """Pull request configuration."""

        repository: str
        title: str
        head_branch: str
        base_branch: str
        body: str = field(default="")
        draft: bool = field(default=False)
        maintainer_can_modify: bool = field(default=True)
        labels: list[str] = field(factory=list)
        assignees: list[str] = field(factory=list)
        reviewers: list[str] = field(factory=list)
        milestone: str = field(default="")

    @define
    class State:
        """Pull request state."""

        repository: str
        title: str
        head_branch: str
        base_branch: str
        body: str
        draft: bool
        maintainer_can_modify: bool
        labels: list[str]
        assignees: list[str]
        reviewers: list[str]
        milestone: str
        # Computed
        pr_id: str = ""
        pr_number: int = 0
        state: str = "open"
        html_url: str = ""
        diff_url: str = ""
        patch_url: str = ""
        mergeable: bool = False
        merged: bool = False
        merge_commit_sha: str = ""
        commits_count: int = 0
        changed_files: int = 0
        additions: int = 0
        deletions: int = 0
        created_at: str = ""
        updated_at: str = ""
        merged_at: str = ""
        closed_at: str = ""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_resource(
            {
                "repository": a_str(required=True, description="Repository name"),
                "title": a_str(required=True, description="PR title"),
                "head_branch": a_str(required=True, description="Source branch (head)"),
                "base_branch": a_str(required=True, description="Target branch (base)"),
                "body": a_str(optional=True, description="PR description"),
                "draft": a_bool(optional=True, description="Create as draft PR"),
                "maintainer_can_modify": a_bool(
                    optional=True,
                    description="Allow maintainers to edit",
                ),
                "labels": a_list(a_str(), optional=True, description="PR labels"),
                "assignees": a_list(a_str(), optional=True, description="Assignees"),
                "reviewers": a_list(a_str(), optional=True, description="Reviewers"),
                "milestone": a_str(optional=True, description="Milestone"),
                # Computed
                "pr_id": a_str(computed=True, description="Pull request ID"),
                "pr_number": a_num(computed=True, description="PR number"),
                "state": a_str(computed=True, description="PR state (open, closed, merged)"),
                "html_url": a_str(computed=True, description="Web URL"),
                "diff_url": a_str(computed=True, description="Diff URL"),
                "patch_url": a_str(computed=True, description="Patch URL"),
                "mergeable": a_bool(computed=True, description="Can be merged"),
                "merged": a_bool(computed=True, description="Has been merged"),
                "merge_commit_sha": a_str(computed=True, description="Merge commit SHA"),
                "commits_count": a_num(computed=True, description="Number of commits"),
                "changed_files": a_num(computed=True, description="Number of changed files"),
                "additions": a_num(computed=True, description="Lines added"),
                "deletions": a_num(computed=True, description="Lines deleted"),
                "created_at": a_str(computed=True, description="Creation time"),
                "updated_at": a_str(computed=True, description="Last update time"),
                "merged_at": a_str(computed=True, description="Merge time"),
                "closed_at": a_str(computed=True, description="Close time"),
            }
        )

    async def _create(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Create pull request."""
        config = self.Config(**base_plan)

        # Generate PR ID and number
        pr_id = f"pr-{hashlib.md5(config.title.encode()).hexdigest()[:8]}"
        pr_number = hash(config.title) % 1000 + 1

        state = {
            **base_plan,
            "pr_id": pr_id,
            "pr_number": pr_number,
            "state": "draft" if config.draft else "open",
            "html_url": f"https://github.com/{config.repository}/pull/{pr_number}",
            "diff_url": f"https://github.com/{config.repository}/pull/{pr_number}.diff",
            "patch_url": f"https://github.com/{config.repository}/pull/{pr_number}.patch",
            "mergeable": True,
            "merged": False,
            "merge_commit_sha": "",
            "commits_count": 1,
            "changed_files": 3,
            "additions": 125,
            "deletions": 42,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "merged_at": "",
            "closed_at": "",
        }

        return state, None

    async def read(self, ctx: Any) -> State | None:
        """Read pull request state."""
        return self.State(**ctx.state.model_dump())

    async def _update(self, ctx: Any, base_plan: dict) -> tuple[dict | None, bytes | None]:
        """Update pull request (e.g., labels, reviewers)."""
        updated_state = {
            **base_plan,
            "pr_id": ctx.state.pr_id,
            "pr_number": ctx.state.pr_number,
            "state": ctx.state.state,
            "html_url": ctx.state.html_url,
            "diff_url": ctx.state.diff_url,
            "patch_url": ctx.state.patch_url,
            "mergeable": ctx.state.mergeable,
            "merged": ctx.state.merged,
            "merge_commit_sha": ctx.state.merge_commit_sha,
            "commits_count": ctx.state.commits_count,
            "changed_files": ctx.state.changed_files,
            "additions": ctx.state.additions,
            "deletions": ctx.state.deletions,
            "created_at": ctx.state.created_at,
            "updated_at": datetime.now().isoformat(),
            "merged_at": ctx.state.merged_at,
            "closed_at": ctx.state.closed_at,
        }

        return updated_state, None

    async def _delete(self, ctx: Any) -> None:
        """Delete (close) pull request."""
        pass


# ============================================================================
# Data Sources
# ============================================================================


@register_data_source("repository_info")
class RepositoryInfo(BaseDataSource):
    """Query repository information."""

    @define
    class Config:
        """Data source configuration."""

        name: str
        owner: str = field(default="")

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source(
            {
                "name": a_str(required=True, description="Repository name"),
                "owner": a_str(optional=True, description="Repository owner"),
                # Computed
                "id": a_str(computed=True, description="Query ID"),
                "full_name": a_str(computed=True, description="Full name"),
                "description": a_str(computed=True, description="Description"),
                "visibility": a_str(computed=True, description="Visibility"),
                "clone_url": a_str(computed=True, description="Clone URL"),
                "default_branch": a_str(computed=True, description="Default branch"),
                "language": a_str(computed=True, description="Primary language"),
                "size_kb": a_num(computed=True, description="Size in KB"),
                "stargazers_count": a_num(computed=True, description="Stars"),
                "forks_count": a_num(computed=True, description="Forks"),
                "open_issues_count": a_num(computed=True, description="Open issues"),
                "topics": a_list(a_str(), computed=True, description="Topics"),
                "license": a_str(computed=True, description="License"),
                "created_at": a_str(computed=True, description="Created at"),
                "updated_at": a_str(computed=True, description="Updated at"),
            }
        )

    async def read(self, ctx: Any) -> dict[str, Any]:
        """Read repository information."""
        config = self.Config(**ctx.config.model_dump())

        owner = config.owner or "example-org"
        full_name = f"{owner}/{config.name}"

        return {
            "id": f"repo-info-{hashlib.md5(full_name.encode()).hexdigest()[:8]}",
            "full_name": full_name,
            "description": "Example repository",
            "visibility": "public",
            "clone_url": f"https://github.com/{full_name}.git",
            "default_branch": "main",
            "language": "Python",
            "size_kb": 1024,
            "stargazers_count": 42,
            "forks_count": 7,
            "open_issues_count": 3,
            "topics": ["python", "terraform", "automation"],
            "license": "MIT",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": datetime.now().isoformat(),
        }


@register_data_source("pull_requests")
class PullRequests(BaseDataSource):
    """Query pull requests for a repository."""

    @define
    class Config:
        """Data source configuration."""

        repository: str
        state: str = field(default="open")
        base_branch: str = field(default="")
        head_branch: str = field(default="")

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_data_source(
            {
                "repository": a_str(required=True, description="Repository name"),
                "state": a_str(
                    optional=True,
                    description="Filter by state (open, closed, all)",
                ),
                "base_branch": a_str(optional=True, description="Filter by base branch"),
                "head_branch": a_str(optional=True, description="Filter by head branch"),
                # Computed
                "id": a_str(computed=True, description="Query ID"),
                "pull_requests": a_list(
                    s_block(
                        {
                            "number": a_num(description="PR number"),
                            "title": a_str(description="PR title"),
                            "state": a_str(description="PR state"),
                            "head_branch": a_str(description="Head branch"),
                            "base_branch": a_str(description="Base branch"),
                            "author": a_str(description="Author"),
                            "created_at": a_str(description="Created at"),
                        }
                    ),
                    computed=True,
                    description="List of pull requests",
                ),
                "count": a_num(computed=True, description="Number of PRs"),
            }
        )

    async def read(self, ctx: Any) -> dict[str, Any]:
        """Read pull requests."""
        config = self.Config(**ctx.config.model_dump())

        # Simulate querying PRs
        prs = [
            {
                "number": 123,
                "title": "Add new feature",
                "state": "open",
                "head_branch": "feature/new-feature",
                "base_branch": "main",
                "author": "alice",
                "created_at": "2024-11-10T10:00:00Z",
            },
            {
                "number": 124,
                "title": "Fix bug in auth",
                "state": "open",
                "head_branch": "fix/auth-bug",
                "base_branch": "main",
                "author": "bob",
                "created_at": "2024-11-11T14:30:00Z",
            },
        ]

        # Filter by state if specified
        if config.state and config.state != "all":
            prs = [pr for pr in prs if pr["state"] == config.state]

        return {
            "id": f"prs-{hashlib.md5(config.repository.encode()).hexdigest()[:8]}",
            "pull_requests": prs,
            "count": len(prs),
        }


# ============================================================================
# Functions
# ============================================================================


@register_function("generate_branch_name")
class GenerateBranchName(BaseFunction):
    """Generate standardized branch names."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            {
                "type": a_str(description="Branch type (feature, fix, hotfix, release)"),
                "description": a_str(description="Brief description"),
                "issue_number": a_str(description="Issue/ticket number (optional)"),
            },
            a_str(description="Generated branch name"),
        )

    async def call(self, type: str, description: str, issue_number: str) -> str:
        """Generate branch name."""
        # Convert description to slug
        slug = description.lower().replace(" ", "-").replace("_", "-")

        # Remove special characters
        slug = "".join(c for c in slug if c.isalnum() or c == "-")

        # Format: type/description or type/issue-description
        if issue_number:
            return f"{type}/{issue_number}-{slug}"
        else:
            return f"{type}/{slug}"


@register_function("parse_commit_message")
class ParseCommitMessage(BaseFunction):
    """Parse conventional commit messages."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            {
                "commit_message": a_str(description="Commit message to parse"),
            },
            a_map(a_str(), description="Parsed commit components"),
        )

    async def call(self, commit_message: str) -> dict[str, str]:
        """Parse commit message following conventional commits."""
        # Simple parser for: type(scope): description
        lines = commit_message.strip().split("\n", 1)
        first_line = lines[0]

        commit_type = "unknown"
        scope = ""
        description = first_line
        body = lines[1] if len(lines) > 1 else ""

        # Try to parse type(scope): description format
        if ":" in first_line:
            header, description = first_line.split(":", 1)
            description = description.strip()

            if "(" in header and ")" in header:
                commit_type = header.split("(")[0]
                scope = header.split("(")[1].split(")")[0]
            else:
                commit_type = header

        return {
            "type": commit_type,
            "scope": scope,
            "description": description,
            "body": body.strip(),
        }


@register_function("validate_branch_name")
class ValidateBranchName(BaseFunction):
    """Validate branch name against conventions."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            {
                "branch_name": a_str(description="Branch name to validate"),
            },
            a_bool(description="Whether branch name is valid"),
        )

    async def call(self, branch_name: str) -> bool:
        """Validate branch name."""
        # Check for valid format: type/description
        if "/" not in branch_name:
            return False

        parts = branch_name.split("/", 1)
        if len(parts) != 2:
            return False

        branch_type, description = parts

        # Valid types
        valid_types = {"feature", "fix", "hotfix", "release", "chore", "docs", "test"}
        if branch_type not in valid_types:
            return False

        # Description should be kebab-case (lowercase with hyphens)
        if not description:
            return False

        # Should not have spaces or uppercase
        if " " in description or description != description.lower():
            return False

        return True


@register_function("calculate_diff_stats")
class CalculateDiffStats(BaseFunction):
    """Calculate statistics from git diff."""

    @classmethod
    def get_schema(cls) -> PvsSchema:
        return s_function(
            {
                "additions": a_num(description="Lines added"),
                "deletions": a_num(description="Lines deleted"),
                "changed_files": a_num(description="Files changed"),
            },
            a_map(a_str(), description="Diff statistics"),
        )

    async def call(
        self,
        additions: float,
        deletions: float,
        changed_files: float,
    ) -> dict[str, str]:
        """Calculate diff statistics."""
        total_changes = additions + deletions
        churn_ratio = deletions / total_changes if total_changes > 0 else 0

        # Calculate average changes per file
        avg_changes_per_file = total_changes / changed_files if changed_files > 0 else 0

        # Determine change magnitude
        if total_changes < 10:
            magnitude = "trivial"
        elif total_changes < 100:
            magnitude = "small"
        elif total_changes < 500:
            magnitude = "medium"
        elif total_changes < 1000:
            magnitude = "large"
        else:
            magnitude = "huge"

        return {
            "total_changes": str(int(total_changes)),
            "churn_ratio": f"{churn_ratio:.2f}",
            "avg_changes_per_file": f"{avg_changes_per_file:.1f}",
            "magnitude": magnitude,
        }
