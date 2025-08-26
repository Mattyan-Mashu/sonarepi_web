from flask import Flask, render_template, request
import json

with open("recipes.json", encoding="utf-8") as f:
    recipes = json.load(f)
    
normalize_dict = {
    "ご飯": "米",
    "ライス": "米",
    "ツナ": "ツナ缶",
    "たまご": "卵",
    "玉子": "卵",
}

def normalize_ingredient(word):
    return normalize_dict.get(word, word)  # 登録されてなければそのまま返す

def matches_ingredients(recipe, available_ings):
 # レシピの材料をセット化（最初の単語だけ使う）
 recipe_ings = set(i.split()[0] for i in recipe["ingredients"])
 return available_ings.issubset(recipe_ings)

def suggest_recipes(user_ingredients):
 raw_inputs = user_ingredients
 user_ingredients = set(normalize_ingredient(word) for word in raw_inputs)
 suggested = []
 for r in recipes:
  if matches_ingredients(r, user_ingredients):
   suggested.append(r)
 return suggested

app = Flask(__name__)

@app.route("/")
def index():
 return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
 # 食材（テキストボックスから入力）
 user_ingredients = request.form["材料名"]
 # スペース区切りやカンマ区切りで複数入力できるようにする
 user_ingredients = set(user_ingredients.replace("、", " ").replace(",", " ").split())
 # レシピ検索
 recipes_result = suggest_recipes(user_ingredients)
 return render_template("result.html", recipes=recipes_result, chosen=user_ingredients)

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
 recipe = recipes[recipe_id]
 return render_template("recipe.html", recipe=recipe)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
