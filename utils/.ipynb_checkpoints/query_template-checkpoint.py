class QTemplate:
    """
    Read all Queries from this template
    Don't Edit without sync with DW team
    All Tables must have the same name in DEV, QA, QAC and Prod ENV
    """
    
    @staticmethod
    def PlanSummary():
        return """SELECT * FROM rpterp.crd_erp_plan_summary"""
        
    @staticmethod
    def ERPDistrictTownship():
        return """SELECT * FROM rpterp.crd_erp_district_township"""
    
    @staticmethod
    def BadDebtProvision():
        return """SELECT * FROM rpterp.crd_erp_bad_debt"""
    
    @staticmethod
    def BillingAndPayment():
        return """SELECT * FROM rpterp.crd_erp_billing_and_payment"""
    
    @staticmethod
    def DataUsage():
        return """SELECT 
                        * 
                    FROM 
                        rpterp.crd_erp_monthly_customer_data_usage 
                    WHERE 
                        record_year = {{ this_year }}"""
    
    @staticmethod
    def BillingAndPaymentSubQuery():
        return """SELECT 
                        *
                    FROM 
                        rpterp.crd_erp_billing_and_payment 
                    WHERE 
                        paid_date 
                    BETWEEN 
                        '{{ start_date }}' AND '{{ end_date }}'"""