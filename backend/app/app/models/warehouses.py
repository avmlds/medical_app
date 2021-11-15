from sqlalchemy import Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


# ------------ Hospital warehouse and transitions between warehouses


class WarehouseTypes(Base):
    """Table with warehouse types, e.g. medical, clothes,
    trash(for items that were discontinued and sent to trash) etc."""

    __tablename__ = "warehouse_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    purpose = Column(String, nullable=False)


class MedicalItems(Base):
    """Various Medical items, from pills to scissors"""

    __tablename__ = "medical_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    medical_name = Column(String)
    unit = Column(String, nullable=False)
    capacity = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)


class MedicalCompositions(Base):
    """Compositions of medical items, Anti-HIV,
    Emergency medical set, etc."""

    __tablename__ = "medical_compositions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    composite_item_id = Column(Integer, ForeignKey("medical_items.id"))
    consists_from = Column(Integer, ForeignKey("medical_items.id"))
    quantity = Column(Float, nullable=False, default=1)

    item_composite = relationship("MedicalItems", foreign_keys=[composite_item_id])
    item_consists_from = relationship("MedicalItems", foreign_keys=[consists_from])


class WareHouses(Base):
    """Warehouses for departments and hospitals.
    Nullable department id and not null hospital id means
    that it is a central hospital warehouse"""

    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, autoincrement=True)

    warehouse_type = Column(Integer, ForeignKey("warehouse_types.id"), nullable=False)

    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    department_id = Column(
        Integer, ForeignKey("hospital_departments.id"), nullable=True
    )

    hospital_refs = relationship("Hospitals")
    warehouse_type_refs = relationship("WarehouseTypes")
    department_refs = relationship("HospitalDepartments")


class WareHouseItems(Base):
    """Class for storing medical items in any warehouse"""

    __tablename__ = "warehouse_items"
    id = Column(Integer, primary_key=True, autoincrement=True)

    warehouse_id = Column(Integer, ForeignKey("warehouses.id"))

    item_id = Column(Integer, ForeignKey("medical_items.id"))
    quantity = Column(Float, nullable=False, default=0)

    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    wh_rel = relationship("WareHouses")
    med_items_rel = relationship("MedicalItems")


class WarehousesTransitions(Base):
    """Class that describes transitions
    between warehouses"""

    __tablename__ = "warehouses_transitions"
    id = Column(Integer, primary_key=True, autoincrement=True)

    current_warehouse = Column(Integer, ForeignKey("warehouses.id"))
    target_warehouse = Column(Integer, ForeignKey("warehouses.id"))

    item = Column(Integer, ForeignKey("warehouse_items.id"))
    quantity = Column(Float, nullable=False, default=0)

    staff = Column(Integer, ForeignKey("staff.id"))
    target_staff = Column(Integer, ForeignKey("staff.id"))

    created_at = Column(DateTime, nullable=False)

    staff_rel = relationship("Staff", foreign_keys=[staff])
    target_staff_rel = relationship("Staff", foreign_keys=[target_staff])

    wh_rel_curr = relationship("WareHouses", foreign_keys=[current_warehouse])
    wh_rel_target = relationship("WareHouses", foreign_keys=[target_warehouse])

    med_items_rel = relationship("WareHouseItems")
