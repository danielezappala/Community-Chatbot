"""
Modulo per la validazione degli input
"""

class ExpenseValidator:
    @staticmethod
    def validate_category(category: str) -> tuple[bool, str]:
        """Validazione categoria con gestione quote"""
        cleaned = category.strip().replace('"','').replace("'",'').replace('“','').replace('”','')
        if not cleaned:
            return False, "❌ Categoria vuota o solo quote"
        return True, ""

    @staticmethod 
    def validate_amount(amount_str: str) -> tuple[bool, str, float]:
        """Validazione importo"""
        try:
            amount = float(amount_str.replace(',','.'))
            if amount <= 0:
                return False, "❌ Importo deve essere positivo", 0
            return True, "", amount
        except ValueError:
            return False, "❌ Importo non numerico", 0
