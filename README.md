# group-community

## 概要

いつメンのためのコミュニティページ作成 Web アプリ

## 使用技術

API - Flask(Python フレームワーク)

フロント - Vue.js

DB - GoogleCloudPlatform

## heroku へのデプロイ方法

```
## heroku へのログイン
sudo heroku login

## heroku コンテナへのログイン
sudo heroku container:login

## Docker イメージのビルドおよびプッシュ
udo heroku container:push -a group-news web

## herokuにプッシュしたDocker イメージの起動
sudo heroku container:release -a group-news web
```
