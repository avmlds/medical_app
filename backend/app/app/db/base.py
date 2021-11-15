# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.item import Item  # noqa
from app.models.user import User  # noqa

from app.models.patients import Patients # noqa
from app.models.patients import Diseases # noqa
from app.models.patients import Diagnoses # noqa
from app.models.patients import Procedures # noqa
from app.models.patients import ProceduresRecords # noqa
from app.models.patients import MedicalRecords # noqa
from app.models.patients import PatientAppointments # noqa
from app.models.patients import PatientPrescriptions # noqa

from app.models.warehouses import WarehouseTypes # noqa
from app.models.warehouses import MedicalItems # noqa
from app.models.warehouses import MedicalCompositions # noqa
from app.models.warehouses import WareHouses # noqa
from app.models.warehouses import WareHouseItems # noqa
from app.models.warehouses import WarehousesTransitions # noqa

from app.models.staff import Specializations # noqa
from app.models.staff import Staff # noqa

from app.models.administrative import DepartmentTypes # noqa
from app.models.administrative import OfficeTypes # noqa
from app.models.administrative import WardTypes # noqa
from app.models.administrative import Hospitals # noqa
from app.models.administrative import HospitalDepartments # noqa
from app.models.administrative import DepartmentOffices # noqa
from app.models.administrative import DepartmentWards # noqa
from app.models.administrative import WardPlaces # noqa
from app.models.administrative import OfficeStaff # noqa