import requests

login_response = requests.post(
    'http://127.0.0.1:8000/api/v1/auth/login',
    json={'email': 'admin@test.com', 'password': 'admin123'}
)
access_token = login_response.json()['access_token']
headers = {'Authorization': f'Bearer {access_token}'}

# Locker assign karo student ko
locker_assign_response = requests.post(
    'http://127.0.0.1:8000/api/v1/admin/locker-assignments',
    json={
        'locker_id': 1,
        'student_id': 1,
        'start_date': '2026-09-27',
        'monthly_fee': '200.00'
    },
    headers=headers
)
print('Locker assign status:', locker_assign_response.status_code)
print('Locker assignment:', locker_assign_response.json())