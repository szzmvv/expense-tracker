import math

from flask import Flask, redirect, render_template, request, url_for

from main import add_expense_db, delete_expense_db, init_db, load_expenses_db


app = Flask(__name__)


@app.get("/")
def index():
	expenses = load_expenses_db()
	total = sum(expense["amount"] for expense in expenses)

	return render_template(
		"index.html",
		expenses=expenses,
		total=total,
		error=request.args.get("error")
	)


@app.post("/expenses")
def create_expense():
	name = request.form.get("name", "").strip()
	category = request.form.get("category", "").strip()

	if not name or not category:
		return redirect(url_for(
			"index",
			error="Заполните название и категорию"
		))

	try:
		amount = float(request.form.get("amount", ""))
	except ValueError:
		return redirect(url_for(
			"index",
			error="Введите сумму числом"
		))

	if not math.isfinite(amount) or amount <= 0:
		return redirect(url_for(
			"index",
			error="Сумма должна быть положительным конечным числом"
		))

	add_expense_db(name, amount, category)
	return redirect(url_for("index"))


@app.post("/expenses/<int:expense_id>/delete")
def delete_expense(expense_id):
	deleted_count = delete_expense_db(expense_id)

	if deleted_count == 0:
		return redirect(url_for(
			"index",
			error="Расход уже удалён или не найден"
		))

	return redirect(url_for("index"))


if __name__ == "__main__":
	init_db()
	app.run()