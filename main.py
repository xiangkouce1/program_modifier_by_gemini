import typer
import os
import google.generativeai as genai
from dotenv import load_dotenv

# .envファイルからAPIキーを読み込む
load_dotenv("api.env")


# 環境変数からAPIキーを取得
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("環境変数 OPENAI_API_KEY が設定されていません。api.env を確認してください。")

# geminiクライアントの初期化
genai.configure(api_key = api_key)


# Typerアプリを作成
app = typer.Typer(help="AIを使用してファイルの内容を修正、デバッグします")

@app.command()
def main(
    file_path: str = typer.Argument(..., help="修正したいファイルパス"),
    prompt: str = typer.Option(..., "--prompt", "-p", help="AIへの修正指示")
):
    """AIを使用してファイルの内容を修正、デバッグします"""
    print("-" * 40)
    print(f"対象ファイル: {file_path}")
    print(f"修正指示: {prompt}")
    print("-" * 40)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            original_code = f.read()
            print("ファイルの読み込みが完了しました")
            print("[読み込んだ内容]")
            print(original_code)
            print("-" * 40)
            print("AIにコードの修正を依頼中")
            
            #モデル定義
            model = genai.GenerativeModel("gemini-2.5-flash")


            full_prompt = f"あなたは優秀なプログラマーです。ユーザーの指示に従って、与えられたソースコードを修正してください。修正後のコード全体のみを出力とし、解説や前置きは一切含めないでください。\n\n##指示\n\n{prompt}\n\n#ソースコード\n\n{original_code}"

            # gemini呼び出し
            response = model.generate_content(full_prompt)
            
            modified_code = response.text.strip()
            print("AIによるコード生成が完了しました")
            print("-"*40)
            print("AIが生成したコード:")
            
            if modified_code.startswith("```"):
                modified_code = modified_code.strip("`")
                if "python" in modified_code:
                    modified_code = modified_code.replace("python", "", 1).strip()
                    
            print(modified_code)

    except FileNotFoundError:
        print(f"対象ファイルのパスは見つかりません: {file_path}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()

