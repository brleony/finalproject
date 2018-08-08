def getexpensecategorynames(expenses, Category):
    for expense in expenses:
        if expense["category_id"]:
            expense["category"] = Category.objects.filter(pk = expense["category_id"]).values()[0]
        else:
            expense["category"] = ""

    return expenses