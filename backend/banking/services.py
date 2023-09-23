import requests
from .models import Token, Account
from accounts.models import User
from djmoney.money import Money

credentials = {
	"secret_id": "5aa6c2d1-2e27-4c46-b030-2d9add58a256",
	"secret_key": "3f36bdccfb992be6d8db4773e180151290e81c1b0e44bf195f15957e97efbfef204e7e0991ce98923874e03bebf3403fb5e5edc3da5db802e4f9e4aefe38432a"
}

base_url = 'https://ob.nordigen.com/api/v2'
base_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

def post(endpoint, headers = {}, body = {}):
    return requests.post(f'{base_url}{endpoint}', headers=base_headers|headers, json=body).json()

def get(endpoint, headers = {}, body = {}):
    return requests.get(f'{base_url}{endpoint}', headers=base_headers|headers, json=body).json()

def delete(endpoint, headers = {}, body = {}):
    return requests.delete(f'{base_url}{endpoint}', headers=base_headers|headers, json=body).json()

# Authentication Logic
def generate_tokens():
    return post('/token/new/', body = credentials)

def refresh_access_token(refresh_token):
    return post('/token/refresh/', body = {'refresh': refresh_token})

def new_refresh_token():
    Token.objects.all().delete()

    r = generate_tokens()
    if (r.get('status_code') in [400,401] and r.get('summary')== "Authentication failed") or r.get('secret_id') == ['This field may not be blank.']:
        return None
    else:
        token = Token(refresh_token = r['refresh'], access_token = r['access'])
        token.set_access_expiry(r['access_expires'])
        token.set_refresh_expiry(r['refresh_expires'])
        token.save()
        return token.access_token

def get_access_token(force_regenerate=False):
    if not Token.objects.all().exists():
        return new_refresh_token()

    token = Token.objects.latest('refresh_token_expiration')
    
    if (not force_regenerate and not token.access_expired()):
        return token.access_token

    # Access token needs to be refreshed
    
    if (token.refresh_expired()):
        return new_refresh_token()
    
    r = refresh_access_token(token.refresh_token)

    if r.get('status_code') == 401 and r.get('detail') == "Token is invalid or expired":
        return new_refresh_token()
    
    token.access_token = r['access']
    token.set_access_expiry(r['access_expires'])
    token.save()

    return token.access_token

def auth_request(method, endpoint, headers = {}, body = {}):
    token = get_access_token()
    r = method(endpoint, headers | {'Authorization': f'Bearer {token}'}, body)

    if isinstance(r,dict) and r.get('status_code') == 401 and r.get("detail") == "Token is invalid or expired":
        token = get_access_token(force_regenerate=True)
        r = method(endpoint, headers  | {'Authorization': f'Bearer {token}'}, body)
    return r

def auth_get(endpoint, headers = {}, body = {}):
    return auth_request(get, endpoint, headers = headers, body = body)

def auth_post(endpoint, headers = {}, body = {}):
    return auth_request(post, endpoint, headers = headers, body = body)

def auth_delete(endpoint, headers = {}, body = {}):
    return auth_request(delete, endpoint, headers = headers, body = body)

# Main Routes
def get_institutions():
    return auth_get('/institutions/?country=gb')

def get_institution(id):
    return auth_get(f'/institutions/{id}')

# Requisitions

def create_requisition(institution_id,redirect,reference):
    # institution_id, redirect, agreement, reference,
    # user_language, ssn, account_selection, redirect_immediate
    body = {
        'institution_id': institution_id,
        'redirect': redirect,
        'user_language': 'EN',
        'reference': reference
    }
    return auth_post('/requisitions/', body=body)

def get_requisitions(id=''):
    return auth_get(f'/requisitions/{id}')

def delete_requisition(id):
    return auth_delete(f'/requisitions/{id}')

# Account
def get_account_data(id):
    return auth_get(f'/accounts/{id}')

def get_account_balances(account_id):
    return auth_get(f'/accounts/{account_id}/balances/')

def get_account_transactions(account_id):
    return auth_get(f'/accounts/{account_id}/transactions/')

def get_account_details(account_id):
    return auth_get(f'/accounts/{account_id}/details/')

# Helper Methods

def update_user_accounts(user):
    accounts = Account.objects.filter(user=user)
    for i in accounts:
        if i.can_update():
            try:
                update_account_balance(i)
                update_account_transactions(i)
            except KeyError as e:
                i.last_update = None
                #print("Error with bank data received")
                if (get_account_data(i.id)['status'] == "SUSPENDED"):
                    #print('Account is suspended')
                    i.disabled = True
                    i.save()


def update_account_transactions(account):
    transaction_data = get_account_transactions(account.id)["transactions"]["booked"]
    account.add_transactions(transaction_data)
    
def update_account_balance(account):
    balance_data = get_account_balances(account.id)["balances"]
    account.add_balances(balance_data)

def account_balance(account):
    update_user_accounts(account.user)
    account.refresh_from_db()
    return account.account_balance()

def total_user_balance(user):
    update_user_accounts(user)
    accounts = Account.objects.filter(user=user)
    if accounts.exists():
        return sum(a.account_balance() for a in accounts) 
    else:
        return Money('0.0', 'GBP')

def chart_breakdown(user):
    update_user_accounts(user)
    accounts = Account.objects.filter(user=user)
    if accounts.exists():
        return [{'x': a.institution_name, 'y': a.account_balance().amount, 'id':a.id} for a in accounts]