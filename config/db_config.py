import psycopg2

def get_connection():
    return psycopg2.connect(
        "postgresql://postgres:cTYFDGMAcfqYIpopvUePDmCepWaasNoq@maglev.proxy.rlwy.net:12963/railway"
    )

