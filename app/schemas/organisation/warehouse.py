from pydantic import BaseModel


class WarehouseStaffBase(BaseModel):
    staff_id: UUID = Field(primary_key=True)
    organisation_id: UUID = Field(primary_key=True)
    warehouse_id: UUID = Field(primary_key=True)

    warehouse: Warehouse = Relationship(
        back_populates="warehouse_staff",
        sa_relationship_kwargs={
            "primaryjoin":"and_("
                          "WarehouseStaff.warehouse_id==Warehouse.id, "
                          "WarehouseStaff.organisation_id==Warehouse.organisation_id"
                          ")"
        }
    )

    staff: "OrganisationMember" = Relationship(
        back_populates="warehouse_assignments",
        sa_relationship_kwargs={"foreign_keys":"[WarehouseStaff.staff_id, WarehouseStaff.organisation_id]"}
    )

    assigned_by_employee: "OrganisationMember" = Relationship(
        sa_relationship_kwargs={"foreign_keys":"[WarehouseStaff.assigned_by, WarehouseStaff.organisation_id]"}
    )


class WarehouseBase(BaseModel):
    name: str
    warehouse_code: str = Field(index=True)
    max_storage_units: Decimal
    status: WarehouseStatusEnum

    created_by: UUID = Field(index=True)
    manager_id: UUID = Field(index=True)

    created_by_user: "OrganisationMember" = Relationship(
        back_populates="warehouses_created",
        sa_relationship_kwargs={
            "primaryjoin":"and_("
                          "Warehouse.created_by==OrganisationMember.user_id, "
                          "Warehouse.organisation_id==OrganisationMember.organisation_id"
                          ")"
        }
    )
    manager: "OrganisationMember" = Relationship(
        back_populates="warehouses_managed",
        sa_relationship_kwargs={
            "primaryjoin":"and_("
                          "Warehouse.manager_id==OrganisationMember.user_id, "
                          "Warehouse.organisation_id==OrganisationMember.organisation_id"
                          ")"
        }
    )

    warehouse_staff: list["WarehouseStaff"] = Relationship(
        back_populates="warehouse", sa_relationship_kwargs={"lazy":"selectin"}
    )

    # warehouse-address relationship
    address_id: UUID = Field(foreign_key="address.id")
    address: "Address" = Relationship(back_populates="warehouse")

    # warehouse-organisation relationship
    organisation_id: UUID = Field(foreign_key="organisation.id")
    organisation: Organisation = Relationship(back_populates="warehouses")