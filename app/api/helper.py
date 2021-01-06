def get_broker_order(order):
    if order == 'asc':
        return 'name'
    elif order == 'desc':
        return '-name'
