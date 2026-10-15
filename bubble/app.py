import os
from flask import Flask, jsonify, request

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

def bubble_sort_with_steps(arr):
    """
    버블 정렬을 수행하며 각 단계별 배열 상태와 비교/교환 정보를 기록합니다.
    - 입력: 숫자 배열 (예: [64, 34, 25, 12])
    - 출력: 각 단계별 상태를 담은 리스트 (steps)
    """
    steps = []
    n = len(arr)
    arr_copy = arr.copy()
    
    # 0단계: 정렬 시작 전 초기 배열 상태 기록
    steps.append({
        "step": 0,
        "array": list(arr_copy),
        "description": "초기 배열 상태"
    })
    
    step_count = 1
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            current_arr = list(arr_copy)
            
            # 인접한 두 원소 크기 비교
            if arr_copy[j] > arr_copy[j + 1]:
                # 앞의 값이 더 크면 위치 교환 (Swap)
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
                desc = f"인덱스 {j}, {j+1} 비교 후 교환: {current_arr[j]} > {current_arr[j+1]}"
            else:
                desc = f"인덱스 {j}, {j+1} 비교 (교환 없음)"
                
            # 현재 비교 및 교환 단계 기록
            steps.append({
                "step": step_count,
                "array": list(arr_copy),
                "comparing": [j, j+1], # 시각화 시 강조할 인덱스
                "description": desc
            })
            step_count += 1
            
        # 최적화: 이번 패스에서 교환이 한 번도 일어나지 않았다면 이미 정렬 완료된 상태
        if not swapped:
            break
            
    # 최종 완료 상태 기록
    steps.append({
        "step": step_count,
        "array": list(arr_copy),
        "description": "버블 정렬 완료"
    })
    return steps

@app.route('/sort', methods=['POST'])
def sort_endpoint():
    """
    클라이언트(GAS)로부터 POST 요청을 받아 버블 정렬 결과를 JSON으로 반환하는 API 엔드포인트
    """
    try:
        data = request.get_json()
        # 요청 바디에 배열 데이터가 없으면 기본값 사용
        arr = data.get('array', [64, 34, 25, 12, 22, 11, 90])
        
        # 버블 정렬 단계별 데이터 생성
        steps = bubble_sort_with_steps(arr)
        
        response_data = {
            "status": "success",
            "server_status": "정상 작동 중",
            "complexity": {
                "time": "O(n^2)",
                "space": "O(1)"
            },
            "steps": steps
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/', methods=['GET'])
def health_check():
    """서버가 정상적으로 떠 있는지 확인하기 위한 헬스체크 엔드포인트"""
    return jsonify({"status": "online", "message": "Cloud Run Bubble Sort Server (app.py) is running."}), 200

if __name__ == '__main__':
    # Cloud Run 환경 변수 PORT를 읽어오며, 로컬 테스트 시 기본값 8080 사용
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
