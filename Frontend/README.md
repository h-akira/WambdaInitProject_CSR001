# WAMBDA CSR001 Frontend

Vue.js 3 + Vite で構築されたシングルページアプリケーション（SPA）です。CloudFront + S3 でホスティングし、WAMBDAバックエンドと統合されています。

## 概要

- **フレームワーク**: Vue.js 3
- **ビルドツール**: Vite
- **ルーティング**: Vue Router (History Mode)
- **ホスティング**: S3 + CloudFront
- **認証**: WAMBDA バックエンド (`/accounts/*`) と連携

## 開発環境

### 前提条件

- Node.js 18以上
- npm

### セットアップ

```bash
# 依存関係をインストール
npm install

# 開発サーバー起動（localhost:5173）
npm run dev

# プロダクション用ビルド
npm run build

# ビルド結果をプレビュー
npm run preview
```

## デプロイ手順

### 1. ビルド

```bash
npm run build
```

### 2. S3にアップロード

```bash
# 一括同期（古いファイルを削除）
aws s3 sync ./dist/ s3://wambda-csr001-frontend/ --delete --cache-control max-age=31536000

# index.htmlは個別にキャッシュ無効化設定
aws s3 cp ./dist/index.html s3://wambda-csr001-frontend/index.html --cache-control "no-cache, no-store, must-revalidate"
```

### 3. CloudFrontキャッシュ無効化

```bash
aws cloudfront create-invalidation --distribution-id [DISTRIBUTION_ID] --paths "/*"
```

## アーキテクチャ

### ルーティング構成

- **`/`**: Vue.js SPA（S3 + CloudFront）
- **`/accounts/*`**: WAMBDA認証画面（API Gateway）
- **`/api/*`**: API エンドポイント（API Gateway）

### 認証フロー

1. 認証が必要なページアクセス時に `/accounts/status` で認証状態確認
2. 未認証の場合は `/accounts/login` にリダイレクト
3. 認証後は元のページに戻る

### ディレクトリ構造

```
src/
├── App.vue           # メインアプリケーション
├── main.js           # エントリーポイント
└── views/            # ページコンポーネント
    ├── Home.vue      # ホームページ
    ├── Login.vue     # ログインページ（リダイレクト用）
    └── Protected.vue # 認証が必要なページ
```

## 設定

### Vue Router

```javascript
// History mode で SPA ルーティング
const router = createRouter({
  history: createWebHistory('/'),
  routes: [
    { path: '/', name: 'Home', component: Home },
    { path: '/login', name: 'Login', component: Login },
    { path: '/protected', name: 'Protected', component: Protected, meta: { requiresAuth: true } }
  ]
})
```

### 認証ガード

```javascript
// 認証が必要なページのガード
router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    try {
      const response = await fetch('/accounts/status')
      const data = await response.json()

      if (data.authenticated) {
        next()
      } else {
        window.location.href = '/accounts/login?next=' + encodeURIComponent(to.fullPath)
      }
    } catch (error) {
      window.location.href = '/accounts/login?next=' + encodeURIComponent(to.fullPath)
    }
  } else {
    next()
  }
})
```

## CloudFront設定

詳細は `/WambdaInitProject_Infra/CSR001/ManuallyCreatedResources/cloudfront.md` を参照。

### 主要設定

- **Default Behavior**: S3 オリジン（Vue.js アプリ）
- **`/accounts/*`**: API Gateway オリジン
- **`/api/*`**: API Gateway オリジン
- **Error Pages**: 404 → 200 (`/index.html`) でSPAルーティング対応

## トラブルシューティング

### よくある問題

1. **SPA ルーティングが動かない**
   - CloudFront の Error Pages 設定を確認
   - 404 エラーが `/index.html` (200) にリダイレクトされているか確認

2. **API呼び出しでCORSエラー**
   - バックエンドのCORS設定を確認
   - CloudFront の Behavior で適切にルーティングされているか確認

3. **静的ファイルが更新されない**
   - CloudFront キャッシュ無効化を実行
   - ブラウザのハードリフレッシュ（Ctrl+F5）

### デバッグ

```bash
# 開発モードでAPIテスト
npm run dev

# ローカルでプロダクションビルドをテスト
npm run build && npm run preview
```

## 本番環境URL

- **アプリケーション**: `https://[DISTRIBUTION_ID].cloudfront.net/`
- **認証**: `https://[DISTRIBUTION_ID].cloudfront.net/accounts/login`
- **API**: `https://[DISTRIBUTION_ID].cloudfront.net/api/`

## 関連ドキュメント

- [S3設定](/WambdaInitProject_Infra/CSR001/ManuallyCreatedResources/s3.md)
- [CloudFront設定](/WambdaInitProject_Infra/CSR001/ManuallyCreatedResources/cloudfront.md)
- [デプロイ手順](/WambdaInitProject_Infra/CSR001/ManuallyCreatedResources/deployment.md)