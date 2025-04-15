Dockerを使ったstreamlitアプリ構築 2025/2/21

ビルド
docker build -t stock_dashboard .

コンテナ起動
docker run -p 8501:8501 stock_dashboard

コンテナ起動 コード変更反映
docker run -p 8501:8501 -v "$(pwd):/app" stock_dashboard