#!/bin/sh
# ISOLATION CANARY. Scaffolding for the Forge A04 live proof, not a real check.
#
# This script runs as whatever identity Forge's verifier runs the repository's
# checks as. It records that identity and the result of trying to reach each
# piece of Forge's own state. Every line is "<name> <ok|denied>"; Forge records
# the output in verification_checks, and the owner reads it from the ledger.
# It exits 0 always: the ledger, not this script, is where the verdict lives.
echo "identity uid=$(id -u) user=$(id -un) groups=$(id -G | tr ' ' ',')"
try(){ name=$1; shift; if "$@" >/dev/null 2>&1; then echo "$name ok"; else echo "$name denied"; fi; }
try read_ledger          cat /var/lib/forge/state/forge.db
try write_ledger         sqlite3 /var/lib/forge/state/forge.db "INSERT INTO decisions(objective_id,task_id,decision_type,allowed,reason,actor,created_at) VALUES('','','canary',1,'live canary','canary','now')"
try read_codex_auth      cat /var/lib/forge/.codex/auth.json
try read_claude_auth     cat /var/lib/forge/.claude.json
try list_backups         ls /home/forge-backups
try read_writer_codex    cat /var/lib/forge-writer/.codex/auth.json
try write_mirror         sh -c 'm=$(ls -d /var/lib/forge-repos/*/.git 2>/dev/null | head -1); test -n "$m" && git --git-dir="$m" update-ref refs/heads/isolation-canary HEAD'
try read_api_token       cat /etc/forge/api-token
try read_app_key         cat /etc/forge/github-app.pem
if env | grep -q FORGE_GH_TOKEN; then echo "token_in_env ok"; else echo "token_in_env denied"; fi
try read_forged_environ  sh -c 'p=$(pgrep -x forged | head -1); test -n "$p" && cat /proc/$p/environ'
try read_unit_credentials sh -c 'ls /run/credentials/forge.service/ && cat /run/credentials/forge.service/*'
try write_own_tree       sh -c 'echo build > .canary.out && rm -f .canary.out'
exit 0
