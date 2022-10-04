import random
import constants as const


def gen_secret_num():
    while len(const.secret_num) != 4:
        r_num = str(random.randint(0, 9))
        if r_num in const.secret_num:
            continue
        else:
            const.secret_num = const.secret_num + r_num
    # print(f"DEBUG: secret num = {const.secret_num}")  # debug: print out secret number


def compare():
    _entered_num = const.num_input
    _correct_num = 0
    _correct_pos = 0
    if _entered_num == const.secret_num:
        const.game_state = 'won'
    else:
        for letter in _entered_num:
            letter_index = _entered_num.find(letter)
            if letter == const.secret_num[letter_index]:
                _correct_num += 1
                _correct_pos += 1
            elif _entered_num[letter_index] in const.secret_num:
                _correct_num += 1
        const.attempts += 1
        const.remaining_attempts = const.MAX_ATTEMPTS - const.attempts
        if const.attempts >= const.MAX_ATTEMPTS:
            const.game_state = 'lost'

        const.combinations.append(_entered_num)
        const.correct_num.append(_correct_num)
        const.correct_pos.append(_correct_pos)

    const.is_compared = True


def restart():
    const.correct_num = []
    const.correct_pos = []
    const.combinations = []
    const.attempts = 0
    const.game_state = 'main_game'
    const.remaining_attempts = const.MAX_ATTEMPTS
    const.secret_num = ''
    const.text_input = ""

    gen_secret_num()
