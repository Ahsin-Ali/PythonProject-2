import csv

customer_name = []
customer_number = []
customer_balance = []
customer_password = []

item_number = []
item_description = []
item_price = []

orders = []

total = 0.0
total_due = 0.0
quantity_item = 0
price_item = 0.0
total_price_item = 0.0
description_item = "*** item not found ***"

customer_file_name = str(input()).lower()
inventory_file_name = str(input()).lower()

with open(customer_file_name, 'r') as customer_file:
    reader = csv.reader(customer_file, delimiter=',')
    for rows in reader:
        customer_number.append(int(rows[0]))
        customer_name.append(str(rows[1]))
        customer_balance.append(float(rows[2]))
        customer_password.append(str(rows[3]))

with open(inventory_file_name, 'r') as inventory_file:
    reader = csv.reader(inventory_file)
    for rows in reader:
        item_number.append(str(rows[0]))
        item_description.append(str(rows[1]))
        item_price.append(float(rows[2]))

orders_file_name = str(input()).lower()
orders_file = open(orders_file_name, 'r')
for order in orders_file:
    if order != "EOF":
        length = len(order)
        orders.append(str(order)[:length-1])
i = 1
for transaction in orders:
    transaction_type = transaction[0:2].upper()
    if transaction_type == "CO":                        # CO for Customer order
        customer_id = int(transaction[2:7])
        if customer_id in customer_number:
            number_of_orders = int(transaction[7:10])
            invoice_type = str(transaction[10]).upper()
            input_order_date = transaction[11:]
            month = input_order_date[:2]
            day = input_order_date[2:4]
            year = input_order_date[4:8]
            order_date = month + '/' + day + '/' + year
            customer_index = customer_number.index(customer_id)
            number_customer = customer_number[customer_index]
            name_customer = customer_name[customer_index]
            balance_customer = customer_balance[customer_index]
            j = 0
            for j in range(number_of_orders):
                order = orders[i+j]
                quantity_item = int(order[:order.find('^')])
                item_id = order[order.find('^') + 1:order.rfind('^')]
                input_order_date = order[order.rfind('^') + 1:]
                month = input_order_date[:2]
                day = input_order_date[2:4]
                year = input_order_date[4:8]
                request_date_item = month + '/' + day + '/' + year
                if item_id in item_number:
                    item_index = item_number.index(item_id)
                    price_item = item_price[item_index]
                    description_item = str(item_description[item_index])
                    total_price_item = round(price_item * quantity_item, 2)
                    total += float(total_price_item)
                    total_due = total + balance_customer
                else:
                    price_item = 0.0
                    description_item = str("*** item not found ***")
                    total_price_item = 0.0
                    total += float(total_price_item)
                    total_due = total + balance_customer
                if invoice_type == "D":
                    if j == 0:
                        print("Order Date:{:>15}".format(order_date))
                        # Customer line:
                        print(" Customer:{:>15}{:>30}".format(number_customer, name_customer))
                        print("")
                        # Headings line:
                        print("{:^3} {:<18}{:<28}{:^10}{:>11}{:>11}{:>14}".format("Ln#", "Item #", "Item Description",
                                                                              "Req Date",
                                                                              "Qty", "Price", "Total"))
                    # Items line:
                    print(
                        "{:^3d} {:<18}{:<28}{:^10}{:>11d}{:>11.2f}   ${:>10.2f}".format(j+1, item_id, description_item,
                                                                                      request_date_item,
                                                                                      quantity_item, price_item,
                                                                                      total_price_item))
                    # Summary line:
                elif invoice_type == "S":
                    if j == 0:
                        print("Order Date:{:>15}".format(order_date))
                        # Customer line:
                        print(" Customer:{:>15}{:>30}".format(number_customer, name_customer))
            print("")
            print("{:>80}{:>18.2f}".format("Total Ordered:", total))
            print("{:>80}{:>18.2f}".format("Balance:", balance_customer))
            print("")
            print("{:>80}{:>18.2f}".format("Total Due:", total_due))
            print("---------------")
            customer_balance[customer_index] = total_due
            j += 1
        else:
            print("Customer number {0} is invalid".format(customer_id))
            print("---------------")
    i += 1
    total = 0.0

