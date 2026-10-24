# HƯỚNG DẪN PULL, PUSH & DEPLOY THEO TOKEN TRONG FILE .ENV

Tài liệu này hướng dẫn cách cấu hình, bảo mật và sử dụng GitHub Personal Access Token (PAT) được lưu trữ an toàn trong file `.env` để thực hiện các thao tác **Pull**, **Push** và **Deploy** cho dự án **KKhome**.

---

## 1. Cơ Chế Lưu Trữ & Bảo Mật Token

### File cấu hình `.env`
Token truy cập GitHub được lưu trong file `.env` tại thư mục gốc dự án:

```env
# ==============================================================================
# GITHUB CONFIGURATION & DEPLOYMENT TOKEN
# ==============================================================================
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GITHUB_USERNAME=kkhome1801-afk
GITHUB_REPO_NAME=KKhome
GITHUB_REPO_URL=https://github.com/kkhome1801-afk/KKhome.git
GITHUB_AUTH_URL=https://ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/kkhome1801-afk/KKhome.git
DEPLOY_BRANCH=main
```

> [!IMPORTANT]
> - File `.env` **đã được đưa vào `.gitignore`**, đảm bảo token cá nhân **KHÔNG bao giờ bị commit hoặc lộ lên GitHub**.
> - Tuyệt đối không xóa dòng `.env*` trong file `.gitignore`.
> - Dự án đã cung cấp file mẫu `.env.example` để chia sẻ cấu trúc biến môi trường cho các thành viên trong nhóm.

---

## 2. Các Script Tiện Ích Tự Động Hóa (Khuyên dùng)

Dự án đã tích hợp sẵn script tự động đọc token từ `.env` và thao tác với Git:

### A. PowerShell trên Windows (`scripts/git-sync.ps1`)

| Thao tác | Câu lệnh PowerShell | Chức năng |
| :--- | :--- | :--- |
| **Pull code mới nhất** | `.\scripts\git-sync.ps1 -Pull` | Kéo toàn bộ code mới nhất từ branch `main` về máy |
| **Commit & Push** | `.\scripts\git-sync.ps1 -Push -Message "Ghi chú commit"` | Tự động add, commit và push lên GitHub |
| **Kiểm tra & Deploy** | `.\scripts\git-sync.ps1 -Deploy -Message "Deploy v1.0.1"` | Chạy lint/kiểm tra lỗi, commit và đẩy code triển khai |
| **Đồng bộ Remote** | `.\scripts\git-sync.ps1 -SyncRemote` | Cập nhật URL Remote của Git theo token mới nhất trong `.env` |

### B. Shell Script trên Linux / macOS / Git Bash (`scripts/git-sync.sh`)

```bash
# Cấp quyền thực thi (chỉ cần làm 1 lần)
chmod +x ./scripts/git-sync.sh

# Kéo code mới
./scripts/git-sync.sh pull

# Đẩy code lên
./scripts/git-sync.sh push "Nội dung commit"

# Deploy
./scripts/git-sync.sh deploy "Deploy phiên bản mới"

# Đồng bộ token vào Git remote
./scripts/git-sync.sh sync
```

---

## 3. Thao Tác Thủ Công Bằng Lệnh Git Chuẩn

Nếu bạn muốn sử dụng các lệnh Git truyền thống trong Terminal / VS Code:

### Bước 1: Thiết lập Git Remote với Token từ `.env`
Khi token trong `.env` được cập nhật, bạn có thể gán trực tiếp URL đã nhúng token vào remote `origin`:
```bash
git remote set-url origin https://<GITHUB_TOKEN>@github.com/kkhome1801-afk/KKhome.git
```
*(Hiện tại remote `origin` của dự án trên máy này đã được cấu hình sẵn URL nhúng token từ `.env`).*

### Bước 2: Kéo code (Pull)
```bash
git pull origin main
```

### Bước 3: Đẩy code (Push)
```bash
git add .
git commit -m "feat: cập nhật chức năng mới"
git push origin main
```

---

## 4. Quy Trình Cập Nhật & Thay Thế Token Khi Hết Hạn

Khi token GitHub của bạn hết hạn hoặc bị thu hồi (revoked):

1. Truy cập GitHub: **Settings** -> **Developer settings** -> **Personal access tokens** -> **Tokens (classic)**.
2. Bấm **Generate new token (classic)**, chọn quyền `repo` (Full control of private repositories).
3. Copy token mới (dạng `ghp_...`).
4. Mở file `.env` và cập nhật dòng:
   ```env
   GITHUB_TOKEN=ghp_token_mới_ở_đây
   ```
5. Chạy lệnh đồng bộ:
   ```powershell
   .\scripts\git-sync.ps1 -SyncRemote
   ```
   *Lập tức git remote trên máy sẽ sử dụng token mới mà không cần phải gõ lại mật khẩu.*

---

## 5. Quy Trình Build & Deploy Dự Án (Next.js)

### Chạy môi trường phát triển (Development)
```bash
npm install
npm run dev
```
Truy cập: `http://localhost:3000`

### Build kiểm tra trước khi Deploy (Production Build)
```bash
npm run build
npm run start
```

### Triển khai tự động (Vercel / Hosting)
Nếu dự án được liên kết với **Vercel** hoặc nền tảng CI/CD:
- Mỗi khi bạn chạy `.\scripts\git-sync.ps1 -Push` hoặc `-Deploy` đẩy commit lên nhánh `main`, Vercel sẽ tự động kích hoạt tiến trình build & deploy phiên bản mới nhất.
- Đảm bảo các biến môi trường khác (Supabase, API keys) đã được thêm đầy đủ trong mục **Project Settings -> Environment Variables** trên dashboard hosting.
