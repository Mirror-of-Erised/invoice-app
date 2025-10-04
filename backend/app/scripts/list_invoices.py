# backend/app/scripts/list_invoices.py
from app.services.container import get_repos

c = get_repos()
try:
    for num, total in c.invoices.list_invoice_summaries():
        print(num, total)
finally:
    c.close()
