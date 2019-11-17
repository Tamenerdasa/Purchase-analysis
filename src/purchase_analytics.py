#
#This programe reads two input files, namely 'product.csv' and 'order_products.csv',  
#and finds the total order of a product from each department. Additionally, the program determines
# whether the product is ordered for the first time. The excel or csv files are read with csv module
# and channled to a lists and the majority of data manipulation is performed therein.
#Finally, the total order in each department, the first time order and the ratio between the latter two
# are calculated and saved in csv file. 
#
#
#Initailly the csv files are opened and saved to two different lists
#
import csv
#
product_order_interm1 = []
#
final_list = []   
#
with open('./input/order_products.csv', 'r') as csvfile:
    csv_reader1 = csv.DictReader(csvfile)
    fields1 = ['product_id','add_to_cart_order','reordered']
    global order_products_list
    order_products_list = []

    order_products_list.append(fields1)
    
    for row1 in csv_reader1:
        order_products= [row1['product_id'],row1['add_to_cart_order'],row1['reordered']]
        order_products_list.append(order_products)
#
with open('./input/products.csv', 'r') as csvfile:
    csv_reader2 = csv.DictReader(csvfile)
    fields2 = ['product_id', 'department_id']
    global products_list
    products_list = []
    products_list.append(fields2)
#       
    for row2 in csv_reader2:
        products = [row2['product_id'],row2['department_id']]
        products_list.append(products)
#
#
def mapping_dict(products_list,order_products_list):
    """
    #For sovling this particular problem, I decided to create one common dictionary file. 
    So, the idea is to map the product id in product.csv file with the one in order_product.csv, 
    which is thier common parameter. In the first section of the following programe 
    I formed a dictionary from the product id and department id of product.csv file.
    Then I add the department ids for each product id in order_products file. Finally,
    I remove the product id colomn. 
    """
    #
    global  product_order_interm1
    #
    keys = []
    values = []
    for i in products_list:
        keys.append(i[0])
        values.append(i[1])
        product_dict = dict(zip(keys, values))
#
    dept_id = []
    for x in order_products_list:
        for y in keys:
            if str(x[0]) == y:
                dept_id.append([product_dict[y]])
            else:
                continue
#
    product_order_sum = []
    for k in range(len(order_products_list)):
        product_order_sum.append(dept_id[k] + order_products_list[k])
#
#For each product id I assigned the corrosponding department id and merged 
#it with product summary list that we have in the first section.
#
    product_order_list = []
    for i in range(len(product_order_sum)):
        for j in range(len(product_order_sum[0])):
            if j != 1:
                x = product_order_sum[i][j]
                product_order_list.append(x)
            else:
                continue
#
#There is no need to keep the product id data anymore, and this part 
#just removes product id column from the above list
#
    i=0
    
    while i<len(product_order_list):
          product_order_interm1.append(product_order_list[i:i+3])
          i+=3
    return product_order_interm1
    #print(product_order_interm1)
#
#
def manipulate_interm_list(product_order_interm1):
    """
    Once I prepared the data that I needed for my problem, I did further manipulation to get the 
    total order and first time orders of ech department. For the sake of easier maniulation 
    I splitted the data on each parameter to different 
    temporary lists. Then depending on the values of the 'add_to_cart_order' and 'reordered', 
    I find the number of 'number_of_order' and 'number_of_first_orders' as well as the 
    ratio of the latter two. 
    """
    #
    temp1 = []
    temp2 = []
    temp3 = []
    temp4 = ['ratio']

    for m in range(len(product_order_interm1)):
        #for n in range(m,len(product_order_interm1[0])):
        temp1.append(product_order_interm1[m][0])
        if product_order_interm1[m][1] == 'add_to_cart_order':
            temp2.append('number_of_orders')
        elif int(product_order_interm1[m][1]) != 0:
            temp2.append(1)
        else:
            temp2.append(0)
        if product_order_interm1[m][2] == 'reordered':
            temp3.append('number_of_first_orders')
        elif int(product_order_interm1[m][2]) != 0:
            temp3.append(0)
        else:
            temp3.append(1) 
#
    dept_id_final = []
    final_list.append([temp1[0], temp2[0], temp3[0], temp4[0]])
    for n in range(len(temp1)):
        for p in range(n+1, len(temp1)):
            if temp1[n] == temp1[p]:
                total_order1 = int(temp2[n])+int(temp2[p])
                ratio = (temp3[n] or temp3[p])*((total_order1)**(-1))
                final_list.append([int(temp1[n]), total_order1, temp3[n] or temp3[p],ratio])
                dept_id_final.append(temp1[n])
                #temp4.append(int(temp3[n] or temp3[p])/total_order1)
    #print(final_list) 
    #print(unique_list)
    for m in range(1,len(temp1)):
        if temp1[m] not in dept_id_final:
                ratio = float(temp3[m]/temp2[m])
                final_list.append([int(temp1[m]), temp2[m], temp3[m],ratio])
    return final_list
    #print(final_list)
#
#
#Sorting the final list
#
    header = final_list[0]
    global main_data
    main_data = []
    for p in range(1,len(final_list)):
        main_data.append(final_list[p])
    main_data_sorted = sorted(main_data, key=lambda x: x[0])
    main_data_sorted.insert(0,header)
#
#
# The final result is piped to an output file in csv format
#
with open("./output/report.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(main_data_sorted)
#
#
#
mapping_dict(products_list,order_products_list)
#
#
manipulate_interm_list(product_order_interm1)
#
#
#sort_list(final_list)
