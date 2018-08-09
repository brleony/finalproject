def getexpensedetails(expenses, Model, detail_id, detailname, optional):
    for expense in expenses:
        if optional:
            expense[detailname] = Model.objects.filter(pk = expense[detail_id][optional]).values()[0]
        elif expense[detail_id]:
            expense[detailname] = Model.objects.filter(pk = expense[detail_id]).values()[0]
        else:
            expense[detailname] = ""
    return expenses