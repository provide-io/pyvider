# Pyvider Examples

Canonical runnable provider examples live in a dedicated public repo, alongside the blog tutorial series that walks through building one step by step.

## Building a Provider from Scratch

A four-part tutorial series on [pyvider.com](https://pyvider.com/posts/building-your-first-provider/) with runnable provider code at every step:

| Part                                                                                                   | Adds                                    | Code                                                                                               |
| ------------------------------------------------------------------------------------------------------ | --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| [1 — Your First Resource](https://pyvider.com/posts/building-your-first-provider/)                     | `mycloud_server` resource + full CRUD   | [`part1-resource/`](https://github.com/provide-io/pyvider-tutorial/tree/main/part1-resource)       |
| [2 — Your First Data Source](https://pyvider.com/posts/building-your-first-data-source/)               | `mycloud_server_info` data source       | [`part2-data-source/`](https://github.com/provide-io/pyvider-tutorial/tree/main/part2-data-source) |
| [3 — Your First Provider Function](https://pyvider.com/posts/building-your-first-function/)            | `provider::mycloud::generate_name(...)` | [`part3-function/`](https://github.com/provide-io/pyvider-tutorial/tree/main/part3-function)       |
| [4 — Your First Ephemeral Resource](https://pyvider.com/posts/building-your-first-ephemeral-resource/) | `mycloud_session_token` ephemeral       | [`part4-ephemeral/`](https://github.com/provide-io/pyvider-tutorial/tree/main/part4-ephemeral)     |

### Clone and run

```bash
git clone https://github.com/provide-io/pyvider-tutorial.git
cd pyvider-tutorial/part1-resource
uv sync
uv run pyvider install
tofu init -upgrade
tofu apply -auto-approve
```

Each part directory is a self-contained `terraform-provider-mycloud` and can be diff'd against its predecessor to see exactly what each concept adds.

### Reproducing the asciinema casts

The same repo includes the recording pipeline that produces the casts embedded in the blog posts:

```bash
cd pyvider-tutorial
./scripts/record-all.sh            # → ./casts/tutorial-part{1..4}-*.cast
```

Requires `asciinema`, `uv`, `tofu` (or `terraform`), and Python 3 on PATH.

## Why this repo doesn't ship a demo provider anymore

Earlier Pyvider releases shipped an `examples/demo-provider/` in this repository. It was redundant with the tutorial series above — and quietly out of date because no one was running `tofu apply` against it. Keeping two canonical "full working provider" examples in sync wasn't paying off. The tutorial repo is now the single source of truth; it's public, it's tested end-to-end against each pyvider release, and each step has prose alongside the code.

If you arrived here looking for a specific pattern that used to be in `demo-provider/`, check the relevant tutorial part or [open an issue](https://github.com/provide-io/pyvider/issues) — anything worth demonstrating should live in the tutorial or in [`pyvider-components`](https://github.com/provide-io/pyvider-components).
