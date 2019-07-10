import csv
from query import *
import time

with open('faculty.csv', 'r') as fac, open('out.csv', 'w', newline='') as out:
    reader = csv.reader(fac, delimiter=',')
    writer = csv.writer(out, delimiter=',')
    counter = 0

    for row in reader:
        print("line : {}\n".format(counter))
        correct_row = ['', '', '', '', '', '', '']

        if (counter == 0):
            correct_row = ['Last Name', 'First Name', 'WOS ID', 'Affiliation Short', 'Affiliation Long', 'Department', 'Employee ID']

        else:
            last, first = row[5].split(',')

            correct_row[0] = last
            correct_row[1] = first
            correct_row[5] = row[2]
            correct_row[6] = row[0]

            try:
                print("Querying {}, {}...\n".format(last, first))
                record = query(last, first)
                # print(record)

                addresses = record['static_data']['fullrecord_metadata']['addresses']
                # print(addresses)
                if (addresses['count'] == 1):
                    addresses = [addresses['address_name']]
                else:
                    addresses = addresses['address_name']

                for address in addresses:
                    # print(address)
                    try:
                        if (address['names']['count'] == 1):
                            names = [address['names']['name']]
                        else:
                            names = address['names']['name']
                        # print(names)
                        try:
                            for name in names:
                                query_last = name['last_name']
                                try:
                                    try:
                                        query_first = name['first_name'].split('-')
                                    except:
                                        print("Couldn't split name\n")
                                    if (len(query_first) > 1):
                                        query_first = '' + query_first[0] + ' ' + query_first[1]
                                    elif(len(query_first) == 1):
                                        query_first = query_first[0]
                                except:
                                    print("Couldn't get first name for author\n")
                                #print(query_last, query_first)
                                # print("{} in {}: {}".format(last, query_last, last in query_last))
                                # print("{} in {}: {}".format(query_last, last, query_last in last))
                                # print("{} in {}: {}".format(first, query_first, first in query_first))
                                # print("{} in {}: {}".format(query_first, first, query_first in first))
                                if ((last in query_last or query_last in last)
                                        and (first in query_first or query_first in first)):
                                    try:
                                        organization = address['address_spec']['organizations']['organization']
                                        # print(organization)
                                        try:
                                            correct_row[2] = name['daisng_id']
                                        except:
                                            print("Couldn't get id\n")
                                        try:
                                            if (len(organization[0]) == 1):
                                                correct_row[3] = organization
                                            else:
                                                correct_row[3] = organization[0]
                                        except:
                                            print("Couldn't get short affiliation\n")
                                        try:
                                            correct_row[4] = organization[1]['content']
                                        except:
                                            print("Couldn't get long affiliation\n")
                                        print(correct_row)
                                        break
                                    except:
                                        print("Couldn't get organization\n")
                        except:
                            print("End of names\n")
                    except:
                        print("No names for this address\n")
            except:
                print("Empty query result for {}, {}\n".format(last, first))

        writer.writerow(correct_row)

        # if (counter == 20):
        #     break

        time.sleep(.5)
        counter += 1

    fac.close()
    out.close()
