with open('dump_data.txt','w') as data:
    for i in range(50):
        data.write(f'{i}\tcontact{i}\t2001-03-02\tcontact_type1\t{str(i)*5}\tdescr{i}\n')
    