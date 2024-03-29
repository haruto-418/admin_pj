# Admin_PJ

## firebase を利用し、ユーザーとオーダーの追加・削除を行う API です（デリバリーサービスを念頭に置いています）。

## 使用手順

&emsp; 1. Docker Compose・Docker のインストール<br>
&emsp; 2. コンテナイメージの作成<br>
&emsp; 3. コンテナの起動<br>
&emsp; 4. シェルの起動<br>

### 1. Docker Compose・Docker のインストール

- http://docs.docker.jp/engine/installation/
- https://docs.docker.jp/compose/install.html

### 2. コンテナイメージの作成

- プロジェクト直下（Dockerfile と docker-compose.yml があるディレクトリ）で`docker-compose build`を実行。

### 3. コンテナの起動

- `docker-compose build`を実行したディレクトリと同じディレクトリで`docker-compose up`を実行。

### 4. シェルの起動

- コンテナでシェルを起動し、/src で、`poetry shell`を実行。
  <br>
  <br>

## 秘密鍵の場所

プロジェクト直下に、`admin-cred.json`の名前で配置。
<br>
<br>

## エミュレータの起動について

プロジェクト直下で`firebase emulators:start`を実行。
<br>
<br>

## 使用可能ツール

- tig
- vim
- git
