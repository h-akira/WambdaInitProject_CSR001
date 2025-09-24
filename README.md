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
┌─────────────────┐    ┌─────────────────┐
│   CloudFront    │    │   CloudFront    │
│  (Frontend SPA) │    │   (Backend API) │
└─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   S3 Bucket     │    │  API Gateway    │
│  (Static Files) │    │                 │
└─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Lambda Function│
                       │   (WAMBDA)      │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  AWS Cognito    │
                       │ (Authentication)│
                       └─────────────────┘
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
│   │   ├── main.js
│   │   ├── App.vue
│   │   ├── views/             # ページコンポーネント
│   │   └── router/            # ルーティング
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 機能

### 認証フロー

1. **未認証ユーザー**: `/accounts/login` にリダイレクト (SSR)
2. **ログイン**: Cognito認証後、Vue.js アプリにリダイレクト
3. **保護されたページ**: JWT トークンで API アクセス

### ページ構成

- **Home (`/app/`)**: 認証状況表示、Hello World
- **Protected (`/app/protected`)**: 認証必須、API呼び出しデモ
- **Login (`/accounts/login`)**: サーバーサイドレンダリング

### API エンドポイント

- `GET /api/auth/status` - 認証状況確認
- `GET /api/hello` - 認証が必要な Hello World API

## 開発環境セットアップ

### 前提条件

- Python 3.9以上
- Node.js 16以上
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

### Backend デプロイ

```bash
cd Backend

# SAM ビルド
sam build

# デプロイ
sam deploy --guided
```

### Frontend デプロイ

```bash
cd Frontend

# ビルド
npm run build

# S3 にアップロード
aws s3 sync dist/ s3://your-frontend-bucket/app/
```

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

- フロントエンドは `/api/auth/status` で認証状況を確認
- 未認証時は `/accounts/login` にリダイレクト
- ログイン後は `?next` パラメータで元のページに戻る

### API 通信

- フロントエンドからバックエンドAPIへの直接アクセス
- CORS設定不要（同一ドメイン）
- JWT認証によるセキュア通信

### CloudFront設定例

```yaml
# CloudFront Behavior 設定例
Behaviors:
  - PathPattern: "/accounts/*"
    TargetOrigin: "BackendAPIGateway"
  - PathPattern: "/api/*"
    TargetOrigin: "BackendAPIGateway"
  - PathPattern: "/app/*"
    TargetOrigin: "FrontendS3"
  - PathPattern: "/"
    TargetOrigin: "BackendAPIGateway"  # Redirect to /app/
```

## トラブルシューティング

### よくある問題

1. **CORS エラー**: 開発時はバックエンドとフロントエンドが異なるポートの場合に発生
2. **認証ループ**: Mock設定時は `NO_AUTH=true` で認証をスキップ
3. **SSM Parameter Store**: 本番では Cognito設定をSSMから読み込み

### デバッグ

```bash
# Backend ログ確認
sam logs -n WambdaCSR001Function --tail

# Frontend デバッグ
# ブラウザの開発者ツールでネットワークタブを確認
```

## ライセンス

MIT License

## 作者

h-akira
