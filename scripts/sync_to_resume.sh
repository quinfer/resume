#!/usr/bin/env bash
#
# sync_to_resume.sh
# -----------------
# Manually mirror canonical CV sources from research-programme (this repo)
# into a local working copy of quinfer/resume, in preparation for a
# reviewable commit-and-push into the downstream deploy repo.
#
# Usage:
#   scripts/sync_to_resume.sh [--dry-run] [--yes] [<path-to-resume-checkout>]
#   scripts/sync_to_resume.sh --help
#
# Behaviour (default):
#   1. Verifies we are at the root of the research-programme repo.
#   2. Verifies this repo has a clean working tree (fails otherwise).
#   3. Locates the resume checkout (argument, or ~/GitHub/resume, or ~/GitHub/research/resume).
#   4. Verifies the resume checkout is clean and on main.
#   5. Runs git pull inside the resume checkout to minimise later conflicts.
#   6. Uses rsync with --itemize-changes to mirror:
#        src/           data/           assets/
#        scripts/       bios.md         custom-styles.css
#      into the resume checkout, preserving file modes.
#   7. Prints git status of the resume checkout and next-step instructions.
#
# The script NEVER commits or pushes in the downstream repo. The user
# inspects, stages, commits, and pushes manually; the downstream repo's
# existing GitHub Actions workflow then rebuilds and deploys.
#
# Flags:
#   --dry-run   : show what would change but copy nothing.
#   --yes       : skip the "proceed?" prompt (useful in wrapper scripts).
#   -h, --help  : print this help and exit.

set -euo pipefail

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

dry_run=0
assume_yes=0
resume_path=""

while (("$#")); do
  case "$1" in
    --dry-run)
      dry_run=1
      shift
      ;;
    --yes|-y)
      assume_yes=1
      shift
      ;;
    -h|--help)
      sed -n '2,/^$/p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    -*)
      echo "sync_to_resume.sh: unknown flag: $1" >&2
      exit 2
      ;;
    *)
      if [[ -n "$resume_path" ]]; then
        echo "sync_to_resume.sh: only one positional argument allowed" >&2
        exit 2
      fi
      resume_path="$1"
      shift
      ;;
  esac
done

# ---------------------------------------------------------------------------
# Locate source (this repo)
# ---------------------------------------------------------------------------

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
src_root="$(cd "$script_dir/.." && pwd)"

if [[ ! -f "$src_root/research-programme.md" ]]; then
  echo "sync_to_resume.sh: cannot find research-programme.md at $src_root." >&2
  echo "Run this script from the research-programme repo." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Locate destination (quinfer/resume)
# ---------------------------------------------------------------------------

if [[ -z "$resume_path" ]]; then
  for candidate in "$HOME/GitHub/resume" "$HOME/GitHub/research/resume" "$HOME/Projects/resume"; do
    if [[ -d "$candidate/.git" ]]; then
      resume_path="$candidate"
      break
    fi
  done
fi

if [[ -z "$resume_path" ]]; then
  cat <<EOF >&2
sync_to_resume.sh: cannot find a local clone of quinfer/resume.

Please pass the path as an argument, or clone it to one of:
  ~/GitHub/resume
  ~/GitHub/research/resume
  ~/Projects/resume

For example:
  gh repo clone quinfer/resume ~/GitHub/resume
  scripts/sync_to_resume.sh
EOF
  exit 1
fi

if [[ ! -d "$resume_path/.git" ]]; then
  echo "sync_to_resume.sh: $resume_path is not a git repository." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Preflight: both repos clean, destination on main, pull latest
# ---------------------------------------------------------------------------

check_clean() {
  # Block only on modifications to tracked files (M/A/D/R/C/U in either
  # column of `git status --porcelain`). Untracked files (prefix '??') are
  # permitted because the script mirrors specific subdirectories and named
  # files only; untracked files outside those paths cannot be clobbered,
  # and untracked files inside them are rare and caller's responsibility.
  local label="$1" path="$2"
  local dirty
  dirty="$(git -C "$path" status --porcelain | grep -v '^?? ' || true)"
  if [[ -n "$dirty" ]]; then
    echo "sync_to_resume.sh: $label has uncommitted modifications to tracked files ($path):" >&2
    echo "$dirty" >&2
    echo "Commit or stash them before syncing." >&2
    exit 1
  fi
  # Surface untracked files as a non-blocking notice.
  local untracked
  untracked="$(git -C "$path" status --porcelain | grep '^?? ' || true)"
  if [[ -n "$untracked" ]]; then
    echo "sync_to_resume.sh: note — $label has untracked files (ignored by preflight):" >&2
    echo "$untracked" | sed 's/^/  /' >&2
  fi
}

check_clean "research-programme" "$src_root"
check_clean "resume"              "$resume_path"

resume_branch="$(git -C "$resume_path" rev-parse --abbrev-ref HEAD)"
if [[ "$resume_branch" != "main" ]]; then
  echo "sync_to_resume.sh: resume is on branch '$resume_branch', not 'main'." >&2
  echo "Switch to main before syncing: git -C $resume_path switch main" >&2
  exit 1
fi

echo "== Updating resume checkout =="
git -C "$resume_path" pull --ff-only

# ---------------------------------------------------------------------------
# Summary and optional confirm
# ---------------------------------------------------------------------------

src_commit="$(git -C "$src_root" rev-parse --short HEAD)"
src_msg="$(git -C "$src_root" log -1 --format='%s')"

echo
echo "== Sync plan =="
echo "Source (hub):       $src_root"
echo "Source commit:      $src_commit  $src_msg"
echo "Destination (spoke):$resume_path"
if ((dry_run)); then
  echo "Mode:               DRY RUN (no files will be written)"
else
  echo "Mode:               apply"
fi
echo

if ((assume_yes == 0 && dry_run == 0)); then
  read -r -p "Proceed with mirror into resume? [y/N] " reply
  case "$reply" in
    y|Y|yes|YES) ;;
    *) echo "Aborted."; exit 0 ;;
  esac
fi

# ---------------------------------------------------------------------------
# Mirror
# ---------------------------------------------------------------------------

rsync_flags=(--archive --itemize-changes --human-readable)
if ((dry_run)); then
  rsync_flags+=(--dry-run)
fi

mirror_dir() {
  local rel="$1"
  local hub_owned="${2:-0}"
  if [[ ! -e "$src_root/$rel" ]]; then
    echo "sync_to_resume.sh: source missing: $rel (skipping)" >&2
    return 0
  fi
  echo "-- $rel --"
  if [[ -d "$src_root/$rel" ]]; then
    mkdir -p "$resume_path/$rel"
    local -a flags=("${rsync_flags[@]}")
    # Apply --delete only for directories the hub owns in full; this
    # protects untracked working files in downstream-shared directories
    # like src/, where accreditation_form.* and similar may live.
    if (( hub_owned )); then
      flags+=(--delete)
    fi
    rsync "${flags[@]}" \
      "$src_root/$rel/" \
      "$resume_path/$rel/"
  else
    rsync "${rsync_flags[@]}" \
      "$src_root/$rel" \
      "$resume_path/$rel"
  fi
}

# Mirror each category. The second argument is 1 when the hub owns the
# directory in full (so --delete is safe); 0 when the downstream checkout
# may legitimately hold additional files. sections/ is entirely hub-owned
# by design; src/, data/, assets/, scripts/ are shared.
# sections/ holds the Quarto partials included from src/*.qmd via
# {{< include ../sections/...>}} and must be mirrored alongside src/.
mirror_dir src       0
mirror_dir sections  1
mirror_dir data      0
mirror_dir assets    0
mirror_dir scripts   0
mirror_dir bios.md
mirror_dir custom-styles.css

# ---------------------------------------------------------------------------
# Post-flight: show status in resume
# ---------------------------------------------------------------------------

echo
if ((dry_run)); then
  echo "== Dry run complete; no changes written =="
  exit 0
fi

echo "== Downstream status in $resume_path =="
git -C "$resume_path" status --short

cat <<EOF

== Next steps ==
Inspect and commit the downstream changes:

  cd "$resume_path"
  git diff                    # review changes
  git add -A
  git commit -m "Sync from research-programme $src_commit: $src_msg"
  git push

The resume repo's GitHub Actions workflow will then rebuild and deploy
to quinfer.github.io/resume/.
EOF
