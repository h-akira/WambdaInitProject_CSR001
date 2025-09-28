# WambdaInitProject_CSR001

WAMBDA + Vue.js のサンプルアプリケーション - Client-Side Rendering (CSR) アーキテクチャ

## 概要

このプロジェクトは、WAMBDAフレームワークとVue.jsを使用したモダンなWebアプリケーションのサンプルです。

### 技術スタック

- **Backend**: WAMBDA (Python), AWS Lambda, API Gateway
- **Frontend**: Vue.js 3, Vite
- **認証**: AWS Cognito
- **インフラ**: AWS SAM (Serverless Application Model)

### アーキテクチャ

```
                 ┌─────────────────────────────────┐
                 │          CloudFront             │
                 │    (Single Distribution)        │
                 └─────────────────┬───────────────┘
                                   │
                        ┌──────────┴──────────┐
                        │                     │
                        ▼                     ▼
               ┌─────────────────┐   ┌─────────────────┐
               │   S3 Bucket     │   │  API Gateway    │
               │ (Vue.js Static) │   │  (WAMBDA API)   │
               └─────────────────┘   └─────────────────┘
                        │                     │
                        │                     ▼
                        │            ┌─────────────────┐
                        │            │ Lambda Function │
                        │            │   (WAMBDA)      │
                        │            └─────────────────┘
                        │                     │
                        │                     ▼
                        │            ┌─────────────────┐
                        │            │  AWS Cognito    │
                        │            │ (Authentication)│
                        │            └─────────────────┘
                        │
                        ▼
              Vue.js SPA Routes:
              - / (Home)
              - /protected
              - /login (redirect)
```

### ルーティング設計

- `/accounts/*` → Backend Lambda (サーバーサイドレンダリング)
- `/api/*` → Backend Lambda (JSON API)
- `/*` → Frontend SPA (Vue.js)

## プロジェクト構造

```
WambdaInitProject_CSR001/
├── Backend/                    # WAMBDA バックエンド
│   ├── Lambda/
│   │   ├── lambda_function.py  # エントリーポイント
│   │   ├── project/           # プロジェクト設定
│   │   ├── accounts/          # 認証機能 (SSR)
│   │   ├── api/               # REST API
│   │   ├── templates/         # HTMLテンプレート
│   │   └── requirements.txt
│   ├── template.yaml          # SAM設定
│   └── samconfig.toml
├── Frontend/                  # Vue.js フロントエンド
│   ├── src/
│   │   ├── main.js            # エントリーポイント + ルーティング
│   │   ├── App.vue
│   │   └── views/             # ページコンポーネント
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 機能

### 認証フロー

1. **未認証ユーザー**: Vue.js Router Guard により `/accounts/login?next=/protected` にリダイレクト (SSR)
2. **ログイン**: Cognito認証後、`/?next=/protected` にリダイレクト
3. **Vue.js での処理**: `next` パラメータを読み取り、適切なページに遷移
4. **保護されたページ**: ナビゲーションバーからアカウント情報ページにアクセス可能

### ページ構成

- **Home (`/`)**: 認証状況表示、動的ナビゲーションバー
- **Protected (`/protected`)**: 認証必須、API呼び出しデモ
- **Login (`/accounts/login`)**: サーバーサイドレンダリング（Cognito認証）
- **Profile (`/accounts/profile`)**: アカウント情報、パスワード変更、アカウント削除

### ナビゲーション機能

- **未ログイン時**: ログインボタン表示
- **ログイン時**: ユーザー名（👤アイコン）表示、クリックでプロフィールページへ
- **ログアウトボタン**: 常に表示、ログアウト後は `/` にリダイレクト

### API エンドポイント

- `GET /accounts/status` - 認証状況確認（JSON）
- `POST /accounts/login` - ログイン（フォーム）
- `GET /accounts/logout` - ログアウト
- `GET /accounts/profile` - アカウント情報ページ
- `GET /api/hello` - 認証が必要な Hello World API

## 開発環境セットアップ

### 前提条件

- Python 3.13
- Node.js 20以上
- AWS CLI (設定済み)
- AWS SAM CLI

### 1. Backend セットアップ

```bash
cd Backend

# 依存関係インストール
cd Lambda
pip install -r requirements.txt
cd ..

# ローカル開発 (3つのターミナルが必要)

# ターミナル1: SAM Local API
sam local start-api --port 3000

# ターミナル2: 静的ファイルサーバー (開発時は不要)
# wambda-admin.py static --port 8080

# ターミナル3: プロキシサーバー (統合)
wambda-admin.py proxy --proxy-port 8000
```

### 2. Frontend セットアップ

```bash
cd Frontend

# 依存関係インストール
npm install

# 開発サーバー起動
npm run dev  # http://localhost:5173
```

### 3. 開発時のアクセス

- **統合開発環境**: http://localhost:8000
- **Frontend開発専用**: http://localhost:5173 (バックエンドは http://localhost:3000)

## テスト

### Backend テスト

```bash
cd Backend/Lambda
python lambda_function.py
```

インタラクティブなテストモードでパスとメソッドを指定してテスト可能。

### Frontend テスト

```bash
cd Frontend
npm run build  # プロダクションビルド
npm run preview  # ビルド結果プレビュー
```

## デプロイ

### 自動デプロイ（推奨）

CodeBuild による自動デプロイが設定されています：

```bash
# 変更をコミット
git add .
git commit -m "Update application"
git push origin main

# 自動的に以下が実行されます：
# 1. Backend変更時: sam build && sam deploy
# 2. Frontend変更時: npm run build && aws s3 sync dist/ s3://wambda-csr001-main/CloudFront/
```

### 手動デプロイ

#### Backend デプロイ

```bash
cd Backend

# SAM ビルド
sam build

# デプロイ
sam deploy --no-confirm-changeset --no-fail-on-empty-changeset
```

#### Frontend デプロイ

```bash
cd Frontend

# ビルド
npm run build

# S3 にアップロード（CloudFrontパス指定）
aws s3 sync dist/ s3://wambda-csr001-main/CloudFront/ --delete
```

#### CloudFront設定

手動設定が必要です。詳細は以下を参照：
- [CloudFront設定ドキュメント](/WambdaInitProject_Infra/CSR001/ManuallyCreatedResources/cloudfront.md)

## 環境変数

### Backend

- `DEBUG`: デバッグモード (`true`/`false`)
- `USE_MOCK`: モックデータ使用 (`true`/`false`)
- `NO_AUTH`: 認証スキップ (`true`/`false`)
- `LOG_LEVEL`: ログレベル (`DEBUG`/`INFO`/`WARNING`/`ERROR`)

### Frontend

環境による自動設定（開発時は localhost、本番は実際のドメイン）

## 開発のポイント

### 認証統合

- Vue.js アプリは `/accounts/status` で認証状況を確認
- 未認証時は Vue Router Guard により `/accounts/login?next=/protected` にリダイレクト
- ログイン成功後は常に `/?next=/protected` にリダイレクト
- Vue.js が `next` パラメータを処理して適切なページに遷移
- ユーザー名の検証: 英数字とハイフンのみ許可（全角文字は不可）

### API 通信

- フロントエンドからバックエンドAPIへの直接アクセス
- CORS設定不要（同一ドメイン）
- JWT認証によるセキュア通信

### CloudFront設定

- **Behavior 1**: `/accounts/*` → API Gateway (SSR認証ページ)
- **Behavior 2**: `/api/*` → API Gateway (JSON API)
- **Default Behavior**: `/*` → S3 (Vue.js SPA)
- **Error Pages**: 404 → 200 `/index.html` (SPA routing対応)
- **Origin Path**: S3は `/CloudFront`、API Gatewayは `/stage-01`

## トラブルシューティング

### よくある問題

1. **CORS エラー**: 開発時はバックエンドとフロントエンドが異なるポートの場合に発生
2. **認証ループ**: Mock設定時は `NO_AUTH=true` で認証をスキップ
3. **AccessDenied エラー**: `/protected` などSPAルートに直接リダイレクトした場合（現在は修正済み）
4. **認証状態エラー**: `/api/auth/status` ではなく `/accounts/status` が正しいエンドポイント
5. **ユーザー名エラー**: 全角文字は使用不可、英数字とハイフンのみ
6. **package-lock.json**: Frontendデプロイ時に必要、コミットして管理

### デバッグ

```bash
# Backend ログ確認
sam logs -n WambdaCSR001Function --tail

# CloudFront Distribution確認
aws cloudfront list-distributions --query "DistributionList.Items[?Comment=='CSR001']"

# S3コンテンツ確認
aws s3 ls s3://wambda-csr001-main/CloudFront/

# Frontend デバッグ
# ブラウザの開発者ツールでネットワークタブを確認
# Vue.js Devtools でルーティング状態を確認
```

## 本番環境

- **URL**: https://csr001.wambda.h-akira.net/
- **CloudFront Distribution**: E2NR60XQZK52KA
- **S3 Bucket**: wambda-csr001-main
- **API Gateway**: SAMデプロイ後に自動生成

## ライセンス

MIT License

## 作者

h-akira
