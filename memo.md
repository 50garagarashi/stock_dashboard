Dockerを使ったstreamlitアプリ構築 2025/2/21

docker build -t stock_dashboard .

docker run -p 8501:8501 stock_dashboard

docker run -p 8501:8501 -v "$(pwd):/app" stock_dashboard