from requests import request
import time


def create_company():
    resp = request("POST", "https://api.pagar.me/1/companies/temporary")
    
    if resp.status_code not in (200, 300):
        raise Exception("Company não foi criada")
    
    resp = resp.json()

    company_id = resp["company_id"]
    api_key = resp["api_key"]["test"]
    return company_id, api_key

def update_company(candidate_github, api_key):
    url = f"https://api.pagar.me/1/company?api_key={api_key}"
    body = {
        "name": candidate_github,
        "address": {
            "street": "Rua Vitorino Carmilo",
            "complementary": "",
            "street_number": "12",
            "neighborhood": "Barra Funda",
            "city": "São Paulo",
            "state": "SP",
            "zipcode": "01153000"
        }
    }
    resp = request("PUT", url, json=body)
    if resp.status_code != 200:
        raise Exception("Company não atualizada")

def create_bank_account(api_key, count):
    url = "https://api.pagar.me/1/bank_accounts"
    body = {
        "agencia": "0932",
        "agencia_dv": "5",
        "api_key": api_key,
        "bank_code": "341",
        "conta": "58054",
        "conta_dv": "1",
        "document_number": "26268738888",
        "legal_name": f"Conta bancária {count}"
    }
    resp = request("POST", url, json=body)
    if resp.status_code not in (200, 300):
        raise Exception("Bank account não foi criada")
    resp = resp.json()
    return resp["id"]

def create_recipient(api_key, bank_account_id):
    url = "https://api.pagar.me/1/recipients/"
    body = {
        "anticipatable_volume_percentage": "85",
        "api_key": api_key,
        "automatic_anticipation_enabled": "true",
        "bank_account_id": bank_account_id,
        "transfer_day": "5",
        "transfer_enabled": "true",
        "transfer_interval": "weekly"
    }
    resp = request("POST", url, json=body)
    if resp.status_code not in (200, 300):
        raise Exception("Recipient não foi criado")
    resp = resp.json()
    return resp["id"]


def create_recipients(api_key):
    for i in range (1, 11):
        bank_account_id = create_bank_account(api_key, i)
        create_recipient(api_key, bank_account_id)
        time.sleep(1)


github_user = input("Qual o usuário do github: ")
company_name = f"desafio-front-{github_user}"

company_id, api_key = create_company()

print(company_name)
print(f"company_id: {company_id}")
print(f"api_key: {api_key}")

update_company(company_name, api_key)
create_recipients(api_key)
