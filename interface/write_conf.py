import openpyxl

#filename = 'real_data.xlsx'

#xlsx = openpyxl.load_workbook(filename)
#sheet = xlsx.active
#data = sheet.rows

conf = open("write.json", "w+")

content = (
    '{"category":{"text":{"idx":[13,14,15,16]},'
    '"enumeration":{"idx":[7,8,9,10,11,12]},'
    '"interval":{"idx":[1,2,3,4,5,6]}},"if-null":{"text":{"default":0},'
    '"enumeration":{"default":1},"interval":{"default":1,"specific":{"2":0}}},'
    '"single-dist":{"text":{"default":"jaccard","specific":{"11":"equality"}},'
    '"enumeration":{"default":"equality","specific":{}},'
    '"interval":{"default":"norm","specific":{},'
    '"norm":{"1":100,"2":100,"3":100,"4":100,"5":100,"6":100}}},'
    '"group-dist":{"text":{"type":"l1","weights":{"13":2}},'
    '"enumeration":{"type":"precision","weights":{}},'
    '"interval":{"type":"l2","weights":{"1":2,"2":4}}},'
    '"final-dist":{"type":"l1","weights":{"text":2,"enumeration":3,"interval":4}}}'
)


conf.write(content)

conf.close()
