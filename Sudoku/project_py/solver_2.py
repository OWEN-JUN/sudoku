
#q1=['704080906','500320008','080700300','040009060','260400051','050670040','006007090','900062004','405010607']

# q1 = ['000604700', '706000009', '000005080', '070020093', '800000005', '430010070', '050200000', '300000208', '002301000']
q1 = ['200006100', '100092080', '007000004', '029800000', '070050020', '000007350', '400000900', '080410007', '003600005']
def rotate(str_list):
    str_questionRotate=["" for i in str_list]
    for i in range(len(str_list)):
        for j in range(len(str_list)):
            str_questionRotate[i]+=str_list[j][i]
    return  str_questionRotate


def answer_sdoqu(str_question,blank=81):
    str_questionRotate=rotate(str_question)
    set_0to9=set(map(lambda a: str(a),range(10)))
    str_poscol=list(map(lambda temp_str: set_0to9 - set(list(temp_str)),str_questionRotate))
    str_posrow=list(map(lambda temp_str: set_0to9 - set(list(temp_str)),str_question))
    str_answer=["" for i in str_question]

    str_box=[set() for i in range(len(str_question))]
    for i in range(len(str_question)):
        for j in range(len(str_question)):
            if str_question[i][j]!='0':
                str_box[3*int(i/3)+int(j/3)].add(str_question[i][j])
    for i,temp in enumerate(str_box):
        str_box[i]=set_0to9-temp

    for i in range(len(str_question)):
        for j in range(len(str_question)):
            if str_question[i][j]=='0':
                if len(str_posrow[i]&str_poscol[j]&str_box[3*int(i/3)+int(j/3)])==1:
                    s=(str_posrow[i]&str_poscol[j]&str_box[3*int(i/3)+int(j/3)]).pop()
                    str_posrow[i].discard(s)
                    str_poscol[j].discard(s)
                    str_box[3*int(i/3)+int(j/3)].discard(s)
                    str_answer[i]+=s
                else:
                    str_answer[i]+='0'
            else:
                str_answer[i]+=str_question[i][j]
    # 재귀부분
    count_blank=0
    for i in str_question:
        count_blank+=i.count('0')

    if blank==count_blank:
        return str_answer
    elif count_blank>0:
        return answer_sdoqu(str_answer,count_blank)
    else:
        return str_answer

#
#
# r=answer_sdoqu(q1)
# print(r)