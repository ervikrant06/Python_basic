from __future__ import print_function
import json
import sys
import enum
from prettytable import PrettyTable
x=PrettyTable()

cpu_list=['physicalcpu','clock','cores','enabled_cores','frequency','physid','product','threads','vendor','version']
ipmi_list=['802.1q-vlan-id','802.1q-vlan-priority','default-gateway-ip','ip-address','ip-address-source','mac-address','subnet-mask','rmcp+-cipher-suites']
network_list=['iface','driver','firmware','serial','link','product','duplex','speed','vendor']
memory_list=['description','product','size','slot','vendor','clock']
disk_list=['disk_name','model','size','vendor','SMART/serial_number','wwn-id']

with open(sys.argv[1]) as data_file:
    data=json.load(data_file)
    options=dict()
    for index,value in enumerate(sorted(data.keys()),1):
        options[index]=value
        print("{0}: {1}".format(index,value))

def display(inputlistarguments):
    if type(data[options[inputlistarguments]]) == dict:
        x.field_names=data[options[inputlistarguments]].keys()
        x.add_row([eachvalue for eachvalue in data[options[inputlistarguments]].values()])
        print(x.get_string())
    else:
        print(data[options[inputlistarguments]])

def extra_options_print(input_main_key,input_sub_key):
    if input_sub_key == 'cpu':
        x.field_names=cpu_list
        for keys in sorted(data[input_main_key][input_sub_key].keys()):
            if keys.startswith('physical_'):
                physical_cpu_list=[data[input_main_key][input_sub_key][keys][eachparameter]
                                   for eachparameter in cpu_list[1:len(cpu_list)]]
                physical_cpu_list.insert(0,keys)
                x.add_row(physical_cpu_list)
        print(x.get_string())
    elif input_sub_key == 'ipmi':
        x.field_names=ipmi_list
        x.add_row([data[input_main_key][input_sub_key]['lan'][eachparameter] for eachparameter in ipmi_list])
        print(x.get_string())
    elif input_sub_key == 'network':
        x.field_names=network_list
        for keys in sorted(data[input_main_key][input_sub_key].keys()):
                network_iface_list=[data[input_main_key][input_sub_key][keys].get(eachparameter)
                                    for eachparameter in network_list[1:len(network_list)]]
                network_iface_list.insert(0, keys)
                x.add_row(network_iface_list) # list1.insert(0,keys))
        print(x.get_string())
    elif input_sub_key == 'memory':
        x.field_names=memory_list
        for keys in sorted(data[input_main_key][input_sub_key].keys()):
            if len(memory_list) == len(data[input_main_key][input_sub_key][keys]):
                x.add_row([data[input_main_key][input_sub_key][keys][eachparameter]
                           for eachparameter in memory_list])
        print(x.get_string())
    elif input_sub_key == 'disk':
        x.field_names=disk_list
        for keys in sorted(data[input_main_key][input_sub_key].keys()):
            if not keys.startswith('logical'):
                physical_disk_list=[data[input_main_key][input_sub_key][keys].get(eachparameter)
                                    for eachparameter in disk_list[1:len(disk_list)]]
                physical_disk_list.insert(0,keys)
                x.add_row(physical_disk_list)
        print(x.get_string())
    elif input_sub_key == 'firmware':
        x.field_names=sorted(data[input_main_key][input_sub_key]['bios'].keys())
        x.add_row([eachvalue for eachvalue in
                   data[input_main_key][input_sub_key]['bios'].values()])
        print(x.get_string())
    elif input_sub_key == 'system':
        x.field_names=sorted(data[input_main_key][input_sub_key]['kernel'].keys())
        x.add_row([eachvalue for eachvalue in
                   data[input_main_key][input_sub_key]['kernel'].values()])
        print(x.get_string())

def inventory_options_print(input_main_key,input_sub_key):
    if type(data[input_main_key][input_sub_key]) == list:
        x.field_names=data[input_main_key][input_sub_key][0].keys()
        for eachelement in data[input_main_key][input_sub_key]:
            x.add_row(eachelement.values())
        print(x.get_string())
    elif type(data[input_main_key][input_sub_key]) == dict:
        x.field_names=data[input_main_key][input_sub_key].keys()
        x.add_row([eachvalue for eachvalue in
                   (data[input_main_key][input_sub_key].values())])
        print(x.get_string())
    else:
        print(data[input_main_key][input_sub_key])

def another_menu(input_values1):
    extra_options=dict()
    for index_extra,value_extra in enumerate(sorted(data[input_values1].keys()),1):
        extra_options[index_extra]=value_extra
        print("{0}: {1}".format(index_extra,value_extra))
    if input_values1 == 'inventory':
        inventory_options_print(input_values1,extra_options[int(input("Enter one numeric value: "))])
    else:
        extra_options_print(input_values1,extra_options[int(input("Enter one numeric value: "))])

def check(input_values):
    if (options[input_values] == 'extra' or options[input_values] == 'inventory'):
        another_menu(options[input_values])
    else:
        display(input_values)

def input_validation():
    inputvalues=str(input("Enter one numeric value: "))
    #if set(inputvalues).issubset(set(options.keys())):
    check(int(inputvalues))
    #else:
    #    raise('One or more input values are invalid')

input_validation()
