from django.shortcuts import render
from django.http import JsonResponse
import random
from django.conf import settings

def rsp_game(request):
    """가위바위보 게임 뷰"""
    context = {}
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # AJAX 요청 처리
        user_choice = request.POST.get('choice')
        choices = ['rock', 'paper', 'scissors']
        computer_choice = random.choice(choices)
        
        # 승패 결정
        result = ""
        won = False
        
        if user_choice == computer_choice:
            result = "무승부"
        elif (
            (user_choice == 'rock' and computer_choice == 'scissors') or
            (user_choice == 'paper' and computer_choice == 'rock') or
            (user_choice == 'scissors' and computer_choice == 'paper')
        ):
            result = "승리"
            won = True
        else:
            result = "패배"
        
        # 승리한 경우 코인 증가
        if won:
            increase_coin(request)
        
        return JsonResponse({
            'computer_choice': computer_choice,
            'result': result,
            'won': won,
            'coin': get_remaining_coin(request)
        })
    
    # GET 요청 - 게임 페이지 표시
    context['coin'] = get_remaining_coin(request)
    return render(request, 'game/rsp_game.html', context)

def lotto_game(request):
    """로또 번호 추첨 게임 뷰"""
    context = {}
    
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # 사용자 번호 6개 받기
        user_numbers = []
        for i in range(1, 7):
            num = request.POST.get(f'number{i}')
            if num:
                user_numbers.append(int(num))
        
        # 번호 유효성 검사
        if len(user_numbers) != 6 or len(set(user_numbers)) != 6 or any(n < 1 or n > 45 for n in user_numbers):
            return JsonResponse({'error': '유효하지 않은 번호가 있습니다. 1~45 사이의 서로 다른 숫자 6개를 입력하세요.'})
        
        # 로또 번호 생성
        lotto_numbers = random.sample(range(1, 46), 6)
        
        # 맞춘 번호 개수
        matched = len(set(user_numbers) & set(lotto_numbers))
        
        # 맞춘 개수에 따라 코인 증가
        if matched >= 6:
            increase_coins(request, 5)
        elif matched == 5:
            increase_coins(request, 4)
        elif matched == 4:
            increase_coins(request, 3)
        elif matched == 3:
            increase_coins(request, 2)
        elif matched == 2:
            increase_coins(request, 1)
        
        return JsonResponse({
            'user_numbers': user_numbers,
            'lotto_numbers': lotto_numbers,
            'matched': matched,
            'coin': get_remaining_coin(request)
        })
    
    # GET 요청 - 게임 페이지 표시
    context['coin'] = get_remaining_coin(request)
    return render(request, 'game/lotto_game.html', context)

def get_remaining_coin(request):
    """현재 남은 코인 개수 계산"""
    nonmember_dict = request.session.get(settings.UPLOAD_SESSION_ID, {})
    used_count = len(nonmember_dict)
    MAX_NONMEMBER_UPLOADS = 5  # upload/views.py와 동일한 상수
    
    # 추가 코인 반영
    additional_coin = request.session.get('additional_coin', 0)
    
    return max(0, MAX_NONMEMBER_UPLOADS - used_count + additional_coin)

def increase_coin(request):
    """게임에서 승리했을 때 코인 증가"""
    additional_coin = request.session.get('additional_coin', 0)
    additional_coin += 1
    request.session['additional_coin'] = additional_coin
    request.session.modified = True

def increase_coins(request, amount):
    """게임에서 여러 코인을 획득할 때 사용"""
    additional_coin = request.session.get('additional_coin', 0)
    additional_coin += amount
    request.session['additional_coin'] = additional_coin
    request.session.modified = True