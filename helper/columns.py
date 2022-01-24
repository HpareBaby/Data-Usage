class ColumnName:
    """
    - to shorten the main tidy program
    - one file rule all files
    """
    @staticmethod
    def ps_raw_cols():
        return ["id","plan_start_date", "plan_start_month", "status",
                "bill_col_day", "bill_col_time","customer_name", "customer_id",
                "plan", "program", "package", "customer_type",
                "email","phone1", "phone2", "live_type",
                "is_blacklist", "is_resller", "cid", "service_id",
                "installation_type", "used_type", "service_township_id", "billing_township_id",
                "billing_township_code_id", "billing_zone", "last_pay_month", "last_pay_year",
                "terminate_reason", "terminate_date", "billing_terminate_date","verified_customer_type",
                "sme_business_type", "deposit","refund"
               ]
    
    @staticmethod
    def ps_req_cols():
        return ["customer_id", "service_id", "cid",
                "status", "is_blacklist", "plan_start_date",
                "plan_start_month", "billing_terminate_date", "terminate_reason",
                "service_township_id", "billing_township_id", "bill_col_day",
                "customer_type", "verified_customer_type", "installation_type",
                "live_type", "sme_business_type", "is_resller", "plan", "program", "package"
               ]
    
    @staticmethod
    def ps_cols():
        return ["customer_id", "service_id", "cid",
                "status", "is_blacklist", "plan_start_date",
                "plan_start_month", "billing_terminate_date", "terminate_reason",
                "service_township_name", "billing_township_name", "bill_col_day",
                "customer_type", "verified_customer_type", "installation_type",
                "live_type", "sme_business_type", "is_resller"
               ]
    
    @staticmethod
    def twn_cols():
        return ["id", "township_code", "township_name",
                "city_id", "create_date", "write_date"
               ]
    
    @staticmethod
    def bp_cols():
        return ["invoice_id", "service_month", "invoice_type",
                "customer_id", "invoice_date", "price_total",
                "invoice_state", "payment_amount", "paid_date"
               ]
    
    @staticmethod
    def bd_cols():
        return ["customer_id", "account_name", "invoice_date",
                "bad_debt_or_provision_date", "amount_total", "currency", "rev_ex_rate"
               ]
