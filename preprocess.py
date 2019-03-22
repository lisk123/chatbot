import glob
import codecs
import re

def debug():
	return 0

def get_a_string(string, i):
    if(('</div></td></tr>\n' in string[i]) or (i <= 11) or (i >= (len(string) - 5))):
        _next = i + 1
        out_string = string[i]
        return out_string, _next
    else:
        _next = i + 1
        out_string = string[i][:len(string[i]) - 1]
#        assert '&lt;br&gt;' in string[_next]
        while('</div></td></tr>\n' not in string[_next]):
#            print(i)
            assert '&lt;br&gt;' in string[_next]
            #write <br> instead
            out_string = out_string + ' br ' + string[_next][10:len(string[_next]) - 1]
            _next += 1
        out_string += string[_next][10:]
        _next += 1
        return out_string, _next

def find_substring_positions(string, substring):
    positions = [i.start() for i in re.finditer(substring, string)]
    return positions

def find_starting_pos(string):
    all_pos = find_substring_positions(string, 'div style')
    pos = all_pos[-1]
    while(string[pos] != '>'):
        pos += 1
    pos += 1
    #string[pos] = the beginning context pos
    return pos

def find_all_pics_pos(string):
    all_pics_pos = find_substring_positions(string, '<img')
    return all_pics_pos

def find_now_position(string, pic_i_pos):
    now_pos = pic_i_pos
    while(string[now_pos] != '>'):
        now_pos += 1
    now_pos += 1
    return now_pos

def is_a_blank_string(string, starting_pos):
    if(string[starting_pos:starting_pos + 16] == '</div></td></tr>'):
        return 1
    else:
        return 0

def build_a_proper_output(string):
    lost_speaker = 0
    flag_string = 'div style'
    last_pos = find_substring_positions(string, flag_string)[-1]
    speaker_pos = last_pos
    output = ''
    while((string[speaker_pos] < u'\u4e00') or (string[speaker_pos] > u'\u9fa5')):
        speaker_pos -= 1
        if(speaker_pos <= 0):
            output += '欺诈者'
            lost_speaker = 1
            break
#        assert speaker_pos > 0
    #get the speaker
    if(string[speaker_pos] == '者'):
        output += '欺诈者'
    elif(string[speaker_pos] == '员'):
        output += '我方战斗人员'
    elif(lost_speaker == 0):
        raise AssertionError()
    
    #if pictures in the string
    all_pics_pos = find_all_pics_pos(string)
    starting_pos = find_starting_pos(string)
    
    is_blank = is_a_blank_string(string, starting_pos)
    if is_blank:
        output += ' blank '
        return output, lost_speaker
    
    now_pos = starting_pos
    NUM_PICS = len(all_pics_pos)
    pic_i = 0
    #pictures at all_pics_pos ;context begins at starting_pos
    while(pic_i < NUM_PICS):
        pic_i_pos = all_pics_pos[pic_i]
        if(now_pos < pic_i_pos):
            output += string[now_pos:pic_i_pos]
            now_pos = pic_i_pos
        else:
            output += ' img '
            now_pos = find_now_position(string, pic_i_pos)
            pic_i += 1
    
    output += string[now_pos:-17]
    
    return output, lost_speaker

def build_proper_outputs(string):
    outputs = []
    _next = 0
    speaker_flag = 0
    NUM_strings = len(string)
    while(_next < NUM_strings):
#        print(get_a_string(string, 53))
        tmp_a_string, _next = get_a_string(string, _next)
#        print(tmp_a_string)
#        print(_next)
        if '</div></td></tr>\n' in tmp_a_string:
            output, lost_speaker = build_a_proper_output(tmp_a_string)
            if lost_speaker:
                speaker_flag = 1
            outputs.append(output)
#            print(build_a_proper_output(tmp_a_string))
    return outputs, speaker_flag

def get_cheat_ours(result):
    #tmp_count = 0
    ours = []
    cheat = []
    ours_write = 0
    cheat_write = 0
    
    ours_line = ''
    cheat_line = ''
    
    if result[0][0] == '我':
        ours_line += result[0][6:]
        ours_write = 1
        flag_begin = 0
    else:
        cheat_line += result[0][3:]
        cheat_write = 1
        flag_begin = 1
    
    tmp_count = 1

    while(tmp_count < len(result)):
        if(result[tmp_count - 1][0] == result[tmp_count][0]):
            if(result[tmp_count][0] == '我'):
                ours_line += ' next ' + result[tmp_count][6:]
#            print('!')
            else:
                cheat_line += ' next ' + result[tmp_count][3:]
#            print('!!')
    
        else:
            if(result[tmp_count - 1][0] == '我'):
                if cheat_write == 0:
                    cheat_line += result[tmp_count][3:]
                    cheat_write = 1
                else:
                    cheat.append(cheat_line + '\n')
                    cheat_line = result[tmp_count][3:]
#            print('?')
            else:
#            print(ours_write)
                if ours_write == 0:
                    ours_line += result[tmp_count][6:]
                    ours_write = 1
                else:
                    ours.append(ours_line + '\n')
                    ours_line = result[tmp_count][6:]
#            print('??')
        tmp_count = tmp_count + 1
#    print('666666')
#    print(tmp_count)

    ours.append(ours_line + '\n')
    cheat.append(cheat_line + '\n')

    tmp_count -= 1

    if((flag_begin == 0) & (result[tmp_count][0] == '我')):
        cheat.append(' silent ' + '\n')
    elif((flag_begin == 1) & (result[tmp_count][0] == '欺')):
        ours.append(' silent ' + '\n')
    
#    ours.append('\n')
#    cheat.append('\n')
    return ours, cheat

def write_into_files(ours, cheat, file_ours, file_cheat):
    N_ours = len(ours)
    N_cheat = len(cheat)
    assert N_ours == N_cheat
    N = N_ours
    for i in range(N):
        file_ours.write(ours[i])
        file_cheat.write(cheat[i])



if __name__ == '__main__':
    all_files = glob.glob('*/' + '*')
    f_ours = codecs.open('ours.txt', 'w', 'utf-8-sig')
    f_cheat = codecs.open('cheat.txt', 'w', 'utf-8-sig')
#    count = 0

    for all_file in all_files:
#skip the bad files
        if all_file == 'data\y-刷单-20181106-外包_6-0f89aebc3fc2fa64246f527216f59bd91a04e413.mht':
#            count += 1
            continue
        f = codecs.open(all_file, "r", "utf-8-sig")
#        print(count)
#        print(all_file)
#        count += 1
        test = f.readlines()
#    print(all_file)
        result, lost_speaker = build_proper_outputs(test)
#        if lost_speaker:
#            print('the speaker is lost in %s'%all_file)
        ours, cheat = get_cheat_ours(result)
        write_into_files(ours, cheat, f_ours, f_cheat)
#    if len(ours) != len(cheat):
#        print("len is not equal!")
#        print(all_file)
#        break
#    count += 1
    
    f_ours.close()
    f_cheat.close()
#    print(ours)
#    print(cheat)