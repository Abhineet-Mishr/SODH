import logging

logger = logging.getLogger(__name__)

class MemoryCreditService:
    def __init__(self, initial_balance: int = 50):
        self._balance = initial_balance

    def get_balance(self) -> int:
        return self._balance

    def deduct(self, amount: int) -> bool:
        if self._balance >= amount:
            self._balance -= amount
            logger.info(f"Deducted {amount} credits. Remaining: {self._balance}")
            return True
        logger.warning(f"Failed to deduct {amount} credits. Insufficient balance ({self._balance})")
        return False

    def refund(self, amount: int) -> None:
        self._balance += amount
        logger.info(f"Refunded {amount} credits. Remaining: {self._balance}")

# Global instance for now
credit_service = MemoryCreditService()
