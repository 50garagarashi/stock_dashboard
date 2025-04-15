# Python公式イメージをベースにする（例: Python3.9）
FROM python:3.9-slim

# 作業ディレクトリを作成
WORKDIR /app

# requirements.txt をコンテナにコピーし、依存関係をインストール
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# アプリのソースコードを全てコピー
COPY . .

# Streamlitのデフォルトポート8501を利用するため、ポートを公開
EXPOSE 8501

# コンテナ起動時に実行されるコマンド
CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false"]
