# リポジトリの説明
- psycopg2とlxml,beautifulsoup4,scrapyなどを学習した、アウトプット
- yahoo天気予報から気温、天気を取得する
- 取得したデータをpandasのデータフレームに変換した後にデータベースに登録する

# 改善点
- lxmlでなく、Scrapyを使用してClass化させるべき
- 取得できなかった場合のエラーハンドリング
- cronによる定時実行をする関係上、手動で動かすと無限に同じ結果がデータベースに追加される
