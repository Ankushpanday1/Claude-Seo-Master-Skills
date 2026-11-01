#!/usr/bin/env bash
# Install Claude SEO Master Skills into one or more AI coding agents.
#
#   bash install-agents.sh --tool claude|codex|cursor|antigravity|kiro|agents|all [--project DIR]
#
# Every tool reads the same Agent Skills format (a folder per skill with a
# SKILL.md). The shared Python runtime and scripts are installed once into
# $SEO_MASTER_HOME (default ~/.seo-master); each tool gets a copy of the skills
# whose script calls point at that runtime.
#
#   claude       ~/.claude/skills  + ~/.claude/agents (25 subagents)
#   codex        ~/.codex/skills   (or $CODEX_HOME/skills)
#   cursor       ~/.cursor/skills
#   antigravity  ~/.gemini/antigravity/skills
#   kiro         ~/.kiro/skills
#   agents       ~/.agents/skills  (shared location some tools also read)
#
# --no-setup skips building the Python runtime (run scripts/claude-seo setup later).
# --project DIR installs into DIR/.claude, DIR/.codex, DIR/.cursor, DIR/.agent
# (Antigravity) or DIR/.kiro instead of your home folder.
set -euo pipefail

SRC="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
HOME_DIR="${SEO_MASTER_HOME:-$HOME/.seo-master}"
TOOLS=()
PROJECT=""
SETUP=1

usage() { sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }

while [[ $# -gt 0 ]]; do
    case "$1" in
        --tool) TOOLS+=("${2:-}"); shift 2 ;;
        --project) PROJECT="${2:-}"; shift 2 ;;
        --no-setup) SETUP=0; shift ;;
        -h|--help) usage 0 ;;
        *) echo "Unknown option: $1" >&2; usage 2 ;;
    esac
done
[[ ${#TOOLS[@]} -eq 0 ]] && usage 2
if [[ " ${TOOLS[*]} " == *" all "* ]]; then TOOLS=(claude codex cursor antigravity kiro); fi

skills_dir() {
    local base
    if [[ -n "$PROJECT" ]]; then
        case "$1" in
            claude) base="$PROJECT/.claude" ;; codex) base="$PROJECT/.codex" ;;
            cursor) base="$PROJECT/.cursor" ;; antigravity) base="$PROJECT/.agent" ;;
            kiro) base="$PROJECT/.kiro" ;; agents) base="$PROJECT/.agents" ;;
        esac
    else
        case "$1" in
            claude) base="$HOME/.claude" ;; codex) base="${CODEX_HOME:-$HOME/.codex}" ;;
            cursor) base="$HOME/.cursor" ;; antigravity) base="$HOME/.gemini/antigravity" ;;
            kiro) base="$HOME/.kiro" ;; agents) base="$HOME/.agents" ;;
        esac
    fi
    [[ -n "${base:-}" ]] || { echo "Unknown tool: $1 (use claude, codex, cursor, antigravity, kiro, agents, all)" >&2; exit 2; }
    printf '%s/skills' "$base"
}

# 1. Shared runtime: scripts, schema, data, manifests. Skills are copied too so
#    cross-skill references (../seo/references/...) resolve from the runtime.
echo ">> Installing shared runtime into $HOME_DIR"
mkdir -p "$HOME_DIR"
for item in scripts schema data skills extensions hooks .claude-plugin requirements.txt pyproject.toml LICENSE; do
    [[ -e "$SRC/$item" ]] && cp -R "$SRC/$item" "$HOME_DIR/"
done
chmod +x "$HOME_DIR/scripts/claude-seo" 2>/dev/null || true

# Absolute runtime path with $HOME kept symbolic so it works in any shell.
case "$HOME_DIR" in
    "$HOME"/*) RT='$HOME'"${HOME_DIR#"$HOME"}" ;;
    *) RT="$HOME_DIR" ;;
esac
RT_ESC=$(printf '%s' "$RT" | sed 's/[#&\\]/\\&/g')

install_skills() {
    local dest="$1" count=0
    mkdir -p "$dest"
    for skill in "$SRC"/skills/*/; do
        local name; name="$(basename "$skill")"
        rm -rf "${dest:?}/$name"
        cp -R "$skill" "$dest/$name"
        find "$dest/$name" -name '*.md' -type f -print0 | xargs -0 sed -i.bak \
            -e "s#\${CLAUDE_PLUGIN_ROOT}#${RT_ESC}#g"
        find "$dest/$name" -name '*.bak' -type f -delete
        count=$((count + 1))
    done
    echo "   $count skills -> $dest"
}

for tool in "${TOOLS[@]}"; do
    dest="$(skills_dir "$tool")"
    echo ">> $tool"
    install_skills "$dest"
    if [[ "$tool" == "claude" ]]; then
        agents="$(dirname "$dest")/agents"
        mkdir -p "$agents"
        for a in "$SRC"/agents/*.md; do
            sed -e "s#\${CLAUDE_PLUGIN_ROOT}#${RT_ESC}#g" "$a" > "$agents/$(basename "$a")"
        done
        echo "   $(ls "$SRC"/agents/*.md | wc -l | tr -d ' ') agents -> $agents"
    fi
done

if [[ $SETUP -eq 1 ]]; then
echo ">> Preparing the Python runtime (one time, about 2 minutes)"
if ! "$HOME_DIR/scripts/claude-seo" setup; then
    echo "   Runtime setup did not finish. Run later: \"$HOME_DIR/scripts/claude-seo\" setup" >&2
fi
fi

cat <<EOF

Done. Restart the tool, then ask it:  "Run an SEO audit of https://yoursite.com"
In Claude Code you can also type:     /seo audit https://yoursite.com
Each audit writes SEO-Report.pdf and FIX-PROMPTS.md into <domain>-audit/.
EOF
