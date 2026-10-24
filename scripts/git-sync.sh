#!/usr/bin/env bash
# ==============================================================================
# Git Sync & Push/Deploy Script using Token from .env
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$ROOT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Không tìm thấy file .env tại $ENV_FILE"
    exit 1
fi

# Load variables from .env
export $(grep -v '^#' "$ENV_FILE" | xargs)

if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN chưa được thiết lập trong file .env"
    exit 1
fi

USERNAME="${GITHUB_USERNAME:-kkhome1801-afk}"
REPO="${GITHUB_REPO_NAME:-KKhome}"
BRANCH="${DEPLOY_BRANCH:-main}"

AUTH_URL="https://${GITHUB_TOKEN}@github.com/${USERNAME}/${REPO}.git"
git remote set-url origin "$AUTH_URL"
echo "-> Đã đồng bộ remote origin với Token từ .env."

ACTION="$1"
MESSAGE="${2:-Auto update code $(date '+%Y-%m-%d %H:%M:%S')}"

case "$ACTION" in
    "pull")
        echo "Đang kéo mã nguồn mới nhất từ origin/$BRANCH..."
        git pull origin "$BRANCH"
        ;;
    "push"|"deploy")
        echo "Đang chuẩn bị commit và push lên origin/$BRANCH..."
        git add -A
        if ! git diff-index --quiet HEAD --; then
            git commit -m "$MESSAGE"
        fi
        git push origin "$BRANCH"
        echo "-> Push/Deploy thành công!"
        ;;
    "sync")
        echo "Đã đồng bộ Git Remote thành công."
        ;;
    *)
        echo "Cách sử dụng:"
        echo "  ./scripts/git-sync.sh pull"
        echo "  ./scripts/git-sync.sh push \"Nội dung commit\""
        echo "  ./scripts/git-sync.sh deploy \"Nội dung deploy\""
        echo "  ./scripts/git-sync.sh sync"
        ;;
esac
