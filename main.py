import os
from flask import Flask, jsonify, request

app = Flask(__name__)

def bubble_sort_with_steps(arr):
    """
    버블 정렬을 수행하며 각 단계별 배열 상태와 비교/교환 정보를 기록합니다.
    """
    steps = []
    n = len(arr)
    arr_copy = arr.copy()
    
    # 초기 상태 기록
    steps.append({
        "step": 0,
        "array": list(arr_copy),
        "description": "초기 배열 상태"
    })
    
    step_count = 1
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            # 비교하는 두 원소 기록
            current_arr = list(arr_copy)
            if arr_copy[j] > arr_copy[j + 1]:
                # 값 교환 (Swap)
                arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                swapped = True
                desc = f"인덱스 {j}, {j+1} 비교 후 교환: {current_arr[j]} > {current_arr[j+1]}"
            else:
                desc = f"인덱스 {j}, {j+1} 비교 (교환 없음)"
                
            steps.append({
                "step": step_count,
                "array": list(arr_copy),
                "comparing": [j, j+1],
                "description": desc
            })
            step_count += 1
            
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
    """클라이언트로부터 배열을 받아 버블 정렬 단계별 결과를 반환하는 API 엔드포인트"""
    try:
        data = request.get_json()
        # 기본값 설정 (요청에 데이터가 없을 경우 예시 데이터 사용)
        arr = data.get('array', [64, 34, 25, 12, 22, 11, 90])
        
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
    """서버 상태 확인용 루트 엔드포인트"""
    return jsonify({"status": "online", "message": "Cloud Run Bubble Sort Server is running."}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
