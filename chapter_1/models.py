from datetime import date
from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty:int


class Batch:
    def __init__(self, ref:str, sku:str, qty:int, eta: Optional[date]) -> None:
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations = set() # type : Set[OrderLine]

    def __gt__(self, other):
        if self.eta is None:
            return False
        
        if other.eta is None:
            return True

        return self.eta > other.eta

    # 비교 연산자중 하나 equal to -> eq
    # x == y 의 판단 기준을 정의
    def __eq__(self, other) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference
    
    def __hash__(self) -> int:
        return hash(self.reference)


    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)


    def deallocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)
    
    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity


    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty
    