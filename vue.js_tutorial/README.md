# 参考サイト

Vue.js については本の手順だと、Flask のテンプレートエンジンに依存してしまう

以下のサイトを参考にする

`Vue.js(vue-cli)とFlaskを使って簡易アプリを作成する【前半 - フロントエンド編】`
https://qiita.com/mitch0807/items/2a93d93adbf6b5fc445c

`Vue.js(vue-cli)とFlaskを使って簡易アプリを作成する【後半 - サーバーサイド編】`
https://qiita.com/mitch0807/items/c2e84beee6c9a61e86cd

`Developing a Single Page App with Flask and Vue.js`
https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/

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
