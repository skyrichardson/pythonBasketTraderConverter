import csv
account = 'DU3062142'  # Dummy trading account so does not need to be private
time_in_force = 'DAY'
risk_per_trade_dollars = 100
basket_tag = 'SET_DAY_TRADES'


def main():
    list_of_lists = []
    with open('signals.txt', 'r') as file:
        for line in file:
            list_of_lists.append(line.strip().split('\t'))  # Use ',' for comma, '\t' for tab
    # print(list_of_lists)
    orders = [
        [
            'Action', 'Quantity', 'Symbol', 'Exchange', 'Currency', 'TimeInForce', 'OrderType',
            'LmtPrice', 'OcaGroup', 'OrderId', 'BasketTag']  # 'Account'
    ]
    for position, sublist in enumerate(list_of_lists[1:]):
        limit_price = float(sublist[3])
        aux_price = float(sublist[4])
        if aux_price == 0:  # IB requires the minimum price to be 0.0001
            aux_price = 0.01
        # print(limit_price)
        diff = limit_price - aux_price
        quantity = abs(risk_per_trade_dollars / diff)
        # print('quantity', int(round(quantity, 0)), diff)  # TODO Determine when rounding exceeds risk_per_trade_dollars
        action = 'BUY'
        stop_action = 'SELL'
        if limit_price < aux_price:
            action = 'SELL'
            stop_action = 'BUY'
        order = [
            action, int(round(quantity, 0)), sublist[2], 'SMART', 'USD', 'DAY', 'LMT',
            limit_price, '', position, '', basket_tag]  #, account]
        # print(order)
        orders.append(order)
        order = [
            stop_action, int(round(quantity, 0)), sublist[2], 'SMART', 'USD', 'DAY', 'LMT',
            aux_price, position, '', position, basket_tag]  # , account]
        orders.append(order)
    # print(orders)
    with open('orders.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(orders)







if __name__ == "__main__":
    main()
